from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.db.schema import Hero


def test_create_hero(client: TestClient):
    r = client.post("/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"})
    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None


def test_create_hero_incomplete(client: TestClient):
    # Missing secret_name in json
    r = client.post("/heroes/", json={"name": "Deadpond"})
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_hero_invalid(client: TestClient):
    r = client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_heroes(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    hero_2 = Hero(name="Rusty-Max", secret_name="Tommy Sharp", age=48)
    session.add(hero_2)
    session.commit()

    r = client.get("/heroes/")
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert len(data) == 2

    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["age"] is None
    assert data[0]["id"] == hero_1.id
    assert data[0]["id"] is not None

    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["age"] is not None
    assert data[1]["id"] == hero_2.id


def test_read_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    r = client.get(f"/heroes/{hero_1.id}")
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == hero_1.id


def test_update_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    r = client.patch(f"/heroes/{hero_1.id}", json={"name": "Deadpuddle"})
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["name"] == "Deadpuddle"
    assert data["age"] is None
    assert data["id"] == hero_1.id


def test_delete_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    r = client.delete(f"/heroes/{hero_1.id}")
    assert r.status_code == status.HTTP_204_NO_CONTENT

    hero_in_db = session.get(Hero, hero_1.id)
    assert hero_in_db is None
