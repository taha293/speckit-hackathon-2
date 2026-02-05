# SQLModel Patterns and Examples

## Core Model Patterns

### Basic Model Definition
```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100)
    headquarters: str = Field(max_length=100)

    # Relationship to heroes
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=50)
    secret_name: str = Field(max_length=50)
    age: Optional[int] = Field(default=None, ge=0, le=150)  # Age validation

    # Foreign key relationship
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", ondelete="SET NULL")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

### Model Variants Pattern
```python
# Base model with shared fields
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

# Database model (includes ID)
class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team: Optional[Team] = Relationship(back_populates="heroes")

# Creation model (when ID is not needed)
class HeroCreate(HeroBase):
    pass

# Update model (all fields optional)
class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None

# Public model (safe for API responses)
class HeroPublic(HeroBase):
    id: int
```

## Database Session Management

### FastAPI Dependency
```python
from sqlmodel import Session, create_engine
from fastapi import Depends

# Create engine
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# In FastAPI app
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

### Alternative Session Management
```python
# Context manager approach
def create_hero_safe(hero_data: HeroCreate) -> HeroPublic:
    with Session(engine) as session:
        hero = Hero.model_validate(hero_data)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return HeroPublic.from_orm(hero)  # If using from_orm method
```

## Query Patterns

### Select Queries
```python
from sqlmodel import select

# Get by ID
hero = session.get(Hero, hero_id)
if not hero:
    raise HTTPException(status_code=404, detail="Hero not found")

# Filtered queries
statement = select(Hero).where(Hero.age > 18)
adult_heroes = session.exec(statement).all()

# Complex queries with joins
statement = select(Hero, Team).join(Team, Hero.team_id == Team.id).where(Team.name == "Avengers")
results = session.exec(statement).all()
```

### Update Operations
```python
def update_hero(session: Session, hero_id: int, hero_update: HeroUpdate) -> HeroPublic:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero_update.model_dump(exclude_unset=True)
    hero.sqlmodel_update(hero_data)  # Efficient update method
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

## Security Best Practices

### SQL Injection Prevention
```python
# CORRECT - Using SQLModel's parameterized queries
user_input = request_data.get("id", "")
statement = select(Hero).where(Hero.id == user_input)
result = session.exec(statement).first()

# WRONG - Direct string concatenation (vulnerable to injection)
user_id = input("Type the user ID: ")
statement = f"SELECT * FROM hero WHERE id = {user_id}"  # Don't do this!
```

### Input Validation
```python
from pydantic import validator

class HeroCreate(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    secret_name: str = Field(max_length=50)
    age: Optional[int] = Field(default=None, ge=0, le=150)

    @validator('name')
    def validate_name(cls, v):
        if v.lower().strip() != v:
            raise ValueError('Name must be in proper case')
        return v.strip()
```

## Testing Patterns

### Test Setup
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
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
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### Sample Test Cases
```python
def test_create_hero(client: TestClient):
    response = client.post(
        "/heroes/",
        json={"name": "Spider-Man", "secret_name": "Peter Parker", "age": 21}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Spider-Man"
    assert data["secret_name"] == "Peter Parker"
    assert data["age"] == 21
    assert data["id"] is not None

def test_create_hero_incomplete(client: TestClient):
    # Missing required field
    response = client.post("/heroes/", json={"name": "Spider-Man"})
    assert response.status_code == 422

def test_read_hero_by_id(session: Session, client: TestClient):
    hero = Hero(name="Iron Man", secret_name="Tony Stark", age=45)
    session.add(hero)
    session.commit()

    response = client.get(f"/heroes/{hero.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero.name
    assert data["secret_name"] == hero.secret_name
    assert data["age"] == hero.age
```

## Advanced Features

### Indexes and Constraints
```python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Indexed fields for faster queries
    name: str = Field(index=True)
    secret_name: str = Field(index=True, unique=True)  # Unique constraint
    age: Optional[int] = Field(default=None, index=True)

    # Composite indexes can be defined at table level
    __table_args__ = (
        # Example of composite constraint
        # CheckConstraint('age >= 0', name='positive_age_check'),
    )
```

### Cascade Delete Relationships
```python
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # With cascade delete - when team is deleted, heroes are deleted too
    heroes: List["Hero"] = Relationship(back_populates="team", cascade_delete=True)

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    # Use CASCADE delete at database level
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", ondelete="CASCADE")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

## Error Handling

### Standard HTTP Responses
```python
from fastapi import HTTPException

def get_hero_or_raise(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=404,
            detail=f"Hero with id {hero_id} not found"
        )
    return hero

def validate_hero_creation_data(hero_data: HeroCreate) -> None:
    if hero_data.age is not None and (hero_data.age < 0 or hero_data.age > 150):
        raise HTTPException(
            status_code=422,
            detail="Age must be between 0 and 150"
        )
```

## Performance Considerations

### Pagination
```python
from fastapi import Query

@app.get("/heroes/", response_model=List[HeroPublic])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=100)
):
    heroes = session.exec(
        select(Hero).offset(offset).limit(limit)
    ).all()
    return heroes
```

### N+1 Prevention
```python
from sqlalchemy.orm import selectinload

# Eager loading to prevent N+1 queries
statement = select(Hero).options(selectinload(Hero.team))
heroes = session.exec(statement).all()
```