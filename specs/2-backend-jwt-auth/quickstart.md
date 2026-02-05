# Quickstart Guide: Backend JWT Authentication API

## Prerequisites

- Python 3.8+
- pip package manager
- Git
- Access to Neon PostgreSQL database

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
# Create the project structure as specified in the feature
mkdir -p root/phase2/backend
cd root/phase2/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlmodel python-jose[cryptography] bcrypt python-multipart psycopg2-binary
```

### 4. Environment Configuration
Create a `.env` file with the following variables:
```bash
# Database
DATABASE_URL="postgresql://username:password@localhost/dbname"

# JWT Configuration
SECRET_KEY="your-secret-key-here"  # Use a strong secret key
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# Server
HOST="0.0.0.0"
PORT=8000
```

## Running the Application

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Usage Examples

### Register a New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Get Tasks (with JWT token)
```bash
curl -X GET "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Create a Task (with JWT token)
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "title": "Sample task",
    "description": "Sample description"
  }'
```

## Project Structure
```
root/
└── phase2/
    └── backend/
        ├── main.py              # Application entry point
        ├── models.py            # SQLModel database models
        ├── schemas.py           # Pydantic request/response schemas
        ├── database.py          # Database session management
        ├── auth.py              # Authentication utilities
        ├── crud.py              # Database operations
        ├── dependencies.py      # FastAPI dependencies
        └── requirements.txt     # Python dependencies
```

## Key Components

### Authentication Flow
1. User registers with email and password
2. Password is hashed using bcrypt
3. User is stored in database
4. On login, credentials are verified
5. JWT token is generated and returned
6. Subsequent requests require the JWT token in Authorization header

### Security Measures
- Passwords are hashed using bcrypt
- JWT tokens use HS256 algorithm
- All sensitive endpoints require authentication
- Input validation on all endpoints
- SQL injection prevention through ORM usage