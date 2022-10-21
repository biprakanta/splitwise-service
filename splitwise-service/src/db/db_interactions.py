# pylint: disable=relative-beyond-top-level

from pydantic import UUID4
from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import exists
from sqlalchemy.sql.selectable import Select

from ..utils.consts import CFConfigServiceConts
from ..utils.exceptions import DuplicateNameException, ConfigDoesNotExist
from .models import CustomFieldConfig, CustomFieldEntityRelation
from .schema import CustomFieldsConfigCreate


def get_cf_config_by_id(db: Session, tenant_id: str, config_id: str) -> Select:
    select_statement = (
        select(CustomFieldConfig)
        .where(CustomFieldConfig.tenant_id == tenant_id)
        .where(CustomFieldConfig.id == config_id)
    )
    result = db.execute(select_statement).scalar()
    return result


def get_cf_config_by_relation_id(
    db: Session,
    tenant_id: str,
    relation_id: str,
    relation_type: str,
    is_active: bool,
    sort_by: CFConfigServiceConts.SortByParams = CFConfigServiceConts.SortByParams.created_at,
    order: CFConfigServiceConts.Order = CFConfigServiceConts.Order.asc,
    paginate: bool = True,
    page: int = 1,
    page_size: int = 10,
) -> Select:
    select_statement = select(CustomFieldConfig)
    select_statement = (
        select_statement.join(CustomFieldEntityRelation)
        .where(CustomFieldEntityRelation.cf_config_id == CustomFieldConfig.id)
        .where(CustomFieldEntityRelation.tenant_id == tenant_id)
        .where(CustomFieldEntityRelation.relation_id == relation_id)
        .where(CustomFieldEntityRelation.relation_type == relation_type)
    )
    if is_active:
        select_statement = select_statement.where(CustomFieldConfig.is_active is True)
    if sort_by == CFConfigServiceConts.SortByParams.created_at:
        if order == CFConfigServiceConts.Order.desc:
            select_statement = select_statement.order_by(
                CustomFieldConfig.created_at.desc()
            )
        else:
            select_statement = select_statement.order_by(
                CustomFieldConfig.created_at.asc()
            )
    elif sort_by == CFConfigServiceConts.SortByParams.alpha:
        if order == CFConfigServiceConts.Order.desc:
            select_statement = select_statement.order_by(CustomFieldConfig.name.desc())
        else:
            select_statement = select_statement.order_by(CustomFieldConfig.name.asc())
    if paginate:
        select_statement = select_statement.offset((page - 1) * page_size).limit(
            page_size
        )
    result = db.execute(select_statement).scalars().unique().all()
    return result


def get_cf_config_by_relation_id_count(
    db: Session,
    tenant_id: str,
    relation_id: str,
    relation_type: str,
    is_active: bool,
) -> int:
    select_statement = select(func.count()).select_from(CustomFieldConfig)
    select_statement = (
        select_statement.join(CustomFieldEntityRelation)
        .where(CustomFieldEntityRelation.cf_config_id == CustomFieldConfig.id)
        .where(CustomFieldEntityRelation.tenant_id == tenant_id)
        .where(CustomFieldEntityRelation.relation_id == relation_id)
        .where(CustomFieldEntityRelation.relation_type == relation_type)
    )

    if is_active:
        select_statement = select_statement.where(CustomFieldConfig.is_active is True)
    result = db.execute(select_statement).scalar()
    return result


def get_cf_config_by_entity_type(
    db: Session,
    tenant_id: str,
    entity_type: str,
    is_active: bool,
    sort_by: CFConfigServiceConts.SortByParams = CFConfigServiceConts.SortByParams.created_at,
    order: CFConfigServiceConts.Order = CFConfigServiceConts.Order.asc,
    paginate: bool = True,
    page: int = 1,
    page_size: int = 10,
) -> Select:
    select_statement = (
        select(CustomFieldConfig)
        .where(CustomFieldConfig.tenant_id == tenant_id)
        .where(CustomFieldConfig.entity_type == entity_type)
    )
    if is_active:
        select_statement = select_statement.where(CustomFieldConfig.is_active is True)
    if sort_by == CFConfigServiceConts.SortByParams.created_at:
        if order == CFConfigServiceConts.Order.desc:
            select_statement = select_statement.order_by(
                CustomFieldConfig.created_at.desc()
            )
        else:
            select_statement = select_statement.order_by(
                CustomFieldConfig.created_at.asc()
            )
    elif sort_by == CFConfigServiceConts.SortByParams.alpha:
        if order == CFConfigServiceConts.Order.desc:
            select_statement = select_statement.order_by(CustomFieldConfig.name.desc())
        else:
            select_statement = select_statement.order_by(CustomFieldConfig.name.asc())

    if paginate:
        select_statement = select_statement.offset((page - 1) * page_size).limit(
            page_size
        )

    result = db.execute(select_statement).scalars().unique().all()
    return result


def get_cf_config_by_entity_type_count(
    db: Session,
    tenant_id: str,
    entity_type: str,
    is_active: bool,
) -> int:
    select_statement = (
        select(func.count())
        .select_from(CustomFieldConfig)
        .where(CustomFieldConfig.tenant_id == tenant_id)
        .where(CustomFieldConfig.entity_type == entity_type)
    )
    if is_active:
        select_statement = select_statement.where(CustomFieldConfig.is_active is True)
    result = db.execute(select_statement).scalar()
    return result


def create_cf_config(
    db: Session, cf_config_data: CustomFieldsConfigCreate
) -> CustomFieldConfig:
    create_stmt = insert(CustomFieldConfig).values(**cf_config_data.dict())
    validate_name(
        db, cf_config_data.tenant_id, cf_config_data.name, cf_config_data.entity_type
    )
    try:
        db.execute(create_stmt)
        db.commit()
    except Exception as exe:
        raise exe

    return get_cf_config_by_id(db, cf_config_data.tenant_id, cf_config_data.id)


def patch_cf_config(
    db: Session,
    tenant_id: str,
    cf_config: CustomFieldConfig,
    cf_config_data: CustomFieldsConfigCreate,
) -> CustomFieldConfig:

    if (
        hasattr(cf_config_data, "name")
        and cf_config_data.name is not None
        and cf_config.name != cf_config_data.name
    ):
        validate_name(db, tenant_id, cf_config_data.name, cf_config_data.entity_type)

    update_statement = (
        update(CustomFieldConfig)
        .where(CustomFieldConfig.id == cf_config.id)
        .where(CustomFieldConfig.tenant_id == tenant_id)
        .values(**cf_config_data.dict(exclude_unset=True))
    )

    try:
        db.execute(update_statement)
        db.commit()
    except Exception as exe:
        raise exe

    db.refresh(cf_config)
    return cf_config


def validate_name(db: Session, tenant_id: UUID4, name: str, entity_type: str) -> None:
    select_stmt = (
        select(exists(CustomFieldConfig))
        .where(CustomFieldConfig.tenant_id == tenant_id)
        .where(CustomFieldConfig.entity_type == entity_type)
        .where(CustomFieldConfig.name == name)
    )
    if db.execute(select_stmt).scalar():
        raise DuplicateNameException("Custom Field with same name already exists")
