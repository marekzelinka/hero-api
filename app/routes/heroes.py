from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query
from sqlmodel import select

from app.db.schema import Hero, Team
from app.db.session import SessionDep

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post("/", response_model=Hero)
def create_hero(
    session: SessionDep,
    hero: Annotated[Hero, Body()],
):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/", response_model=list[Hero])
def read_heroes(
    session: SessionDep,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    heroes = session.exec(select(Hero).offset(skip).limit(limit)).all()
    return heroes


@router.get("/{hero_id}", response_model=Hero)
def read_hero(session: SessionDep, hero_id: Annotated[int, Path()]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.put("/{hero_id}", response_model=Hero)
def update_hero(
    session: SessionDep,
    hero_id: Annotated[int, Path()],
    hero_data: Annotated[Hero, Body()],
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    for field, value in hero_data.model_dump().items():
        setattr(hero, field, value)
    session.commit()
    session.refresh(hero)
    return hero


@router.put("/{hero_id}/team/{team_id}")
def assign_hero_to_team(
    session: SessionDep,
    hero_id: Annotated[int, Path()],
    team_id: Annotated[int, Path()],
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    hero.team_id = team_id
    session.commit()
    session.refresh(hero)
    return hero


@router.delete("/{hero_id}", response_model=Hero)
def delete_hero(session: SessionDep, hero_id: Annotated[int, Path()]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return hero
