# pylint: disable=relative-beyond-top-level
from sqlalchemy import func, insert, select, update
from sqlalchemy.sql.expression import case
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import exists
from sqlalchemy.sql.selectable import Select


from ..utils.consts import *
from ..utils.exceptions import DuplicateMobileException, DoesNotExist
from .models import User, Group, UserGroupMapping, Expense, ExpenseUserMapping
from .schema import UserData, GroupData, ExpenseCreate, ExpenseHistory


def get_user_by_mobile(db: Session, mobile: int) -> Select:
    select_statement = (
        select(User)
        .where(User.mobile == mobile)
    )
    result = db.execute(select_statement).scalar()
    return result


def create_user(db: Session, user_data: UserData) -> User:
    validate_mobile(
        db, user_data.mobile
    )
    create_stmt = insert(User).values(**user_data.dict(exclude_none=True))
    
    try:
        db.execute(create_stmt)
        #db.commit()
        get_expense_by_user_id(db, user_data.id)
    except Exception as exe:
        raise exe

    return get_user_by_mobile(db, user_data.mobile)


def validate_mobile(db: Session, mobile: int) -> None:
    select_stmt = (
        select(exists(User))
        .where(User.mobile == mobile)
    )
    if db.execute(select_stmt).scalar():
        raise DuplicateMobileException("Custom Field with same name already exists")


def create_group(db: Session, group_data: GroupData) -> GroupData:
    # TODO: after auth enabling create group with creator by getting identity from auth
    create_stmt = insert(Group).values(**group_data.dict(exclude_none=True))
    
    try:
        db.execute(create_stmt)
        db.commit()
    except Exception as exe:
        raise exe

    return get_group_by_id(db, group_data.id)

def get_group_by_id(db: Session, group_id: str) -> Select:
    select_statement = (
        select(UserGroupMapping, Group, User)
        .join(Group).join(User)
        .where(Group.id == group_id)
    )
    alt_select_statement = (
        select(Group)
        .where(Group.id == group_id)
    )


    result = db.execute(select_statement).all()
    if result:
        user_list = [UserData.from_orm(item[2]) for item in result]
        group_data = GroupData.from_orm(result[0][1])
        group_data.users = user_list
        return group_data
    else:
        print(alt_select_statement)
        print(db.execute(alt_select_statement).scalar())
        result = GroupData.from_orm(db.execute(alt_select_statement).scalar())
        result.users=[]
    return result

def update_group(db: Session, group_id: str, group_data: GroupData) -> GroupData:
    # TODO: Only allowing adding users to group
    mapping = []
    for user_id in group_data.users:
        assert(not isinstance(user_id, UserData))
        mapping.append(
            {
                "user_id": user_id,
                "group_id": group_id,
            }
        )
    
    group_data = group_data.dict(exclude_unset=True)
    group_data.pop("users")
    if group_data:
        update_statement = (
            update(Group)
            .where(Group.id == group_id)
            .values(**group_data)
        )
        db.execute(update_statement)
    try:
        db.bulk_insert_mappings(UserGroupMapping, mapping)
        db.commit()
        return get_group_by_id(db, group_id)
    except Exception as exe:
        if "user_group_mapping_user_id_fkey" in str(exe) or "user_group_mapping_group_id_fkey" in str(exe):
            raise Exception("Invalid UserId/GroupId")
        raise exe


def insert_expense(db: Session,  expense_data: ExpenseCreate) -> ExpenseCreate:
    mapping = []
    if expense_data.shares:
        for user_id, share in expense_data.shares.items():
            mapping.append(
                {
                    "user_id": user_id,
                    "amount": share,
                    "expense_id": expense_data.id
                }
            )
    else:
        group_data = get_group_by_id(db, expense_data.group_id)
        if group_data.users:
            share = expense_data.total_amount/(len(group_data.users))
            for user in group_data.users:
                mapping.append(
                {
                    "user_id": user.id,
                    "amount": share,
                    "expense_id": expense_data.id
                }
            )
    expense_data = expense_data.dict(exclude_none=True)
    expense_data.pop('shares')
    create_stmt = insert(Expense).values(**expense_data)
    try:
        db.execute(create_stmt)
        if mapping:
            db.bulk_insert_mappings(ExpenseUserMapping, mapping)
        db.commit()
        return expense_data
    except Exception as exe:
        if "expense_user_mapping_user_id_fkey" in str(exe) or "expense_user_mapping_expense_id_fkey" in str(exe):
            raise Exception("Invalid UserId/GroupId")
        raise exe

def get_expense_by_user_id(db: Session, user_id: str):
    select_stmt = (
        select(
            ExpenseUserMapping.amount,
            Expense.id, 
            Expense.title, 
            Expense.created_at,
            Expense.paid_by,
            Expense.total_amount,
            Group.id.label('group_id'),
            Group.name,
            case( [
                
                (Expense.paid_by == user_id, Expense.total_amount - ExpenseUserMapping.amount), 
                (Expense.paid_by != user_id, -1*ExpenseUserMapping.amount)
                ]
                ).label('pending')
        
        )
        .join(Expense, ExpenseUserMapping.expense_id == Expense.id)
        .join(Group, Group.id==Expense.group_id)
        .where(ExpenseUserMapping.user_id == user_id)
        
    )
    cursor = db.execute(select_stmt).scalars().all()
    results = []
    for result in cursor:
        results.append(ExpenseHistory.from_orm(result))
    return results


