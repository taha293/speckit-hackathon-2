---
name: sqlmodel-builder
description: |
  This skill should be used when creating SQLModel-based applications with database models,
  CRUD operations, and FastAPI integration. Provides complete SQLModel setup with
  security best practices, validation, and testing patterns.
allowed-tools: Read, Grep, Glob, Bash
---

# SQLModel Builder Skill

This skill creates robust SQLModel applications with proper database models, FastAPI integration, security measures, and testing.

## When to Use This Skill

Use this skill when you need to:
- Create SQLModel data models with proper relationships
- Build FastAPI endpoints with CRUD operations
- Set up secure database connections
- Implement proper validation and error handling
- Create test suites for SQLModel applications

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing project structure, patterns, and database setup |
| **Conversation** | User's specific requirements for models, endpoints, and functionality |
| **Skill References** | SQLModel best practices, security patterns, and API design |
| **User Guidelines** | Project-specific conventions, team standards |

Ensure all required context is gathered before implementing.

## Model Creation

When creating SQLModel models:

### Basic Model Structure
```python
from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional

class BaseModel(SQLModel):
    """Base model with common fields"""
    pass

class MyModel(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # Add index for frequently queried fields
    description: Optional[str] = None
    # Add specific fields based on requirements
```

### Model Variants
Create different variants for different API operations:
- Base model: Common fields
- Create model: Fields needed for creation
- Read/Update models: Additional fields as needed
- Public model: Safe fields for public API responses

### Relationships
- Use `Relationship()` for related entities
- Always define `back_populates` for bidirectional relationships
- Consider using `cascade_delete=True` when appropriate
- Handle foreign key constraints with `ondelete` parameter

## Database Setup

### Engine Creation
- Use appropriate connection parameters for the database type
- For SQLite, use `connect_args={"check_same_thread": False}` in production
- Set up proper connection pooling for production environments
- Configure logging with `echo=True` for debugging

### Session Management
- Use dependency injection for session management in FastAPI
- Properly close sessions to avoid connection leaks
- Use transactions appropriately for multi-operation changes

## Security Best Practices

### SQL Injection Prevention
- Always use parameterized queries through SQLModel
- Never concatenate user input directly into SQL statements
- Use SQLModel's `select()` statements with proper `.where()` clauses

### Input Validation
- Leverage Pydantic validation built into SQLModel
- Use `Field()` validators for specific constraints
- Implement proper error handling and status codes

## API Endpoints

### CRUD Operations
- POST: Create resources with proper validation
- GET: Read single and multiple resources with pagination
- PATCH: Partial updates with proper validation
- DELETE: Safe deletion with proper confirmation

### Error Handling
- Return appropriate HTTP status codes (404 for not found, 422 for validation errors)
- Provide meaningful error messages
- Don't expose internal details in error responses

## Testing Strategy

### Unit Tests
- Test model creation and validation
- Test individual CRUD operations
- Use in-memory database for testing

### Integration Tests
- Test full API endpoints
- Verify relationships and constraints
- Mock external dependencies

### Test Database Setup
- Use `StaticPool` and in-memory SQLite for fast tests
- Override dependencies in test client
- Isolate test data between tests

## Production Considerations

### Performance
- Add database indexes to frequently queried fields
- Use pagination for list endpoints
- Optimize queries to avoid N+1 problems

### Monitoring
- Log database operations appropriately
- Monitor query performance
- Track error rates and performance metrics

### Migration Strategy
- Plan for schema evolution
- Implement safe migration procedures
- Consider backward compatibility