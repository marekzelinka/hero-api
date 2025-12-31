from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class DBHero(Base):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(), index=True)
    secret_name: Mapped[str]
    age: Mapped[int | None]


class Hero(BaseModel):
    id: int | None = None
    name: str
    secret_name: str
    age: int | None = None


# Database setup
DATABASE_URL = "sqlite:///./db.sqlite3"
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Create a Hero
@app.post("/heroes/", response_model=Hero)
def create_hero(
    session: Annotated[Session, Depends(get_session)],
    hero: Annotated[Hero, Body()],
):
    db_hero = DBHero(**hero.model_dump())
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


# Read all heroes
@app.get("/heroes/", response_model=list[Hero])
def read_heroes(
    session: Annotated[Session, Depends(get_session)],
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    heroes = session.query(DBHero).offset(skip).limit(limit).all()
    return heroes


# Read a hero by ID
@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(
    session: Annotated[Session, Depends(get_session)], hero_id: Annotated[int, Path()]
):
    hero = session.query(DBHero).filter(DBHero.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


# Update a Hero
@app.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(
    session: Annotated[Session, Depends(get_session)],
    hero_id: Annotated[int, Path()],
    hero_data: Annotated[Hero, Body()],
):
    hero = session.query(DBHero).filter(DBHero.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    # Update the hero's attributes
    for field, value in hero_data.model_dump().items():
        setattr(hero, field, value)

    session.commit()
    session.refresh(hero)
    return hero


# Delete a Hero
@app.delete("/heroes/{hero_id}", response_model=Hero)
def delete_hero(
    session: Annotated[Session, Depends(get_session)], hero_id: Annotated[int, Path()]
):
    hero = session.query(DBHero).filter(DBHero.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return hero
