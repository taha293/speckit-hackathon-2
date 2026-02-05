from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - can be overridden by environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the database engine with connection pooling (max 20 connections)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300
)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session