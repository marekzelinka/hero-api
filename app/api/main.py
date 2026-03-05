from fastapi import APIRouter

from app.api.routers import heroes, missions, teams

api_router = APIRouter()
api_router.include_router(heroes.router)
api_router.include_router(missions.router)
api_router.include_router(teams.router)
