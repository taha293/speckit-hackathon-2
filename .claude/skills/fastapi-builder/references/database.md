# FastAPI Database Integration

## SQLModel Setup

### Database Engine Configuration
```python
from sqlmodel import create_engine, SQLModel
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.pool import QueuePool
import os

# SQLite Configuration
def create_sqlite_engine():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}  # Required for SQLite with threading
    return create_engine(sqlite_url, connect_args=connect_args)

# PostgreSQL Configuration
def create_postgresql_engine():
    postgres_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    engine = create_engine(
        postgres_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
    )
    return engine

# MySQL Configuration
def create_mysql_engine():
    mysql_url = os.getenv("MYSQL_DATABASE_URL", "mysql+pymysql://user:password@localhost/dbname")
    engine = create_engine(
        mysql_url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,   # Recycle connections every hour
    )
    return engine
```

### Database Initialization
```python
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI

def create_db_and_tables(engine):
    """Create all database tables defined in SQLModel models."""
    SQLModel.metadata.create_all(engine)

# Using lifespan to initialize database
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables(engine)
    yield

app = FastAPI(lifespan=lifespan)
```

## Session Management

### Session Dependency Pattern
```python
from sqlmodel import Session
from contextlib import contextmanager
from typing import Generator

def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session

# Alternative using context manager
@contextmanager
def get_session_context():
    """Context manager for database session."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Annotated dependency for type hints
from typing import Annotated
from fastapi import Depends

SessionDep = Annotated[Session, Depends(get_session)]
```

### Async Session Management (for asyncio support)
```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async_engine = create_async_engine(os.getenv("ASYNC_DATABASE_URL"))

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
```

## Connection Pooling

### Advanced Pool Configuration
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

def create_optimized_engine():
    """Create an engine with optimized connection pooling."""
    return create_engine(
        "postgresql://user:pass@localhost/db",
        poolclass=QueuePool,
        pool_size=20,           # Number of connections to maintain
        max_overflow=30,        # Additional connections beyond pool_size
        pool_pre_ping=True,     # Verify connections before use
        pool_recycle=3600,      # Recycle connections after 1 hour
        pool_timeout=30,        # Timeout for getting connection from pool
        echo=False,             # Set to True for SQL logging
        connect_args={
            "connect_timeout": 10,
            "application_name": "fastapi_app"
        }
    )
```

## Transaction Management

### Manual Transaction Control
```python
from fastapi import HTTPException
from sqlmodel import Session

def create_user_with_profile(session: Session, user_data: UserCreate, profile_data: ProfileCreate):
    """Create user and profile in a single transaction."""
    try:
        # Create user
        user = User(**user_data.dict())
        session.add(user)
        session.flush()  # Get ID without committing

        # Create profile
        profile = Profile(user_id=user.id, **profile_data.dict())
        session.add(profile)

        # Commit both operations
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")
```

### Nested Session Pattern
```python
def get_nested_session(parent_session: Session):
    """Create a nested session for complex operations."""
    trans = parent_session.begin_nested()
    try:
        yield parent_session
        trans.commit()
    except Exception:
        trans.rollback()
        raise
```

## Database Relationships

### One-to-Many Relationships
```python
from sqlmodel import Relationship

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

### Many-to-Many Relationships
```python
# Association table for many-to-many relationship
class HeroTeamLink(SQLModel, table=True):
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    is_training: bool = False  # Additional relationship data

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str

    teams: List["Team"] = Relationship(
        back_populates="heroes",
        link_model=HeroTeamLink
    )

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    heroes: List["Hero"] = Relationship(
        back_populates="teams",
        link_model=HeroTeamLink
    )
```

## Query Optimization

### Eager Loading
```python
from sqlalchemy.orm import selectinload

@app.get("/heroes-with-team/{hero_id}")
def get_hero_with_team(hero_id: int, session: SessionDep):
    """Get hero with team data in single query."""
    hero = session.exec(
        select(Hero)
        .options(selectinload(Hero.team))
        .where(Hero.id == hero_id)
    ).first()
    return hero

@app.get("/teams-with-heroes")
def get_teams_with_heroes(session: SessionDep):
    """Get teams with all heroes in single query."""
    teams = session.exec(
        select(Team)
        .options(selectinload(Team.heroes))
    ).all()
    return teams
```

