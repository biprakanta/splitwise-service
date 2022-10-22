from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings
from ..data.database import get_db
from ..data.db_interactions import (
    get_settlement_for_user_id,
    make_settlement_for_user_id,
)
from ..data.schema import SettlementRequest
from ..utils.consts import MetaServiceConsts
from ..utils.exceptions import DoesNotExist
from ..utils.custom_logger import CustomizeLogger


settings = get_settings()
LOGGER = CustomizeLogger.make_logger(settings)


router = APIRouter(
    prefix="",
    tags=["settlement"],
    responses={404: {MetaServiceConsts.DESCRIPTION: "Not found"}},
)


@router.put("/settlement/")
async def settle(
    settlement_data: SettlementRequest,
    db: Session = Depends(get_db),
):
    make_settlement_for_user_id(
        db,
        settlement_data.user_id,
        settlement_data.settle_with,
        settlement_data.group_id,
    )
    return {"msg": "Success"}


@router.get("/settlement")
async def get_settlement_amount(
    db: Session = Depends(get_db),
    user_id: str = Query(description="Id of User"),
    settle_with: str = Query(description="Id of User to Settle With"),
    group_id: str = Query(description="Id of Group"),
):
    return get_settlement_for_user_id(db, user_id, settle_with, group_id)
