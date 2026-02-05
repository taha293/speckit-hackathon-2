from sqlmodel import Session, select
from models.user import User, UserCreate
from utils.security import hash_password, verify_password
from typing import Optional
import uuid

class UserService:
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user with hashed password"""
        # Check if user with this email already exists
        existing_user = db.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise ValueError("Email already registered")

        # Create new user
        hashed_pwd = hash_password(user_create.password)
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_create.email,
            hashed_password=hashed_pwd
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.exec(select(User).where(User.email == email)).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.exec(select(User).where(User.id == user_id)).first()