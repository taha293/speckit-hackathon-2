# Data Model: Multi-User Todo Web Application Frontend

## Core Entities

### User
Represents a registered user with authentication details and owns todo tasks.

**Fields**:
- `id`: Unique identifier for the user (string/UUID)
- `email`: User's email address for authentication (string, required, unique)
- `name`: User's display name (string, optional)
- `createdAt`: Timestamp of account creation (DateTime)
- `updatedAt`: Timestamp of last account update (DateTime)

**Validation**:
- Email must be a valid email format
- Email must be unique across all users
- Required fields must be present

### Task
Represents a todo item with title, description, status (completed/incomplete), creation date, and ownership tied to a User.

**Fields**:
- `id`: Unique identifier for the task (string/UUID)
- `title`: Task title or description (string, required, max 200 characters)
- `description`: Optional detailed description (string, optional, max 1000 characters)
- `completed`: Status indicating completion (boolean, default: false)
- `createdAt`: Timestamp of task creation (DateTime)
- `updatedAt`: Timestamp of last task update (DateTime)
- `userId`: Foreign key linking to the owning user (string/UUID, required)
- `dueDate`: Optional due date for the task (DateTime, optional)

**Validation**:
- Title must be between 1-200 characters
- Description (if provided) must be under 1000 characters
- Completed field must be boolean
- UserId must reference an existing user
- Due date must be a valid future date if provided

### Session
Represents an authenticated user session where JWT tokens issued by backend are managed by Better Auth.

**Fields**:
- `token`: JWT authentication token issued by backend and managed by Better Auth (string, required)
- `userId`: Associated user identifier from backend system (string/UUID, required)
- `expiresAt`: Token expiration timestamp (DateTime)
- `createdAt`: Session creation timestamp (DateTime)
- `refreshToken`: Optional refresh token issued by backend (string, optional)
- `sessionId`: Internal session identifier from Better Auth (string, required)

**Validation**:
- Token must be a valid JWT format issued by backend system
- Expiration must be in the future
- UserId must reference an existing user in the backend system
- SessionId must be valid and active in Better Auth system

## Relationships

### User → Task
- **Relationship**: One-to-Many (One user can have many tasks)
- **Cardinality**: 1:M
- **Constraint**: Cascade delete (when user is deleted, all their tasks are deleted)
- **Foreign Key**: Task.userId → User.id

### Session → User
- **Relationship**: Many-to-One (Many sessions can be associated with one user over time)
- **Cardinality**: M:1
- **Constraint**: Session userId must reference an existing user
- **Foreign Key**: Session.userId → User.id

## Data Operations

### Task Operations
- **Create**: Requires title and userId; generates ID and timestamps
- **Read**: Filter by userId to ensure users only see their own tasks
- **Update**: Allows modification of title, description, completed status, dueDate
- **Delete**: Removes task from database

### Session Operations
- **Create**: Generated on successful authentication with token and expiration
- **Validate**: Check token validity and expiration status
- **Refresh**: Obtain new token before expiration
- **Destroy**: Invalidate session on logout

## State Transitions

### Task Status Transition
- **Active** ↔ **Completed**: User can toggle completed status
- **Validations**: Creation date remains unchanged, updated date updates on any change

### Session State
- **Active** → **Expired**: Automatically transitions when token expires
- **Active** → **Inactive**: Occurs on logout or token invalidation
- **Inactive** → **Active**: Only possible through new authentication flow

## Data Integrity Rules

### Ownership Enforcement
- Users can only view, edit, or delete their own tasks
- Backend API enforces ownership via JWT token validation
- Frontend displays only tasks belonging to authenticated user

### Validation Enforcement
- All data must pass validation before storage
- Backend validation serves as final authority
- Frontend validation provides user experience improvements

## Storage Patterns

### Client-Side Storage
- Sessions stored in secure cookies or localStorage (as per Better Auth configuration)
- Temporary state cached in React component state and Context API
- Offline data stored in browser's IndexedDB when available

### Server-Side Storage
- Primary data stored in backend database (referenced in backend documentation)
- JWT tokens validated against backend user records
- All CRUD operations coordinated through backend API