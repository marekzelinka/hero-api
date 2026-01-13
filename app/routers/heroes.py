import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlmodel import select

from app.deps import SessionDep
from app.models import (
    Hero,
    HeroCreate,
    HeroPublic,
    HeroPublicWithTeamMissions,
    HeroUpdate,
    Team,
)

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=HeroPublic,
)
async def create_hero(
    *,
    session: SessionDep,
    hero: Annotated[HeroCreate, Body()],
) -> Any:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/", response_model=list[HeroPublic])
async def read_heroes(
    *,
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0)] = 100,
) -> Any:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/{hero_id}", response_model=HeroPublicWithTeamMissions)
async def read_hero(
    *,
    session: SessionDep,
    hero_id: Annotated[uuid.UUID, Path()],
) -> Any:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    return hero


@router.patch("/{hero_id}", response_model=HeroPublic)
async def update_hero(
    *,
    session: SessionDep,
    hero_id: Annotated[uuid.UUID, Path()],
    hero: Annotated[HeroUpdate, Body()],
) -> Any:
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    hero_data = hero.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.put("/{hero_id}/team/{team_id}", response_model=HeroPublic)
async def assign_hero_to_team(
    *,
    hero_id: Annotated[uuid.UUID, Path()],
    team_id: Annotated[uuid.UUID, Path()],
    session: SessionDep,
) -> Any:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    hero.team_id = team_id
    session.commit()
    session.refresh(hero)
    return hero


@router.delete("/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(
    *,
    session: SessionDep,
    hero_id: Annotated[uuid.UUID, Path()],
) -> None:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    session.delete(hero)
    session.commit()
    return None
