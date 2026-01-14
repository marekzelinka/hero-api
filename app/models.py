import uuid

from sqlmodel import Field, MetaData, Relationship, SQLModel

sqlite_naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

SQLModel.metadata = MetaData(naming_convention=sqlite_naming_convention)


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    heroes: list[Hero] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: uuid.UUID


class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroMissionLink(SQLModel, table=True):
    hero_id: uuid.UUID | None = Field(
        default=None, foreign_key="hero.id", primary_key=True
    )
    mission_id: uuid.UUID | None = Field(
        default=None, foreign_key="mission.id", primary_key=True
    )


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: uuid.UUID | None = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    team: Team | None = Relationship(
        back_populates="heroes",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    missions: list[Mission] = Relationship(
        back_populates="heroes",
        link_model=HeroMissionLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class HeroCreate(HeroBase):
    pass


class HeroPublic(HeroBase):
    id: uuid.UUID


class HeroPublicWithTeamMissions(HeroPublic):
    team: TeamPublic | None = None
    missions: list[MissionPublic] = []


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

    team_id: uuid.UUID | None = None


class MissionBase(SQLModel):
    description: str
    active: bool = Field(default=True)


class Mission(MissionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    heroes: list[Hero] = Relationship(
        back_populates="missions",
        link_model=HeroMissionLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class MissionCreate(MissionBase):
    pass


class MissionPublic(MissionBase):
    id: uuid.UUID


class MissionPublicWithHeroes(MissionPublic):
    heroes: list[HeroPublic] = []


class MissionUpdate(SQLModel):
    description: str | None = None
    active: bool | None = None


class Message(SQLModel):
    """Models a generic messages, used as a response model in routes."""

    message: str
