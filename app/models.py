from sqlmodel import Field, Relationship, SQLModel


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list[Hero] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int


class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroMissionLink(SQLModel, table=True):
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    mission_id: int | None = Field(
        default=None, foreign_key="mission.id", primary_key=True
    )


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    team: Team | None = Relationship(back_populates="heroes")
    missions: list[Mission] = Relationship(
        back_populates="heroes", link_model=HeroMissionLink
    )


class HeroCreate(HeroBase):
    pass


class HeroPublic(HeroBase):
    id: int


class HeroPublicWithTeamMissions(HeroPublic):
    team: TeamPublic | None = None
    missions: list[MissionPublic] = []


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

    team_id: int | None = None


class MissionBase(SQLModel):
    description: str
    active: bool = Field(default=True)


class Mission(MissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list[Hero] = Relationship(
        back_populates="missions", link_model=HeroMissionLink
    )


class MissionCreate(MissionBase):
    pass


class MissionPublic(MissionBase):
    id: int


class MissionPublicWithHeroes(MissionPublic):
    heroes: list[HeroPublic] = []


class MissionUpdate(SQLModel):
    description: str | None = None
    active: bool | None = None


# Generic message
class Message(SQLModel):
    message: str
