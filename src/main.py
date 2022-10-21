from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .services import expense, group, settlement, user, meta
from .utils.custom_logger import CustomizeLogger

settings = get_settings()
logger = CustomizeLogger.make_logger(settings)



app = FastAPI()
app.logger = logger

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(meta.router)
app.include_router(expense.router)
app.include_router(group.router)
app.include_router(settlement.router)
app.include_router(user.router)
