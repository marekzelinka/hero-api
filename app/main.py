from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.cors import setup_cors
from .core.logging import setup_logging
from .db.session import create_db_and_tables
from .routers import heroes, missions, teams

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

setup_cors(app)

app.include_router(teams.router)
app.include_router(heroes.router)
app.include_router(missions.router)
