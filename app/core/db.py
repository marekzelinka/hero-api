from sqlmodel import SQLModel, create_engine

from app.core.config import config

engine = create_engine(config.database_url, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
