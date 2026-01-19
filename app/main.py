from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import config
from app.deps import SessionDep
from app.models import HealthCheck

app = FastAPI(
    title="Hero API",
    summary="A high-performance API for managing superheros.",
    version="1.0.0",
)


# Set all CORS enabled origins
if config.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,  # ty:ignore[invalid-argument-type]
        allow_origins=config.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router)


@app.get(
    "/health",
    tags=["status"],
    summary="Perform a Health Check",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def read_health(*, _session: SessionDep) -> HealthCheck:
    return HealthCheck(status="ok")
