from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db.session import create_db_and_tables
from .routes import heroes, missions, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(teams.router)
app.include_router(heroes.router)
app.include_router(missions.router)
