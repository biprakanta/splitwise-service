import os
from functools import lru_cache
from typing import Dict, List, Tuple, Union

import environ
from pydantic import BaseSettings

from .utils.buildinfo import get_build_info

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = environ.Env()
ENV.read_env(os.path.join(BASE_DIR, ".env"))

release = get_build_info()


class Settings(BaseSettings):
    postgres_host: str = ENV.str("POSTGRES_HOST")
    postgres_port: str = ENV.str("POSTGRES_PORT")
    postgres_db: str = ENV.str("POSTGRES_DB")
    postgres_user: str = ENV.str("POSTGRES_USER")
    postgres_password: str = ENV.str("POSTGRES_PASSWORD")
    postgres_sslmode: str = ENV.str("POSTGRES_SSLMODE")

    logger_level: str = ENV("LOGGER_LEVEL")
    logger_path: str = ENV("LOGGER_PATH")
    logger_rotation: str = ENV("LOGGER_ROTATION")
    logger_retention: str = ENV("LOGGER_RETENTION")
    logger_format: str = ENV("LOGGER_FORMAT")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
