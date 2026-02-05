"""Database initialization script for the Todo backend API."""
from sqlmodel import SQLModel
from database import engine
from models.user import User
from models.task import Task

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()