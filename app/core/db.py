from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.sqlalchemy_database_uri,
    connect_args={"check_same_thread": False},
    echo=settings.environment == "local",
)
