from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import DATABASE_URL

# Database setup
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


# Dependency
def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
