from typing import Annotated, Any

from fastapi import APIRouter, Body, HTTPException, Path, status

from app.deps import SessionDep
from app.models import (
    Hero,
    HeroMissionLink,
    Mission,
    MissionCreate,
    MissionPublic,
    MissionPublicWithHeroes,
    MissionUpdate,
)

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MissionPublic)
async def create_mission(
    *,
    session: SessionDep,
    mission: Annotated[MissionCreate, Body()],
) -> Any:
    db_mission = Mission.model_validate(mission)
    session.add(db_mission)
    session.commit()
    session.refresh(db_mission)
    return db_mission


@router.get("/{mission_id}", response_model=MissionPublicWithHeroes)
async def read_mission(
    *,
    session: SessionDep,
    mission_id: Annotated[int, Path()],
) -> Any:
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
        )
    return mission


@router.put("/{mission_id}/heroes/{hero_id}", response_model=MissionPublicWithHeroes)
async def assign_hero_to_mission(
    *,
    session: SessionDep,
    mission_id: Annotated[int, Path()],
    hero_id: Annotated[int, Path()],
) -> Any:
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
    session: SessionDep,
    mission_id: Annotated[int, Path()],
    mission: Annotated[MissionUpdate, Body()],
) -> Any:
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


@router.delete("/{mission_id}/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_hero_from_mission(
    *,
    session: SessionDep,
    mission_id: Annotated[int, Path()],
    hero_id: Annotated[int, Path()],
) -> None:
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
        )
    elif not mission.active:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="Can't remove hero from inactive mission",
        )
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    hero_mission_link = session.get(
        HeroMissionLink,
        (
            hero_id,
            mission_id,
        ),
    )
    if not hero_mission_link:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="Hero wasn't assigned to mission",
        )
    session.delete(hero_mission_link)
    session.commit()
    return None
