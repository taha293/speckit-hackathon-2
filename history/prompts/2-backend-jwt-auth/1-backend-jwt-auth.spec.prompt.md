---
id: 1
title: "Backend JWT Authentication API Spec"
stage: spec
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-jwt-auth
branch: 2-backend-jwt-auth
user: cash
command: "/sp.specify"
labels: ["backend", "jwt", "authentication", "api", "security"]
spec: "specs/2-backend-jwt-auth/spec.md"
ticket: null
adr: null
pr: null
files:
  - "specs/2-backend-jwt-auth/spec.md"
  - "specs/2-backend-jwt-auth/checklists/requirements.md"
  - "history/prompts/2-backend-jwt-auth/1-backend-jwt-auth.spec.prompt.md"
tests: []
outcome: "Successfully created specification for backend JWT authentication API with proper user scenarios, functional requirements, and success criteria."
evaluation: "Specification follows template structure, includes prioritized user stories, clear functional requirements with identifiers, and measurable success criteria."
---

# Backend JWT Authentication API Specification

## User Input

```
PHASE II — BACKEND SPECIFICATION (FASTAPI)

Objective
Implement a secure, production-ready backend for a multi-user Todo web application. The backend must expose RESTful APIs, enforce authentication using JWT, persist data in PostgreSQL, and strictly isolate user data. All implementation must be performed by Claude Code using this specification as the source of truth.

Technology Stack
- Python FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL
- JWT-based authentication (tokens issued by Better Auth on frontend)

────────────────────────────────────────
CORE RESPONSIBILITIES
────────────────────────────────────────

1. Expose RESTful APIs for task management
2. Verify and enforce user authentication using JWT
3. Persist and query data from PostgreSQL
4. Enforce strict per-user data isolation
5. Return consistent JSON responses and proper HTTP status codes

────────────────────────────────────────
AUTHENTICATION & SECURITY
────────────────────────────────────────

JWT Verification
- Every API request must include a JWT token in the Authorization header
  Authorization: Bearer <token>
- Backend must verify the JWT signature using a shared secret
- JWT verification must occur before request handling
- Invalid or missing token must return 401 Unauthorized

User Identity Extraction
- Backend must decode the JWT token to extract:
  - user_id
  - email
- Backend must treat JWT data as the single source of user identity

Authorization Rules
- user_id extracted from JWT must match user_id provided in request path
- Mismatch must return 403 Forbidden
- Backend must never trust client-provided user_id without JWT verification

Token Properties
- JWT must support expiration
- Expired tokens must be rejected automatically

────────────────────────────────────────
API ENDPOINTS
────────────────────────────────────────

All endpoints require a valid JWT token.

GET /api/{user_id}/tasks
- Return all tasks belonging to the authenticated user
- Must filter tasks by user_id from JWT
- Response: list of task objects

POST /api/{user_id}/tasks
- Create a new task for the authenticated user
- Request body:
  - title (required, 1–200 chars)
  - description (optional, max 1000 chars)
- Response: created task object

GET /api/{user_id}/tasks/{task_id}
- Return task details if task belongs to user
- If task not found or not owned by user, return 404

PUT /api/{user_id}/tasks/{task_id}
- Update task title, description, or completed status
- Only allowed if task belongs to authenticated user
- Response: updated task object

DELETE /api/{user_id}/tasks/{task_id}
- Delete task owned by authenticated user
- Response: success confirmation

PATCH /api/{user_id}/tasks/{task_id}/complete
- Toggle completed status of task
- Only allowed if task belongs to authenticated user
- Response: updated task object

────────────────────────────────────────
DATA MODEL REQUIREMENTS
────────────────────────────────────────

User
- Managed externally by Better Auth
- Fields used by backend:
  - id (string)
  - email (string)

Task
- id: integer (primary key)
- user_id: string (foreign key reference to user)
- title: string (not null)
- description: text (nullable)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp

Indexes
- Index on user_id for fast filtering
- Index on completed for status queries

────────────────────────────────────────
DATABASE BEHAVIOR
────────────────────────────────────────

- All database operations must use SQLModel
- Database connection string must be loaded from environment variables
- Queries must always be filtered by authenticated user_id
- Backend must never return tasks belonging to another user

────────────────────────────────────────
ERROR HANDLING
────────────────────────────────────────

- 401 Unauthorized: missing or invalid JWT
- 403 Forbidden: user_id mismatch or unauthorized access
- 404 Not Found: task does not exist or not owned by user
- 422 Validation Error: invalid request data
- Errors must return JSON responses with clear messages

────────────────────────────────────────
IMPLEMENTATION RULES
────────────────────────────────────────

- This specification is the single source of truth
- Claude Code must read and follow this spec before implementation
- No manual code edits are permitted
- Any behavior change must be reflected in this spec first

────────────────────────────────────────
SUCCESS CRITERIA
────────────────────────────────────────

- All endpoints require JWT authentication
- User identity is derived exclusively from JWT
- Tasks are fully isolated per user
- CRUD operations function correctly
- Database persistence works across restarts
- Backend is secure, stateless, and production-ready

────────────────────────────────────────
Folder Structure
────────────────────────────────────────

-Root/Backend (All work here in Backend Folder)

────────────────────────────────────────
Code
────────────────────────────────────────

-Code Should be simple and easy to understand even for beginner



END OF PHASE II BACKEND SPEC
```

## Response Summary

Successfully created a comprehensive feature specification for the backend JWT authentication API following the required template structure. The specification includes:

1. **Prioritized User Stories**:
   - P1: Secure Task Management
   - P1: Authentication Enforcement
   - P2: Data Isolation

2. **Functional Requirements** with unique identifiers (FR-001 through FR-009)

3. **Key Entities** (Task and User)

4. **Measurable Success Criteria** (SC-001 through SC-004)

5. **Edge Cases** covering token expiration, concurrency, and error handling

The specification adheres to the template requirements and focuses on user value and business needs without implementation details. All mandatory sections are completed and the specification is ready for the planning phase.

## Files Created/Modified
- `specs/2-backend-jwt-auth/spec.md`: Main specification document
- `specs/2-backend-jwt-auth/checklists/requirements.md`: Quality validation checklist
- `history/prompts/2-backend-jwt-auth/1-backend-jwt-auth.spec.prompt.md`: This PHR record