# SQLModel Code Templates

## Basic Model Template

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class {{ModelName}}Base(SQLModel):
    """Base {{ModelName}} model with shared attributes."""
    name: str = Field(index=True, min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)


class {{ModelName}}({{ModelName}}Base, table=True):
    """{{ModelName}} database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    {% if has_relationships %}
    related_items: List["RelatedModel"] = Relationship(back_populates="{{model_name}}")
    {% endif %}


class {{ModelName}}Create({{ModelName}}Base):
    """{{ModelName}} creation model."""
    pass


class {{ModelName}}Update(SQLModel):
    """{{ModelName}} update model with optional fields."""
    name: Optional[str] = None
    description: Optional[str] = None


class {{ModelName}}Public({{ModelName}}Base):
    """Public {{ModelName}} model without sensitive data."""
    id: int
```

## FastAPI Endpoint Template

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from database.session import get_session
from models.{{model_name}} import (
    {{ModelName}},
    {{ModelName}}Create,
    {{ModelName}}Update,
    {{ModelName}}Public
)

router = APIRouter(prefix="/{{model_name}}s", tags=["{{model_name}}s"])


@router.post("/", response_model={{ModelName}}Public)
def create_{{model_name}}(
    {{model_name}}: {{ModelName}}Create,
    session=Depends(get_session)
):
    """Create a new {{model_name}}."""
    db_{{model_name}} = {{ModelName}}.model_validate({{model_name}})
    session.add(db_{{model_name}})
    session.commit()
    session.refresh(db_{{model_name}})
    return db_{{model_name}}


@router.get("/", response_model=List[{{ModelName}}Public])
def read_{{model_name}}s(
    skip: int = 0,
    limit: int = 100,
    session=Depends(get_session)
):
    """Retrieve {{model_name}}s."""
    {{model_name}}s = session.exec(
        select({{ModelName}}).offset(skip).limit(limit)
    ).all()
    return {{model_name}}s


@router.get("/{model_name}_id", response_model={{ModelName}}Public)
def read_{{model_name}}(
    {{model_name}}_id: int,
    session=Depends(get_session)
):
    """Get a specific {{model_name}} by ID."""
    {{model_name}} = session.get({{ModelName}}, {{model_name}}_id)
    if not {{model_name}}:
        raise HTTPException(status_code=404, detail="{{ModelName}} not found")
    return {{model_name}}


@router.patch("/{model_name}_id", response_model={{ModelName}}Public)
def update_{{model_name}}(
    {{model_name}}_id: int,
    {{model_name}}_update: {{ModelName}}Update,
    session=Depends(get_session)
):
    """Update a {{model_name}}."""
    {{model_name}} = session.get({{ModelName}}, {{model_name}}_id)
    if not {{model_name}}:
        raise HTTPException(status_code=404, detail="{{ModelName}} not found")

    update_data = {{model_name}}_update.model_dump(exclude_unset=True)
    {{model_name}}.sqlmodel_update(update_data)
    session.add({{model_name}})
    session.commit()
    session.refresh({{model_name}})
    return {{model_name}}


@router.delete("/{model_name}_id")
def delete_{{model_name}}(
    {{model_name}}_id: int,
    session=Depends(get_session)
):
    """Delete a {{model_name}}."""
    {{model_name}} = session.get({{ModelName}}, {{model_name}}_id)
    if not {{model_name}}:
        raise HTTPException(status_code=404, detail="{{ModelName}} not found")

    session.delete({{model_name}})
    session.commit()
    return {'message': '{{ModelName}} deleted successfully'}
```

## Database Setup Template

```python
from sqlmodel import create_engine, SQLModel
import os


# Database URL - can be configured via environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sqlmodel_database.db")

# Create engine with appropriate settings
engine = create_engine(DATABASE_URL, echo=bool(os.getenv("DB_ECHO", False)))


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)
```

## Test Template

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from models.{{model_name}} import {{ModelName}}


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


def test_create_{{model_name}}(client: TestClient):
    """Test creating a {{model_name}}."""
    response = client.post(
        "/api/v1/{{model_name}}s/",
        json={"name": "{{ModelName}} Name", "description": "Description here"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "{{ModelName}} Name"
    assert data["description"] == "Description here"
    assert data["id"] is not None
```