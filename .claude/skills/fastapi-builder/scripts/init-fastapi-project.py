#!/usr/bin/env python3
"""
FastAPI Project Initializer Script

This script creates a new FastAPI project with recommended structure and configurations.
"""

import os
import sys
from pathlib import Path
import argparse
from typing import Dict, List


def create_directory_structure(base_path: Path) -> None:
    """Create the recommended FastAPI project directory structure."""
    directories = [
        base_path / "app",
        base_path / "app" / "models",
        base_path / "app" / "schemas",
        base_path / "app" / "routers",
        base_path / "app" / "database",
        base_path / "app" / "auth",
        base_path / "app" / "utils",
        base_path / "tests",
        base_path / "docs",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")


def create_main_file(base_path: Path) -> None:
    """Create the main FastAPI application file."""
    main_content = '''from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.session import engine
from app.database.setup import create_db_and_tables
from app.routers import users, items  # Import your routers here


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print("Starting up...")
    # Create database tables on startup
    create_db_and_tables(engine)
    yield
    print("Shutting down...")


app = FastAPI(
    title="FastAPI Project",
    description="A production-ready FastAPI application",
    version="1.0.0",
    lifespan=lifespan
)


# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to FastAPI!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    main_file = base_path / "app" / "main.py"
    main_file.write_text(main_content)
    print(f"Created main file: {main_file}")


def create_database_files(base_path: Path) -> None:
    """Create database configuration files."""
    # Database session
    session_content = '''from sqlmodel import create_engine, Session
from typing import Generator
from app.core.config import settings


# Create database engine
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=settings.DB_ECHO,  # Set to True to log SQL queries
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=300,      # Recycle connections every 5 minutes
)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
'''

    session_file = base_path / "app" / "database" / "session.py"
    session_file.write_text(session_content)
    print(f"Created database session: {session_file}")

    # Database setup
    setup_content = '''from sqlmodel import SQLModel
from app.database.session import engine


def create_db_and_tables(db_engine=None):
    """Create all database tables."""
    if db_engine is None:
        db_engine = engine
    SQLModel.metadata.create_all(db_engine)
'''

    setup_file = base_path / "app" / "database" / "setup.py"
    setup_file.write_text(setup_content)
    print(f"Created database setup: {setup_file}")


def create_config_file(base_path: Path) -> None:
    """Create configuration file."""
    config_content = '''from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    DB_ECHO: bool = False

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
'''

    config_file = base_path / "app" / "core" / "config.py"
    config_file.write_text(config_content)
    print(f"Created config file: {config_file}")


def create_env_file(base_path: Path) -> None:
    """Create .env file template."""
    env_content = '''# Database
DATABASE_URL=sqlite:///./sql_app.db

# Security
SECRET_KEY=change_this_to_a_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=False
'''

    env_file = base_path / ".env"
    env_file.write_text(env_content)
    print(f"Created .env file: {env_file}")


def create_requirements_file(base_path: Path) -> None:
    """Create requirements.txt file."""
    requirements_content = '''fastapi>=0.104.1
uvicorn[standard]>=0.24.0
sqlmodel>=0.0.16
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[argon2]>=1.7.4
python-multipart>=0.0.6
python-dotenv>=1.0.0
alembic>=1.13.1
pytest>=7.4.0
httpx>=0.25.0
sqlalchemy>=2.0.23
psycopg2-binary>=2.9.9  # For PostgreSQL
asyncpg>=0.29.0          # For async PostgreSQL
'''

    req_file = base_path / "requirements.txt"
    req_file.write_text(requirements_content)
    print(f"Created requirements file: {req_file}")


def create_gitignore_file(base_path: Path) -> None:
    """Create .gitignore file."""
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Environment variables
.env
.env.local
.env.production
.env.development

# Database
*.db
*.db-journal

# Coverage
.coverage
htmlcov/

# FastAPI
.DS_Store
'''

    gitignore_file = base_path / ".gitignore"
    gitignore_file.write_text(gitignore_content)
    print(f"Created .gitignore file: {gitignore_file}")


def create_readme(base_path: Path, project_name: str) -> None:
    """Create README.md file."""
    readme_content = f'''# {project_name}

A production-ready FastAPI application.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
{project_name}/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app instance
│   ├── core/               # Configuration and utilities
│   ├── models/             # SQLModel/Pydantic models
│   ├── schemas/            # API schemas
│   ├── routers/            # API route handlers
│   ├── database/           # Database setup and session management
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
└── .gitignore
```

## API Documentation

- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Alternative docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)
'''

    readme_file = base_path / "README.md"
    readme_file.write_text(readme_content)
    print(f"Created README file: {readme_file}")


def main():
    parser = argparse.ArgumentParser(description="Initialize a new FastAPI project")
    parser.add_argument("project_name", help="Name of the project directory to create")
    parser.add_argument("--path", default=".", help="Parent directory for the project (default: current directory)")

    args = parser.parse_args()

    project_path = Path(args.path) / args.project_name

    if project_path.exists():
        print(f"Error: Directory '{project_path}' already exists!")
        sys.exit(1)

    print(f"Creating FastAPI project: {project_path}")

    # Create directory structure
    create_directory_structure(project_path)

    # Create core files
    create_main_file(project_path)
    create_database_files(project_path)
    create_config_file(project_path)
    create_env_file(project_path)
    create_requirements_file(project_path)
    create_gitignore_file(project_path)
    create_readme(project_path, args.project_name)

    print(f"\n✅ FastAPI project '{args.project_name}' has been created successfully!")
    print(f"📁 Project location: {project_path}")
    print("\nNext steps:")
    print(f"1. cd {args.project_name}")
    print("2. Create virtual environment and install dependencies")
    print("3. Update the .env file with your configuration")
    print("4. Run: uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()