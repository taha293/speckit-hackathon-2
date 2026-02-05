#!/usr/bin/env python3
"""
SQLModel Project Setup Script

This script generates a complete SQLModel project structure with models,
FastAPI endpoints, database setup, and testing.
"""

import os
import argparse
from pathlib import Path

def create_directory_structure(base_path):
    """Create the basic directory structure for a SQLModel project."""
    directories = [
        base_path / "models",
        base_path / "api",
        base_path / "database",
        base_path / "tests",
        base_path / "schemas"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        # Create __init__.py files
        (directory / "__init__.py").touch(exist_ok=True)

def create_base_models(base_path):
    """Create base SQLModel models."""
    models_dir = base_path / "models"

    # Base model
    base_model_content = '''"""
Base SQLModel Definitions
"""
from sqlmodel import Field, SQLModel
from typing import Optional


class TimestampMixin(SQLModel):
    """Mixin to add timestamp fields to models."""
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)


class BaseSQLModel(TimestampMixin, SQLModel):
    """Base model with common fields."""
    pass
'''

    with open(models_dir / "base.py", "w") as f:
        f.write(base_model_content)

def create_sample_model(base_path, model_name="hero", has_relationships=False):
    """Create a sample model with CRUD operations."""
    models_dir = base_path / "models"

    # Model with variants
    model_content = f'''"""
{model_name.title()} Model Definitions
"""
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from .base import BaseSQLModel


class {model_name.title()}Base(BaseSQLModel):
    """Base {model_name} model with shared attributes."""
    name: str = Field(index=True, min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)


class {model_name.title()}({model_name.title()}Base, table=True):
    """{model_name.title()} database model."""
    id: Optional[int] = Field(default=None, primary_key=True)

{'    ' + f'{model_name}s: List["{model_name.title()}"] = Relationship(back_populates="{model_name}s")' if has_relationships else ''}


class {model_name.title()}Create({model_name.title()}Base):
    """{model_name.title()} creation model."""
    pass


class {model_name.title()}Update(SQLModel):
    """{model_name.title()} update model with optional fields."""
    name: Optional[str] = None
    description: Optional[str] = None


class {model_name.title()}Public({model_name.title()}Base):
    """Public {model_name} model without sensitive data."""
    id: int
'''

    with open(models_dir / f"{model_name}.py", "w") as f:
        f.write(model_content)

def create_database_setup(base_path):
    """Create database setup and session management."""
    db_dir = base_path / "database"

    engine_content = '''"""
Database Engine Setup
"""
from sqlmodel import create_engine, SQLModel
import os


# Database URL - can be configured via environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sqlmodel_database.db")

# Create engine with appropriate settings
engine = create_engine(DATABASE_URL, echo=bool(os.getenv("DB_ECHO", False)))


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)
'''

    session_content = '''"""
Database Session Management
"""
from contextlib import contextmanager
from sqlmodel import Session
from .engine import engine


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session


def get_session_factory():
    """Get a session factory for dependency injection."""
    return lambda: Session(engine)
'''

    with open(db_dir / "engine.py", "w") as f:
        f.write(engine_content)

    with open(db_dir / "session.py", "w") as f:
        f.write(session_content)

def create_api_endpoints(base_path, model_name="hero"):
    """Create FastAPI endpoints for the model."""
    api_dir = base_path / "api"

    endpoints_content = f'''"""
{model_name.title()} API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from ..database.session import get_session
from ..models.{model_name} import (
    {model_name.title()},
    {model_name.title()}Create,
    {model_name.title()}Update,
    {model_name.title()}Public
)


router = APIRouter()


@router.post("/", response_model={model_name.title()}Public)
def create_{model_name}(
    {model_name}: {model_name.title()}Create,
    session=Depends(get_session)
):
    """Create a new {model_name}."""
    db_{model_name} = {model_name.title()}.model_validate({model_name})
    session.add(db_{model_name})
    session.commit()
    session.refresh(db_{model_name})
    return db_{model_name}


@router.get("/", response_model=List[{model_name.title()}Public])
def read_{model_name}s(
    skip: int = 0,
    limit: int = 100,
    session=Depends(get_session)
):
    """Retrieve {model_name}s."""
    {model_name}s = session.exec(
        select({model_name.title()}).offset(skip).limit(limit)
    ).all()
    return {model_name}s


@router.get("/{model_name}_id", response_model={model_name.title()}Public)
def read_{model_name}(
    {model_name}_id: int,
    session=Depends(get_session)
):
    """Get a specific {model_name} by ID."""
    {model_name} = session.get({model_name.title()}, {model_name}_id)
    if not {model_name}:
        raise HTTPException(status_code=404, detail="{model_name.title()} not found")
    return {model_name}


@router.patch("/{model_name}_id", response_model={model_name.title()}Public)
def update_{model_name}(
    {model_name}_id: int,
    {model_name}_update: {model_name.title()}Update,
    session=Depends(get_session)
):
    """Update a {model_name}."""
    {model_name} = session.get({model_name.title()}, {model_name}_id)
    if not {model_name}:
        raise HTTPException(status_code=404, detail="{model_name.title()} not found")

    update_data = {model_name}_update.model_dump(exclude_unset=True)
    {model_name}.sqlmodel_update(update_data)
    session.add({model_name})
    session.commit()
    session.refresh({model_name})
    return {model_name}


@router.delete("/{model_name}_id")
def delete_{model_name}(
    {model_name}_id: int,
    session=Depends(get_session)
):
    """Delete a {model_name}."""
    {model_name} = session.get({model_name.title()}, {model_name}_id)
    if not {model_name}:
        raise HTTPException(status_code=404, detail="{model_name.title()} not found")

    session.delete({model_name})
    session.commit()
    return {{'message': '{model_name.title()} deleted successfully'}}
'''

    with open(api_dir / f"{model_name}_api.py", "w") as f:
        f.write(endpoints_content)

def create_main_app(base_path):
    """Create the main FastAPI application."""
    main_content = '''"""
Main FastAPI Application
"""
from fastapi import FastAPI
from .database.engine import create_db_and_tables
from .api.hero_api import router as hero_router


app = FastAPI(title="SQLModel API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup."""
    create_db_and_tables()


# Include API routers
app.include_router(hero_router, prefix="/api/v1/heroes", tags=["heroes"])


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to SQLModel API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    with open(base_path / "main.py", "w") as f:
        f.write(main_content)

def create_requirements(base_path):
    """Create requirements.txt file."""
    requirements_content = '''fastapi==0.104.1
sqlmodel==0.0.16
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
pytest==7.4.3
httpx==0.25.2
SQLAlchemy==2.0.23
'''

    with open(base_path / "requirements.txt", "w") as f:
        f.write(requirements_content)

def create_pyproject_toml(base_path):
    """Create pyproject.toml file."""
    toml_content = '''[tool.poetry]
name = "sqlmodel-project"
version = "0.1.0"
description = "A project using SQLModel for database models and FastAPI for API endpoints"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
fastapi = "^0.104.1"
sqlmodel = "^0.0.16"
uvicorn = {extras = ["standard"], version = "^0.24.0"}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
httpx = "^0.25.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
'''

    with open(base_path / "pyproject.toml", "w") as f:
        f.write(toml_content)

def create_readme(base_path):
    """Create README.md file."""
    readme_content = '''# SQLModel Project

This is a project using SQLModel for database models and FastAPI for API endpoints.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or with Poetry:
```bash
poetry install
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`.

## API Documentation

- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Project Structure

- `models/` - SQLModel database models
- `api/` - FastAPI endpoints
- `database/` - Database setup and session management
- `tests/` - Test files
- `schemas/` - Pydantic schemas
'''

    with open(base_path / "README.md", "w") as f:
        f.write(readme_content)

def main():
    parser = argparse.ArgumentParser(description="Setup a SQLModel project")
    parser.add_argument("--name", default="sqlmodel-app", help="Name of the project")
    parser.add_argument("--model", default="hero", help="Sample model name")
    parser.add_argument("--has-relationships", action="store_true",
                       help="Include relationship fields in models")

    args = parser.parse_args()

    project_path = Path(args.name)

    # Create directory structure
    create_directory_structure(project_path)

    # Create base models
    create_base_models(project_path)

    # Create sample model
    create_sample_model(project_path, args.model, args.has_relationships)

    # Create database setup
    create_database_setup(project_path)

    # Create API endpoints
    create_api_endpoints(project_path, args.model)

    # Create main app
    create_main_app(project_path)

    # Create supporting files
    create_requirements(project_path)
    create_pyproject_toml(project_path)
    create_readme(project_path)

    print(f"SQLModel project '{args.name}' has been created successfully!")
    print("Next steps:")
    print(f"1. cd {args.name}")
    print("2. pip install -r requirements.txt")
    print("3. python main.py")


if __name__ == "__main__":
    main()