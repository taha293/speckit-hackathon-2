from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlmodel import Session
from typing import Optional
from utils.auth import verify_token
from models.user import User
from database import get_session

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> User:
    """Dependency to get the current user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token, db)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # In a real implementation, you would query the database for the user
    # user = db.query(User).filter(User.id == user_id).first()
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User not found",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # return user

    # Placeholder for now
    return User(id=user_id, email="placeholder@example.com", hashed_password="")  # Placeholder