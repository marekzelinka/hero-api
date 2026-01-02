from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlmodel import select

from app.db.schema import Team, TeamCreate, TeamPublic, TeamUpdate
from app.db.session import SessionDep

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=TeamPublic, status_code=status.HTTP_201_CREATED)
def create_team(
    *,
    team: Annotated[TeamCreate, Body()],
    session: SessionDep,
):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/", response_model=list[TeamPublic])
async def read_teams(
    *,
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    session: SessionDep,
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/{team_id}", response_model=TeamPublic)
def read_team(
    *,
    team_id: Annotated[int, Path()],
    session: SessionDep,
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@router.patch("/{team_id}", response_model=TeamPublic)
async def update_team(
    *,
    team_id: Annotated[int, Path()],
    team: Annotated[TeamUpdate, Body()],
    session: SessionDep,
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    team_data = team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(*, team_id: Annotated[int, Path()], session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    session.delete(team)
    session.commit()
