from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config import get_settings, release
from ..data.database import get_db
from ..data.db_interactions import (
    create_user,
    get_user_by_mobile
)
from ..data.schema import (
    UserData
)
from ..utils.consts import MetaServiceConsts
from ..utils.exceptions import DoesNotExist
from ..utils.custom_logger import CustomizeLogger

settings = get_settings()
LOGGER = CustomizeLogger.make_logger(settings)


router = APIRouter(
    prefix="",
    tags=["user"],
    responses={404: {MetaServiceConsts.DESCRIPTION: "Not found"}},
)


@router.post("/register")
async def register(
    user_data: UserData,
    db: Session = Depends(get_db)
):

    user = create_user(db, user_data)
    return UserData.from_orm(user) if user else {}


@router.get("/user")
async def get_user(
    mobile: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_mobile(db, mobile)
    if user:
        return UserData.from_orm(user)
    raise DoesNotExist("User with mobile {} does not exist".format(mobile))
    


