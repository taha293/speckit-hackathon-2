# FastAPI Authentication

## JWT Authentication Setup

### Core Configuration
```python
from datetime import datetime, timedelta
from typing import Optional
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, Session, select

# Security configuration
SECRET_KEY = "your-secret-key-here"  # Generate with: secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

### User Models
```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(SQLModel):
    username: str = Field(unique=True)
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(exclude=True)

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDB(User):
    pass
```

## Password Hashing Functions

### Hashing and Verification
```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a hash for a plain text password."""
    return pwd_context.hash(password)

def authenticate_user(session: Session, username: str, password: str):
    """
    Authenticate user by username and password.
    Returns UserInDB object if valid, False otherwise.
    """
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
```

## JWT Token Management

### Token Creation
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with optional custom expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Token Validation
```python
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    Dependency function that validates JWT token and returns current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Dependency function that validates the user is active.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

## Authentication Endpoints

### Login Endpoint
```python
from fastapi import FastAPI, Depends
from datetime import timedelta

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
```

### Registration Endpoint
```python
@app.post("/users/register", response_model=UserPublic)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user account.
    """
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.username == user.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
```

## Protected Routes

### Using Authentication Dependencies
```python
@app.get("/users/me", response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's profile information.
    """
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """
    Get items belonging to the current user.
    """
    return [{"item_id": 1, "owner": current_user.username}]

@app.put("/users/me")
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update current user's profile information.
    """
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
```

## Role-Based Access Control (RBAC)

### Role Models and Dependencies
```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class UserWithRole(UserPublic):
    role: UserRole = UserRole.USER

def require_role(required_role: UserRole):
    """
    Dependency to check if user has required role.
    """
    def role_checker(current_user: User = Depends(get_current_active_user)):
        # In a real app, user roles would be stored in the database
        user_role = getattr(current_user, 'role', UserRole.USER)

        if user_role != required_role and user_role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Usage example
@app.get("/admin/users")
async def get_all_users(
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Admin-only endpoint to get all users.
    """
    # Implementation here
    pass
```

## Security Best Practices

### Environment Variables for Secrets
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
```

### Rate Limiting for Authentication
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@app.post("/token")
@limiter.limit("5/minute")  # Limit login attempts
async def login_for_access_token(...):
    # Implementation here
    pass
```

### Password Validation
```python
import re
from pydantic import validator

class UserCreateWithValidation(UserCreate):
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
```

## Session Management

### Logout and Token Blacklisting
```python
# In-memory store for blacklisted tokens (use Redis in production)
blacklisted_tokens = set()

def blacklist_token(token: str):
    """Add token to blacklist."""
    blacklisted_tokens.add(token)

def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted."""
    return token in blacklisted_tokens

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """Logout user by blacklisting their token."""
    blacklist_token(token)
    return {"message": "Successfully logged out"}
```

## Testing Authentication

### Authentication Tests
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_user_registration(client: TestClient):
    """Test user registration endpoint."""
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_login_success(client: TestClient):
    """Test successful login."""
    # First register a user
    client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!"
    })

    # Then login
    response = client.post("/token", data={
        "username": "testuser",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_protected_route(client: TestClient):
    """Test access to protected route."""
    # Login first
    login_response = client.post("/token", data={
        "username": "testuser",
        "password": "SecurePass123!"
    })
    token = login_response.json()["access_token"]

    # Access protected route
    response = client.get("/users/me",
                         headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```