from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from ..config import get_settings
from ..data.database import get_db
from ..data.db_interactions import (
    insert_expense,
    get_expense_by_user_id
)
from ..data.schema import (
    ExpenseCreate
)
from ..utils.consts import MetaServiceConsts
from ..utils.exceptions import DoesNotExist
from ..utils.custom_logger import CustomizeLogger

settings = get_settings()
LOGGER = CustomizeLogger.make_logger(settings)


router = APIRouter(
    prefix="",
    tags=["expense"],
    responses={404: {MetaServiceConsts.DESCRIPTION: "Not found"}},
)


@router.post("/expense/{group_id}")
async def add_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    group_id: str = Path(..., title="ID of group")
):
    expense_data.group_id = group_id
    expense = insert_expense(db, expense_data)
    return expense if expense else {}



@router.get("/expense/{user_id}")
async def list_expenses(
    expense_data,
    db: Session = Depends(get_db),
    user_id: str = Path(..., title="ID of user")
):
    pass

