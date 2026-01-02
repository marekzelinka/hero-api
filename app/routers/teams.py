from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, status

from app.db.schema import Team
from app.db.session import SessionDep

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(
    *,
    team: Annotated[Team, Body()],
    session: SessionDep,
):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.get("/{team_id}", response_model=Team)
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
