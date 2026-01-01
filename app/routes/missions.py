from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path

from app.db.schema import Hero, HeroMissionLink, Mission
from app.db.session import SessionDep

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=Mission)
def create_mission(session: SessionDep, mission: Annotated[Mission, Body()]):
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@router.put("/{mission_id}/heroes/{hero_id}", response_model=Mission)
def assign_hero_to_mission(
    session: SessionDep,
    mission_id: Annotated[int, Path()],
    hero_id: Annotated[int, Path()],
):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_mission_link = HeroMissionLink(hero_id=hero_id, mission_id=mission_id)
    session.add(hero_mission_link)
    session.commit()
    return mission


@router.get("/{mission_id}", response_model=Mission)
def read_mission(session: SessionDep, mission_id: Annotated[int, Path()]):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission
