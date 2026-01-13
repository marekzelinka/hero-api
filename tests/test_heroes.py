import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models import Hero


@pytest.mark.asyncio
async def test_create_hero(client: AsyncClient):
    r = await client.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
    )
    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_create_hero_incomplete(client: AsyncClient):
    # Falis validation because of missing secret_name in json
    r = await client.post("/heroes/", json={"name": "Deadpond"})
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_create_hero_invalid(client: AsyncClient):
    r = await client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_read_heroes(session: AsyncSession, client: AsyncClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    hero_2 = Hero(name="Rusty-Max", secret_name="Tommy Sharp", age=48)
    session.add(hero_2)
    await session.commit()
    await session.refresh(hero_1)
    await session.refresh(hero_2)

    r = await client.get("/heroes/")
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert len(data) == 2

    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["age"] is None
    assert data[0]["id"] == str(hero_1.id)
    assert data[0]["id"] is not None

    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["age"] is not None
    assert data[1]["id"] == str(hero_2.id)


@pytest.mark.asyncio
async def test_read_hero(session: AsyncSession, client: AsyncClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    await session.commit()
    await session.refresh(hero_1)

    r = await client.get(f"/heroes/{str(hero_1.id)}")
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == str(hero_1.id)


@pytest.mark.asyncio
async def test_update_hero(session: AsyncSession, client: AsyncClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    await session.commit()
    await session.refresh(hero_1)

    r = await client.patch(f"/heroes/{hero_1.id}", json={"name": "Deadpuddle"})
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["name"] == "Deadpuddle"
    assert data["age"] is None
    assert data["id"] == str(hero_1.id)


@pytest.mark.asyncio
async def test_delete_hero(session: AsyncSession, client: AsyncClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    await session.commit()
    await session.refresh(hero_1)

    r = await client.delete(f"/heroes/{hero_1.id}")
    assert r.status_code == status.HTTP_204_NO_CONTENT

    hero_in_db = await session.get(Hero, hero_1.id)
    assert hero_in_db is None
