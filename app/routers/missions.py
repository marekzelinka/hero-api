from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, status

from app.db.schema import (
    Hero,
    HeroMissionLink,
    Mission,
    MissionCreate,
    MissionPublic,
    MissionPublicWithHeroes,
    MissionUpdate,
)
from app.db.session import SessionDep

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=MissionPublic, status_code=status.HTTP_201_CREATED)
def create_mission(
    *,
    mission: Annotated[MissionCreate, Body()],
    session: SessionDep,
):
    db_mission = Mission.model_validate(mission)
    session.add(db_mission)
    session.commit()
    session.refresh(db_mission)
    return db_mission


@router.get("/{mission_id}", response_model=MissionPublicWithHeroes)
def read_mission(
    *,
    mission_id: Annotated[int, Path()],
    session: SessionDep,
):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
        )
    return mission


@router.put("/{mission_id}/heroes/{hero_id}", response_model=MissionPublicWithHeroes)
def assign_hero_to_mission(
    *,
    mission_id: Annotated[int, Path()],
    hero_id: Annotated[int, Path()],
    session: SessionDep,
):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
        )
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    if hero in mission.heroes:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="Hero already assigned to mission",
        )
    hero_mission_link = HeroMissionLink(hero_id=hero_id, mission_id=mission_id)
    session.add(hero_mission_link)
    session.commit()
    return mission


@router.patch("/{mission_id}", response_model=MissionPublic)
async def update_mission(
    *,
    mission_id: Annotated[int, Path()],
    mission: Annotated[MissionUpdate, Body()],
    session: SessionDep,
):
    db_mission = session.get(Mission, mission_id)
    if not db_mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="mission not found"
        )
    mission_data = mission.model_dump(exclude_unset=True)
    db_mission.sqlmodel_update(mission_data)
    session.add(db_mission)
    session.commit()
    session.refresh(db_mission)
    return db_mission
