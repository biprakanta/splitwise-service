from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import get_settings

settings = get_settings()

# Postgres connection string guide:
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
userspec = f"{quote(settings.postgres_user)}:{quote(settings.postgres_password)}@"
hostspec = f"{quote(settings.postgres_host)}:{settings.postgres_port}"
dbname = f"/{settings.postgres_db}"
paramspec = f"?sslmode={settings.postgres_sslmode}"
DATABASE_URL = f"postgresql://{userspec}{hostspec}{dbname}{paramspec}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, future=True, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