### Pagination and Limits
```python
from fastapi import Query

@app.get("/heroes/")
def get_heroes_paginated(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    name_filter: Optional[str] = None
):
    """Get paginated list of heroes with optional filtering."""
    query = select(Hero)

    if name_filter:
        query = query.where(Hero.name.contains(name_filter))

    # Get total count for pagination metadata
    total = session.exec(select(func.count(Hero.id))).one()

    # Get paginated results
    heroes = session.exec(query.offset(skip).limit(limit)).all()

    return {
        "data": heroes,
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

## Raw SQL Queries

### Using Raw SQL When Needed
```python
from sqlalchemy import text

def get_hero_statistics(session: Session):
    """Get complex statistics using raw SQL."""
    result = session.execute(text("""
        SELECT
            t.name as team_name,
            COUNT(h.id) as hero_count,
            AVG(h.age) as avg_age
        FROM team t
        LEFT JOIN hero h ON t.id = h.team_id
        GROUP BY t.id, t.name
        ORDER BY hero_count DESC
    """)).fetchall()

    return [
        {"team_name": row[0], "hero_count": row[1], "avg_age": row[2]}
        for row in result
    ]
```

## Database Migration Strategies

### Alembic Integration
```python
# alembic/env.py for FastAPI integration
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# Import all models for Alembic to detect
from app.models import *  # Import all your models

config = context.config
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Database Seeding
```python
def seed_database(session: Session):
    """Seed the database with initial data."""
    # Check if already seeded
    existing_heroes = session.exec(select(Hero)).first()
    if existing_heroes:
        print("Database already seeded")
        return

    # Create seed data
    team1 = Team(name="Avengers", headquarters="Stark Tower")
    team2 = Team(name="Justice League", headquarters="Metropolis")

    session.add(team1)
    session.add(team2)
    session.commit()

    # Create heroes
    heroes = [
        Hero(name="Spider-Man", secret_name="Peter Parker", age=21, team_id=team1.id),
        Hero(name="Iron Man", secret_name="Tony Stark", age=48, team_id=team1.id),
        Hero(name="Superman", secret_name="Clark Kent", age=35, team_id=team2.id),
    ]

    for hero in heroes:
        session.add(hero)

    session.commit()
    print("Database seeded successfully")
```

## Error Handling

### Database-Specific Error Handling
```python
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException

def create_unique_hero(session: Session, hero_data: HeroCreate):
    """Create hero with proper error handling."""
    try:
        hero = Hero(**hero_data.dict())
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Hero with this name already exists"
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred: {str(e)}"
        )

def get_hero_by_id(session: Session, hero_id: int):
    """Get hero by ID with proper error handling."""
    try:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(
                status_code=404,
                detail="Hero not found"
            )
        return hero
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="Hero not found"
        )
```

## Performance Monitoring

### Query Timing and Logging
```python
import time
from functools import wraps

def timed_query(func):
    """Decorator to time database queries."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        query_time = end_time - start_time
        if query_time > 1.0:  # Log slow queries (> 1 second)
            print(f"SLOW QUERY ({query_time:.2f}s): {func.__name__}")

        return result
    return wrapper

@timed_query
def get_complex_report(session: Session):
    """Example of a complex query that benefits from timing."""
    # Complex query here
    pass
```

## Testing Database Integration

### Database Tests
```python
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session

# Create test database engine
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def override_get_session(test_engine):
    def _get_session():
        with Session(test_engine) as session:
            yield session
    app.dependency_overrides[get_session] = _get_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client(override_get_session):
    with TestClient(app) as c:
        yield c

def test_create_hero(client: TestClient):
    """Test creating a hero in the database."""
    response = client.post("/heroes/", json={
        "name": "Test Hero",
        "secret_name": "Secret Identity",
        "age": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Hero"

    # Verify it was actually saved to database
    get_response = client.get(f"/heroes/{data['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Hero"
```