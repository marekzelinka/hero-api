from sqlmodel import Field, Relationship, SQLModel


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    headsquarters: str

    heroes: list[Hero] = Relationship(back_populates="team")


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


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

    team_id: int | None = None


class Mission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    description: str

    heroes: list[Hero] = Relationship(
        back_populates="missions", link_model=HeroMissionLink
    )
