# FastAPI Builder Skill

A comprehensive FastAPI application builder skill that helps create production-ready FastAPI applications with database integration, authentication, and CRUD operations.

## Overview

This skill provides:

- **Model Generation**: Create SQLModel/Pydantic models with proper validation
- **CRUD Operations**: Full Create, Read, Update, Delete endpoints
- **Authentication**: JWT token authentication with OAuth2
- **Database Integration**: SQLModel with SQLite/PostgreSQL setup
- **Project Scaffolding**: Complete project structure with best practices
- **Security Features**: Password hashing, input validation, and secure practices

## Installation

The skill is ready to use once installed in your Claude Code environment. All necessary references and templates are included.

## Usage

### Quick Start

To create a new FastAPI application:

```
"Create a FastAPI app with User model and CRUD operations"
```

To add authentication to an existing API:

```
"Add JWT authentication to my FastAPI app"
```

To create database models:

```
"Generate SQLModel for a Product with name, price, and category"
```

### Model Creation

The skill follows SQLModel best practices:
- Base models for common fields
- Create models for POST requests
- Update models for PATCH requests
- Public models for responses

### Authentication System

The skill implements:
- OAuth2 password flow
- JWT token creation and validation
- Password hashing with Argon2
- Current user dependencies

### Database Integration

The skill includes:
- SQLModel configuration
- Session management
- Connection pooling
- Relationship handling

## Key Features

### 1. Model Generation
- Base, Create, Update, and Public model patterns
- Field validation and constraints
- Relationship support

### 2. CRUD Operations
- Complete REST API endpoints
- Proper response models
- Error handling
- Pagination support

### 3. Authentication
- JWT token system
- User registration/login
- Protected endpoints
- Role-based access control

### 4. Project Structure
- Organized directory structure
- Configuration management
- Environment variables
- Testing setup

## References Included

- `models.md`: SQLModel patterns and validation
- `crud.md`: CRUD operation implementations
- `auth.md`: Authentication and security
- `database.md`: Database integration patterns

## Assets Included

- `model-template.py`: Template for new models
- `auth-template.py`: Authentication system template
- `requirements.txt`: Production-ready dependencies
- `init-fastapi-project.py`: Project scaffolding script

## Best Practices

The skill implements FastAPI best practices:
- Dependency injection
- Type hints and validation
- Proper error handling
- Security measures
- Testing patterns
- Documentation generation

## Contributing

This skill is designed to evolve with FastAPI best practices. Contributions are welcome for:
- New template additions
- Updated security patterns
- Performance optimizations
- Additional database integrations