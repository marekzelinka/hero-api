from sqlmodel import create_engine

from app.core.config import config

engine = create_engine(config.database_url, connect_args={"check_same_thread": False})
