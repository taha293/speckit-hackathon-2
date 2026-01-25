---
name: fastapi-builder
description: |
  Comprehensive FastAPI application builder with support for CRUD operations, models, authentication, and database integration.
  Use when Claude needs to create FastAPI applications with: (1) Database models and CRUD endpoints, (2) Authentication and authorization systems,
  (3) SQLModel/SQLAlchemy integration, (4) Pydantic validation, or (5) Production-ready API structures with documentation.
---

# FastAPI Builder Skill

This skill provides comprehensive guidance for building production-ready FastAPI applications with database integration, authentication, and CRUD operations.

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI structure, patterns, dependencies, and project layout |
| **Conversation** | User's specific requirements, models needed, authentication preferences, database choices |
| **Skill References** | FastAPI patterns from `references/` (models, CRUD, auth, best practices) |
| **User Guidelines** | Project-specific conventions, team standards, deployment requirements |

Ensure all required context is gathered before implementing.

## Core Capabilities

### 1. Model Generation
- Create SQLModel/Pydantic models with proper validation
- Generate base, create, update, and public response models
- Handle relationships between models

### 2. CRUD Endpoint Generation
- Full Create, Read, Update, Delete operations
- Proper response models and status codes
- Pagination and filtering support

### 3. Authentication Systems
- JWT token authentication
- OAuth2 password flow
- User registration and login endpoints
- Protected endpoints with dependencies

### 4. Database Integration
- SQLModel with SQLite/PostgreSQL setup
- Session dependency management
- Connection pooling and optimization

## FastAPI Best Practices

### Application Structure
```python
# Recommended project structure
project/
├── main.py              # FastAPI app instance
├── models/              # Pydantic/SQLModel models
├── schemas/             # API schemas
├── database/            # DB setup and session management
├── auth/                # Authentication logic
├── routers/             # API route handlers
└── requirements.txt     # Dependencies
```

### Model Patterns
- Use SQLModel for database models with Pydantic validation
- Separate input, output, and database models
- Leverage inheritance for common fields

### Dependency Injection
- Use Depends() for database sessions
- Create reusable dependency functions
- Handle authentication as dependencies

## Implementation Guidelines

### Model Creation Process
1. Define base model with common fields
2. Create input models for POST/PUT requests
3. Create output models for responses
4. Implement database model inheriting from base

### CRUD Endpoint Standards
- POST for creation (201 Created)
- GET for reading (200 OK)
- PATCH for partial updates (200 OK)
- DELETE for removal (204 No Content or 200 with success message)

### Authentication Flow
1. OAuth2PasswordBearer for token authentication
2. JWT tokens with configurable expiration
3. Password hashing with Argon2 or bcrypt
4. Current user dependency for protected endpoints

## Quick Start Patterns

### Basic Model with CRUD
```
User requests: "Create a User model with CRUD operations"
Response: Generate SQLModel, create router with full CRUD, and database setup
```

### Authentication-Protected Endpoints
```
User requests: "Add authentication to my API"
Response: Implement JWT auth, token endpoints, and protected routes
```

### Database Integration
```
User requests: "Connect to PostgreSQL with FastAPI"
Response: Configure engine, sessions, and connection pooling
```

## Error Handling
- Use HTTPException for proper error responses
- Implement consistent error response format
- Handle validation errors automatically with Pydantic

## Security Considerations
- Input validation with Pydantic
- SQL injection prevention with ORM
- Secure password hashing
- CORS configuration for web clients
- Rate limiting for API protection

## Testing Recommendations
- Use pytest with FastAPI TestClient
- Mock database connections for unit tests
- Test authentication flows separately
- Validate response schemas automatically