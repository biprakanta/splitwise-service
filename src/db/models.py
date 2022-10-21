from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSON, UUID

from ..utils.consts import EntityTypeChoices, FieldTypeChoices, RelationTypeChoices
from .database import Base


class CustomFieldConfig(Base):
    __tablename__ = "custom_field_config"

    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid4
    )
    entity_type = Column(
        Enum(EntityTypeChoices),
        nullable=False,
        default=EntityTypeChoices.asset,
        index=True,
    )
    name = Column(Text, nullable=True)
    reference_id = Column(Text, nullable=True)
    field_type = Column(
        Enum(FieldTypeChoices), nullable=False, default=FieldTypeChoices.text
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    created_by = Column(UUID(as_uuid=True), nullable=False, index=True)

    last_updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
    )
    last_updated_by = Column(UUID(as_uuid=True), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint(
            "name", "entity_type", "tenant_id", name="unique_ids_custom_field_config"
        ),
    )


class CustomFieldValue(Base):
    __tablename__ = "custom_field_value"

    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid4
    )

    cf_config_id = Column(
        UUID(as_uuid=True),
        ForeignKey("custom_field_config.id"),
        index=True,
        nullable=False,
    )

    entity_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    field_value = Column(JSON, nullable=True)

    display_value = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    created_by = Column(UUID(as_uuid=True), nullable=False, index=True)

    last_updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
    )
    last_updated_by = Column(UUID(as_uuid=True), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint(
            "cf_config_id", "entity_id", name="unique_ids_custom_field_value"
        ),
    )


class CustomFieldEntityRelation(Base):
    __tablename__ = "custom_field_entity_relation"

    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False, primary_key=True)

    relation_id = Column(
        UUID(as_uuid=True), index=True, nullable=False, primary_key=True
    )

    cf_config_id = Column(
        UUID(as_uuid=True),
        ForeignKey("custom_field_config.id"),
        index=True,
        nullable=False,
        primary_key=True,
    )

    relation_type = Column(
        Enum(RelationTypeChoices),
        nullable=False,
        default=RelationTypeChoices.asset_type,
        primary_key=True,
    )
