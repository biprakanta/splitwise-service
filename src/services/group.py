from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ..config import get_settings
from ..data.database import get_db
from ..data.db_interactions import (
    create_group,
    get_group_by_id,
    update_group
)
from ..data.schema import (
    GroupData
)
from ..utils.consts import MetaServiceConsts
from ..utils.exceptions import DoesNotExist
from ..utils.custom_logger import CustomizeLogger

settings = get_settings()
LOGGER = CustomizeLogger.make_logger(settings)


router = APIRouter(
    prefix="",
    tags=["group"],
    responses={404: {MetaServiceConsts.DESCRIPTION: "Not found"}},
)


@router.get("/group/{group_id}")
async def get_group(
    group_id: str = Path(..., title="ID of group"),
    db: Session = Depends(get_db)
):

    group = get_group_by_id(db, group_id)
    if group:
        return GroupData.from_orm(group)
    raise DoesNotExist("Group with id {} does not exist".format(group_id))
    


@router.post("/group")
async def start_group(
    group_data: GroupData,
    db: Session = Depends(get_db)
):

    group = create_group(db, group_data)
    return group if group else {}


@router.patch("/group/{group_id}")
async def update_group_users( 
    group_data: GroupData,
    db: Session = Depends(get_db),
    group_id: str = Path(..., title="ID of group")
):

    group = update_group(db, group_id, group_data)
    if group:
        return group
    raise DoesNotExist("Group with id {} does not exist".format(group_id))