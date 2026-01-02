from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlmodel import select

from app.db.schema import (
    Hero,
    HeroCreate,
    HeroPublic,
    HeroPublicWithTeam,
    HeroUpdate,
    Team,
)
from app.db.session import SessionDep

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post("/", response_model=HeroPublic, status_code=status.HTTP_201_CREATED)
def create_hero(
    *,
    hero: Annotated[HeroCreate, Body()],
    session: SessionDep,
):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/", response_model=list[HeroPublic])
def read_heroes(
    *,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
    session: SessionDep,
):
    heroes = session.exec(select(Hero).offset(skip).limit(limit)).all()
    return heroes


@router.get("/{hero_id}", response_model=HeroPublicWithTeam)
def read_hero(
    *,
    hero_id: Annotated[int, Path()],
    session: SessionDep,
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    return hero


@router.patch("/{hero_id}", response_model=HeroPublic)
def update_hero(
    *,
    hero_id: Annotated[int, Path()],
    hero: Annotated[HeroUpdate, Body()],
    session: SessionDep,
):
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
def assign_hero_to_team(
    *,
    hero_id: Annotated[int, Path()],
    team_id: Annotated[int, Path()],
    session: SessionDep,
):
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
def delete_hero(
    *,
    hero_id: Annotated[int, Path()],
    session: SessionDep,
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    session.delete(hero)
    session.commit()
