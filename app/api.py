from fastapi import APIRouter

from app.routers import heroes, missions, teams

api_router = APIRouter(prefix="/api")
api_router.include_router(teams.router)
api_router.include_router(heroes.router)
api_router.include_router(missions.router)
