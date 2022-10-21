from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings, release
from ..data.database import get_db
from ..utils.consts import MetaServiceConsts
from ..utils.custom_logger import CustomizeLogger

settings = get_settings()
LOGGER = CustomizeLogger.make_logger(settings)


router = APIRouter(
    prefix="",
    tags=["meta"],
    responses={404: {MetaServiceConsts.DESCRIPTION: "Not found"}},
)


@router.get("/buildinfo")
async def get_buildinfo(db: Session = Depends(get_db)):
    result = release
    health_check_meta = {
        MetaServiceConsts.DB: False,
    }
    try:
        db.scalar(select(1))
        health_check_meta[MetaServiceConsts.DB] = True
    except Exception as err:
        LOGGER.exception(err)
    result.update({MetaServiceConsts.HEALTH: health_check_meta})
    return result

