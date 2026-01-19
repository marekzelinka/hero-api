from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import config

engine = create_async_engine(
    config.database_url,
    connect_args={"check_same_thread": False},
    echo=True,
)
