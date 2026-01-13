from typing import Annotated, Any

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlmodel import select

from app.deps import SessionDep
from app.models import Team, TeamCreate, TeamPublic, TeamPublicWithHeroes, TeamUpdate

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TeamPublic,
)
async def create_team(
    *,
    session: SessionDep,
    team: Annotated[TeamCreate, Body()],
) -> Any:
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/", response_model=list[TeamPublic])
async def read_teams(
    *,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0)] = 100,
    session: SessionDep,
) -> Any:
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/{team_id}", response_model=TeamPublicWithHeroes)
async def read_team(
    *,
    session: SessionDep,
    team_id: Annotated[int, Path()],
) -> Any:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@router.patch("/{team_id}", response_model=TeamPublic)
async def update_team(
    *,
    session: SessionDep,
    team_id: Annotated[int, Path()],
    team: Annotated[TeamUpdate, Body()],
) -> Any:
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
async def delete_team(
    *,
    session: SessionDep,
    team_id: Annotated[int, Path()],
) -> None:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    session.delete(team)
    session.commit()
    return None
