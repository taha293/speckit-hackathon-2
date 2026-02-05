# Data Model: Backend JWT Authentication API

## Entity Definitions

### User Entity

**Description**: Represents a registered user in the system

**Fields**:
- `id`: UUID (Primary Key)
  - Type: UUID string
  - Constraints: Not null, unique, auto-generated
  - Purpose: Unique identifier for the user

- `email`: VARCHAR(255)
  - Type: String (max 255 characters)
  - Constraints: Not null, unique
  - Purpose: User's email address for login and identification

- `hashed_password`: VARCHAR(255)
  - Type: String (max 255 characters)
  - Constraints: Not null
  - Purpose: BCrypt-hashed password for secure authentication

- `created_at`: DateTime with timezone
  - Type: Timestamp with timezone
  - Constraints: Not null, auto-generated
  - Purpose: Record when the user account was created

- `updated_at`: DateTime with timezone
  - Type: Timestamp with timezone
  - Constraints: Not null, auto-generated/updated
  - Purpose: Record when the user account was last modified

**Relationships**:
- One-to-many relationship with Task entity (one User has many Tasks)

### Task Entity

**Description**: Represents a todo item created by a user

**Fields**:
- `id`: Integer (Primary Key)
  - Type: Auto-incrementing integer
  - Constraints: Not null, unique, auto-generated
  - Purpose: Unique identifier for the task

- `user_id`: UUID (Foreign Key)
  - Type: UUID string
  - Constraints: Not null, references User.id
  - Purpose: Links the task to the user who created it

- `title`: VARCHAR(200)
  - Type: String (1-200 characters)
  - Constraints: Not null
  - Purpose: The title or description of the task

- `description`: TEXT
  - Type: Text (optional)
  - Constraints: Nullable
  - Purpose: Additional details about the task

- `completed`: Boolean
  - Type: Boolean
  - Constraints: Not null, default false
  - Purpose: Whether the task has been completed

- `created_at`: DateTime with timezone
  - Type: Timestamp with timezone
  - Constraints: Not null, auto-generated
  - Purpose: Record when the task was created

- `updated_at`: DateTime with timezone
  - Type: Timestamp with timezone
  - Constraints: Not null, auto-generated/updated
  - Purpose: Record when the task was last modified

**Relationships**:
- Many-to-one relationship with User entity (many Tasks belong to one User)

## Database Schema

### Tables

**users**:
```
id: UUID PRIMARY KEY
email: VARCHAR(255) UNIQUE NOT NULL
hashed_password: VARCHAR(255) NOT NULL
created_at: TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at: TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**tasks**:
```
id: SERIAL PRIMARY KEY
user_id: UUID NOT NULL REFERENCES users(id)
title: VARCHAR(200) NOT NULL
description: TEXT
completed: BOOLEAN NOT NULL DEFAULT FALSE
created_at: TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at: TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

## Indexes

**Primary indexes**:
- users.id (primary key)
- tasks.id (primary key)

**Secondary indexes**:
- users.email (unique index for fast email lookup)
- tasks.user_id (index for filtering tasks by user)
- tasks.completed (index for status queries)

## Validation Rules

### User Validation
- Email format: Must be a valid email address
- Email uniqueness: No duplicate emails allowed
- Password strength: Minimum 8 characters (enforced at registration)
- Email length: Maximum 255 characters

### Task Validation
- Title length: 1-200 characters
- Description length: Maximum 1000 characters
- User ownership: Tasks can only be accessed by their owner
- Completed status: Boolean value (true/false)

## State Transitions

### Task State Transitions
- New task: `completed` = false (default)
- Task completion: `completed` = true (via PUT or PATCH endpoint)
- Task reactivation: `completed` = false (via PUT or PATCH endpoint)

## Relationship Constraints

- Referential Integrity: Tasks cannot exist without a valid user
- Cascade Behavior: Deleting a user deletes all their tasks
- Access Control: Users can only access their own tasks