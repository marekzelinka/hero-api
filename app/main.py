from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.session import create_db_and_tables
from .routes import heroes, missions, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type] Typing problem, still works, ignore for now,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teams.router)
app.include_router(heroes.router)
app.include_router(missions.router)
