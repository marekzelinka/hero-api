from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path

from app.db.schema import Team
from app.db.session import SessionDep

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=Team)
def create_team(session: SessionDep, team: Annotated[Team, Body()]):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.get("/{team_id}", response_model=Team)
def read_team(session: SessionDep, team_id: Annotated[int, Path()]):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
