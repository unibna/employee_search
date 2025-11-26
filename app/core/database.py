from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from sqlalchemy import event

from app.core.config import settings
from app.models import *


connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False,
        "timeout": 30.0,  # Increase timeout for long operations
    }

engine = create_engine(
    settings.database_url,
    echo=True,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connections before using
)


# Enable WAL mode for SQLite (better concurrency)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    if settings.database_url.startswith("sqlite"):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

