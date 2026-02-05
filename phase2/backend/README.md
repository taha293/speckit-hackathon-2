# Todo Backend API

Backend API for Todo application with JWT authentication, PostgreSQL persistence, and user data isolation.

## Features

- JWT-based authentication with secure token handling
- User registration and login functionality
- Secure task management with user data isolation
- RESTful API with proper error handling
- PostgreSQL database with SQLModel ORM

## Prerequisites

- Python 3.9+
- PostgreSQL database (or Neon Serverless PostgreSQL)

## Installation

1. Clone the repository
2. Navigate to the backend directory: `cd phase2/backend`
3. Install dependencies: `pip install -e .` (or use your preferred method based on pyproject.toml)

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=postgresql://username:password@localhost/dbname
```

## Running the Application

```bash
# Using uvicorn directly
uvicorn main:app --reload --port 8000

# Or run the main module
python -m main
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## API Endpoints

### Authentication

#### Register a new user
- **Endpoint**: `POST /api/v1/auth/register`
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
- **Response**: `{"message": "User created successfully"}`

#### Login to get JWT token
- **Endpoint**: `POST /api/v1/auth/login`
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
- **Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Task Management

All task endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

#### Get all tasks for current user
- **Endpoint**: `GET /api/v1/tasks`
- **Headers**:
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
- **Response**: Array of task objects

#### Create a new task
- **Endpoint**: `POST /api/v1/tasks`
- **Headers**:
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
  - `Content-Type: application/json`
- **Request Body**:
```json
{
  "title": "Task title (1-200 characters)",
  "description": "Optional description (max 1000 characters)",
  "completed": false
}
```
- **Response**: Created task object

#### Get a specific task
- **Endpoint**: `GET /api/v1/tasks/{task_id}`
- **Headers**:
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
- **Response**: Task object

#### Update a task
- **Endpoint**: `PUT /api/v1/tasks/{task_id}`
- **Headers**:
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
  - `Content-Type: application/json`
- **Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```
- **Response**: Updated task object

#### Delete a task
- **Endpoint**: `DELETE /api/v1/tasks/{task_id}`
- **Headers**:
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
- **Response**: `{"message": "Task deleted successfully"}`

#### Toggle task completion status
- **Endpoint**: `PATCH /api/v1/tasks/{task_id}/complete`
- **Headers**:
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`
  - `Content-Type: application/json`
- **Request Body**:
```json
{
  "completed": true
}
```
- **Response**: Updated task object

## Example API Calls

### Using cURL

#### Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

#### Login to get JWT token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

#### Create a task (requires JWT token)
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive docs for the API endpoints",
    "completed": false
  }'
```

## Security

- Passwords are securely hashed using bcrypt
- JWT tokens with configurable expiration (24 hours by default)
- User data isolation - users can only access their own tasks
- Input validation on all endpoints (title: 1-200 chars, description: max 1000 chars)
- Proper authentication and authorization checks on all protected endpoints

## Database Models

- **User**: Stores user information (id, email, hashed password)
- **Task**: Stores task information (id, user_id, title, description, completed status)

## Frontend Integration Guide

### Authentication Flow
1. Register a new user with email and password
2. Login to get JWT access token
3. Store the token in local storage/session storage
4. Include the token in Authorization header for all protected requests
5. Handle 401 Unauthorized responses appropriately (redirect to login)

### Error Handling
- `401 Unauthorized`: Invalid or expired JWT token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error in request body
- `500 Internal Server Error`: Server-side error

### Example JavaScript Implementation
```javascript
// Store JWT token after login
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data;
  }
  throw new Error('Login failed');
};

// Create a task
const createTask = async (taskData) => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/v1/tasks', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(taskData)
  });

  if (response.ok) {
    return await response.json();
  }
  throw new Error('Failed to create task');
};
```