# FastAPI CRUD Operations

## Standard CRUD Pattern

### Complete CRUD Implementation
```python
from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel

# Models defined elsewhere
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
    secret_name: str

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    pass

class HeroUpdate(HeroBase):
    name: Optional[str] = None
    age: Optional[int] = None
    secret_name: Optional[str] = None

# Database session dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# CREATE - POST
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep) -> HeroPublic:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# READ ALL - GET
@app.get("/heroes/", response_model=List[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[HeroPublic]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# READ SINGLE - GET by ID
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep) -> HeroPublic:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# UPDATE - PATCH
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(
    hero_id: int,
    hero: HeroUpdate,
    session: SessionDep
) -> HeroPublic:
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

# DELETE - DELETE
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep) -> dict:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

## Advanced CRUD Patterns

### Filtering and Searching
```python
@app.get("/heroes/")
def read_heroes_filtered(
    session: SessionDep,
    name: Optional[str] = Query(None, description="Filter by name"),
    min_age: Optional[int] = Query(None, ge=0),
    max_age: Optional[int] = Query(None, le=150),
    offset: int = 0,
    limit: int = Query(100, le=100)
) -> List[HeroPublic]:
    query = select(Hero)

    if name:
        query = query.where(Hero.name.contains(name))
    if min_age is not None:
        query = query.where(Hero.age >= min_age)
    if max_age is not None:
        query = query.where(Hero.age <= max_age)

    heroes = session.exec(query.offset(offset).limit(limit)).all()
    return heroes
```

### Sorting
```python
from enum import Enum

class SortField(str, Enum):
    id = "id"
    name = "name"
    age = "age"
    created_at = "created_at"

@app.get("/heroes/")
def read_heroes_sorted(
    session: SessionDep,
    sort_by: SortField = SortField.id,
    sort_desc: bool = False,
    offset: int = 0,
    limit: int = Query(100, le=100)
) -> List[HeroPublic]:
    query = select(Hero)

    # Apply sorting
    if sort_desc:
        query = query.order_by(getattr(Hero, sort_by.value).desc())
    else:
        query = query.order_by(getattr(Hero, sort_by.value))

    heroes = session.exec(query.offset(offset).limit(limit)).all()
    return heroes
```

### Bulk Operations
```python
# Bulk Create
@app.post("/heroes/bulk/")
def create_heroes_bulk(heroes: List[HeroCreate], session: SessionDep) -> List[HeroPublic]:
    db_heroes = []
    for hero in heroes:
        db_hero = Hero.model_validate(hero)
        session.add(db_hero)
        db_heroes.append(db_hero)

    session.commit()
    for db_hero in db_heroes:
        session.refresh(db_hero)

    return db_heroes

# Bulk Delete
@app.delete("/heroes/bulk/")
def delete_heroes_bulk(hero_ids: List[int], session: SessionDep) -> dict:
    deleted_count = 0
    for hero_id in hero_ids:
        hero = session.get(Hero, hero_id)
        if hero:
            session.delete(hero)
            deleted_count += 1

    session.commit()
    return {"deleted": deleted_count, "total_requested": len(hero_ids)}
```

## Error Handling Patterns

### Custom Exceptions
```python
from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, resource_type: str, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_type} with id {resource_id} not found"
        )

class ValidationErrorException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )
```

### Enhanced Error Responses
```python
from datetime import datetime
from typing import Optional

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[dict] = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTP Exception",
            message=str(exc.detail),
            details={"status_code": exc.status_code}
        ).dict()
    )
```

## Performance Optimization

### Pagination with Total Count
```python
class PaginatedResponse(BaseModel):
    data: List[HeroPublic]
    total: int
    offset: int
    limit: int

@app.get("/heroes/", response_model=PaginatedResponse)
def read_heroes_paginated(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(100, le=100)
) -> PaginatedResponse:
    # Count total records
    total = session.exec(select(func.count(Hero.id))).one()

    # Get paginated data
    heroes = session.exec(
        select(Hero).offset(offset).limit(limit)
    ).all()

    return PaginatedResponse(
        data=heroes,
        total=total,
        offset=offset,
        limit=limit
    )
```

### Database Session Optimization
```python
# Use read-only sessions when appropriate
@app.get("/heroes/")
def read_heroes_readonly(session: SessionDep) -> List[HeroPublic]:
    # This query is read-only, so we don't need to worry about commits
    heroes = session.exec(select(Hero)).all()
    return heroes

# Batch operations for efficiency
@app.put("/heroes/batch-update/")
def batch_update_heroes(
    updates: List[HeroUpdateWithId],
    session: SessionDep
) -> dict:
    updated_count = 0
    for update_item in updates:
        hero = session.get(Hero, update_item.id)
        if hero:
            hero_data = update_item.model_dump(exclude={'id'})
            hero.sqlmodel_update(hero_data)
            updated_count += 1

    session.commit()
    return {"updated": updated_count, "total": len(updates)}
```

## Validation and Business Logic

### Pre-create Validation
```python
@app.post("/heroes/", response_model=HeroPublic)
def create_hero_validated(hero: HeroCreate, session: SessionDep) -> HeroPublic:
    # Check for duplicates
    existing_hero = session.exec(
        select(Hero).where(Hero.name == hero.name)
    ).first()

    if existing_hero:
        raise HTTPException(
            status_code=400,
            detail="Hero with this name already exists"
        )

    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

### Post-operation Hooks
```python
from sqlalchemy import event

# Define event listeners for database operations
@event.listens_for(Hero, 'before_insert')
def before_hero_insert(mapper, connection, target):
    # Perform actions before insert
    target.created_at = datetime.utcnow()

@event.listens_for(Hero, 'after_update')
def after_hero_update(mapper, connection, target):
    # Perform actions after update
    target.updated_at = datetime.utcnow()
```

## Testing Patterns

### CRUD Operation Tests
```python
import pytest
from fastapi.testclient import TestClient

def test_create_hero(client: TestClient):
    response = client.post("/heroes/", json={
        "name": "Test Hero",
        "secret_name": "Secret Identity",
        "age": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Hero"
    assert data["secret_name"] == "Secret Identity"

def test_read_hero(client: TestClient, created_hero_id: int):
    response = client.get(f"/heroes/{created_hero_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_hero_id

def test_update_hero(client: TestClient, created_hero_id: int):
    response = client.patch(f"/heroes/{created_hero_id}", json={
        "name": "Updated Hero Name"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Hero Name"

def test_delete_hero(client: TestClient, created_hero_id: int):
    response = client.delete(f"/heroes/{created_hero_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True
```