"""
Test Setup for SQLModel Project
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch

from main import app
from database.engine import engine
from models.hero import Hero


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with overridden dependencies."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_hero(client: TestClient):
    """Test creating a hero."""
    response = client.post(
        "/api/v1/heroes/",
        json={"name": "Deadpond", "description": "Nice guy"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["description"] == "Nice guy"
    assert data["id"] is not None


def test_read_heroes(session: Session, client: TestClient):
    """Test reading multiple heroes."""
    hero_1 = Hero(name="Deadpond", description="Nice guy")
    hero_2 = Hero(name="Rusty-Man", description="Old hero")
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/api/v1/heroes/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert data[1]["name"] == hero_2.name


def test_read_hero(session: Session, client: TestClient):
    """Test reading a single hero."""
    hero = Hero(name="Deadpond", description="Nice guy")
    session.add(hero)
    session.commit()

    response = client.get(f"/api/v1/heroes/{hero.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero.name
    assert data["description"] == hero.description


def test_update_hero(session: Session, client: TestClient):
    """Test updating a hero."""
    hero = Hero(name="Deadpond", description="Nice guy")
    session.add(hero)
    session.commit()

    response = client.patch(
        f"/api/v1/heroes/{hero.id}",
        json={"name": "Dragonfly", "description": "Changed name"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Dragonfly"
    assert data["description"] == "Changed name"


def test_delete_hero(session: Session, client: TestClient):
    """Test deleting a hero."""
    hero = Hero(name="Deadpond", description="Nice guy")
    session.add(hero)
    session.commit()

    response = client.delete(f"/api/v1/heroes/{hero.id}")

    hero_in_db = session.get(Hero, hero.id)

    assert response.status_code == 200
    assert hero_in_db is None