from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure bcrypt with proper backend
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
    bcrypt__min_rounds=12,
)

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt"""
    # Ensure password doesn't exceed 72 bytes for bcrypt
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash"""
    # Ensure password doesn't exceed 72 bytes for bcrypt
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)