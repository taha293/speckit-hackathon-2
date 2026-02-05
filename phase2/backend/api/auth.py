from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from schemas.auth import UserRegister, UserLogin, Token
from services.user_service import UserService
from utils.auth import create_access_token
from datetime import timedelta
import os

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_session)):
    """Register a new user"""
    try:
        user = UserService.create_user(db, user_data)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_session)):
    """Login user and return JWT token"""
    user = UserService.authenticate_user(
        db, user_data.email, user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")))
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
def refresh_token():
    """Refresh the access token using refresh token"""
    # This is a simplified implementation - in a real app you'd validate the refresh token
    # For now, we'll just return a new access token if the user is authenticated
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token functionality not fully implemented yet"
    )