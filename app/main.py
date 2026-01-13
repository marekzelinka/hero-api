import logging
from contextlib import asynccontextmanager
from typing import Any, TypedDict

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import config
from app.core.db import create_db_and_tables
from app.deps import SessionDep
from app.routers import heroes, missions, teams

logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Hero API", lifespan=lifespan)

# Set all CORS enabled origins
if config.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,  # ty:ignore[invalid-argument-type]
        allow_origins=config.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(teams.router)
app.include_router(heroes.router)
app.include_router(missions.router)


@app.get(
    "/health",
    tags=["status"],
    summary="Perform a Health Check",
    status_code=status.HTTP_200_OK,
    response_model=TypedDict("Health", {"status": str}),
)
async def read_health(*, _session: SessionDep) -> Any:
    return {"status": "ok"}
