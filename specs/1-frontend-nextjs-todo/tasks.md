# Tasks: Multi-User Todo Web Application Frontend

**Feature**: Multi-User Todo Web Application Frontend
**Branch**: 1-frontend-nextjs-todo
**Input**: Implementation plan from `/specs/1-frontend-nextjs-todo/plan.md`

## Dependencies

User stories follow priority order from spec with these dependencies:
- User Story 1 (Authentication) must be completed before User Story 2 (Task Management)
- User Story 2 (Task Management) must be completed before User Story 3 (Session Management)
- User Story 3 (Session Management) must be completed before User Story 4 (Responsive UI/Error Handling)

## Parallel Execution Examples

Within each user story phase, tasks can be executed in parallel where they affect different files/components:
- Authentication components and layout components can be developed in parallel
- Task UI components and API client can be developed in parallel
- UI styling and form validation can be developed in parallel

## Implementation Strategy

**MVP First**: Focus on User Story 1 (Authentication) and basic User Story 2 (Task CRUD) to deliver core value quickly.
**Incremental Delivery**: Each user story builds upon the previous one to provide continuous value.

---

## Phase 1: Setup Tasks

- [X] T001 Create project structure in phase2/frontend with Next.js 16
- [X] T002 Initialize package.json with Next.js 16, React 18, Better Auth, Tailwind CSS dependencies
- [X] T003 Set up TypeScript configuration (tsconfig.json) with proper Next.js settings
- [X] T004 Configure Tailwind CSS with proper Next.js integration
- [X] T005 Create .env.example file with required environment variables
- [X] T006 Set up basic Next.js configuration (next.config.js)
- [X] T007 Create initial directory structure (app/, components/, lib/, hooks/, types/, public/)

---

## Phase 2: Foundational Tasks

- [X] T008 Create API client in lib/api.ts with JWT token handling
- [X] T009 Create type definitions for User, Task, Session in types/ directory
- [X] T010 Implement centralized toast notifications component
- [X] T011 Set up basic error handling utilities in lib/utils.ts
- [X] T012 Create authentication utilities in lib/auth.ts for Better Auth integration
- [X] T013 Set up basic hooks for authentication and tasks in hooks/ directory
- [X] T014 [P] Implement standard security controls (password complexity, session timeouts, rate limiting)
- [X] T015 [P] Implement robust backend API integration with retry mechanisms and comprehensive error handling
- [X] T016 [P] Implement basic offline functionality allowing users to view and edit tasks with synchronization
- [X] T017 [P] Implement last-write-wins data synchronization strategy with user notifications

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1)

**Goal**: A new user visits the application and needs to create an account, then log in to access their todo list. The user should be able to register with email/password, securely log in, and be redirected to their dashboard.

**Independent Test**: The registration and login flow can be tested independently by registering a new user, logging in, and verifying access to the dashboard. The flow delivers core value by enabling personalized todo management.

**Acceptance Scenarios**:
1. **Given** a user is on the signup page, **When** they enter valid email and password and click signup, **Then** they should be registered and automatically logged in
2. **Given** a user has an account, **When** they visit the login page and enter valid credentials, **Then** they should be authenticated and redirected to their dashboard
3. **Given** a user enters invalid credentials, **When** they attempt to log in, **Then** they should see an error message with feedback

- [X] T014 [P] [US1] Create login page component in app/login/page.tsx
- [X] T015 [P] [US1] Create signup page component in app/signup/page.tsx
- [X] T016 [P] [US1] Implement email/password login form with validation
- [X] T017 [P] [US1] Implement email/password signup form with validation
- [X] T018 [P] [US1] Create authentication API integration for login endpoint
- [X] T019 [P] [US1] Create authentication API integration for signup endpoint
- [X] T020 [US1] Set up JWT token management with Better Auth
- [X] T021 [US1] Implement redirect to dashboard after successful login/signup
- [X] T022 [US1] Handle authentication errors and display toast notifications
- [X] T023 [US1] Create "Don't have an account?" / "Already have an account?" links between pages
- [X] T024 [US1] Style login/signup pages with Tailwind CSS

---

## Phase 4: User Story 2 - Task Management Dashboard (Priority: P1)

**Goal**: An authenticated user needs to view, create, update, and delete their tasks on a responsive dashboard. The user should see their tasks with ability to mark as complete, edit details, and delete unwanted tasks.

**Independent Test**: The task management features can be tested independently by creating tasks, updating them, marking them as complete, and deleting them. The dashboard delivers value by providing a central place to manage todos.

**Acceptance Scenarios**:
1. **Given** a user is logged in and on the dashboard, **When** they create a new task, **Then** the task should appear in their list with correct details
2. **Given** a user has existing tasks, **When** they toggle the completion status of a task, **Then** the change should be reflected in the UI and persisted to the backend
3. **Given** a user wants to edit a task, **When** they modify the task details, **Then** the changes should be saved and updated in the UI
4. **Given** a user wants to remove a task, **When** they confirm deletion, **Then** the task should be removed from the list and backend

- [X] T025 [P] [US2] Create dashboard page component in app/page.tsx - FIX: Prevent API requests when not logged in
- [X] T026 [P] [US2] Create task card component in components/tasks/task-card.tsx
- [X] T027 [P] [US2] Create task list component in components/tasks/task-list.tsx
- [X] T028 [P] [US2] Create task creation form component in components/tasks/task-form.tsx - FIX: Remove date option since backend doesn't support due dates
- [X] T029 [P] [US2] Implement task creation API integration
- [X] T030 [P] [US2] Implement task retrieval API integration
- [X] T031 [P] [US2] Implement task update API integration
- [X] T032 [P] [US2] Implement task deletion API integration
- [X] T033 [US2] Display tasks with title, status, creation date, completion toggle, edit and delete options
- [X] T034 [US2] Implement toggle task completion functionality with immediate visual feedback - FIX: Use correct API endpoint according to backend README.md (PATCH /api/v1/tasks/{id}/complete)
- [X] T035 [US2] Implement task editing functionality (modal or inline editing) - ADD: Update option for tasks
- [X] T036 [US2] Implement task deletion with confirmation modal
- [X] T037 [US2] Show loading states and skeleton screens during API calls
- [X] T038 [US2] Show toast notifications for task operations success/error - FIX: Show user-friendly messages instead of HTTP status codes

---

## Phase 5: User Story 3 - Session Management and Security (Priority: P2)

**Goal**: An authenticated user should have their session maintained across browser sessions and be gracefully redirected to login when their JWT token expires.

**Independent Test**: The session management can be tested by maintaining a login session, allowing token expiration, and verifying graceful re-authentication. The feature delivers value by maintaining security while providing good UX.

**Acceptance Scenarios**:
1. **Given** a user is logged in, **When** they refresh the page, **Then** they should remain authenticated
2. **Given** a user's JWT token has expired, **When** they try to access protected resources, **Then** they should be redirected to the login page with a clear message
3. **Given** a user is actively using the app, **When** their token is near expiration, **Then** the system should attempt to refresh the token seamlessly

- [X] T039 [P] [US3] Implement session validation utilities in lib/auth.ts
- [X] T040 [P] [US3] Create protected route component for checking authentication
- [X] T041 [P] [US3] Implement token expiration handling with redirect to login
- [X] T042 [P] [US3] Create API error interceptor to handle 401 responses
- [X] T043 [US3] Implement token refresh mechanism when approaching expiration
- [X] T044 [US3] Set up persistent session storage with Better Auth
- [X] T045 [US3] Create session context for managing authentication state
- [X] T046 [US3] Implement auto-refresh or re-login flow on token expiration
- [X] T047 [US3] Create middleware for protecting routes that require authentication

---

## Phase 6: User Story 4 - Responsive UI and Error Handling (Priority: P3)

**Goal**: Users should have a consistent, responsive experience across devices with clear feedback for all actions and errors.

**Independent Test**: The UI can be tested independently by accessing the application on different device sizes and triggering various error conditions to verify proper feedback.

**Acceptance Scenarios**:
1. **Given** a user is on mobile device, **When** they interact with the application, **Then** the UI should adapt appropriately to the smaller screen
2. **Given** an API call fails, **When** the user performs an action, **Then** they should see a toast notification with clear error information
3. **Given** the user performs a successful action, **When** the operation completes, **Then** they should see a toast notification confirming success

- [X] T048 [P] [US4] Create responsive layout components in components/layout/
- [X] T049 [P] [US4] Implement mobile-first responsive design with Tailwind CSS
- [X] T050 [P] [US4] Create 404 page component in app/not-found.tsx
- [X] T051 [P] [US4] Implement form validation with proper error feedback
- [X] T052 [P] [US4] Create reusable UI components (buttons, inputs, modals) in components/ui/
- [X] T053 [US4] Implement comprehensive error handling for all API operations
- [X] T054 [US4] Add smooth transitions and hover effects for modern feel
- [X] T055 [US4] Ensure proper ARIA labels and keyboard navigation support
- [X] T056 [US4] Add accessibility features to all interactive components
- [X] T057 [US4] Implement offline capability with service workers and local storage
- [X] T058 [US4] Add loading spinners and skeleton screens for better UX

---

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T059 Implement comprehensive error boundaries for React components
- [X] T060 Add performance optimizations (memoization, code splitting) to achieve page load under 2 seconds
- [X] T061 Create comprehensive testing setup (Jest, React Testing Library)
- [X] T062 Add security headers and best practices implementation
- [X] T063 Implement comprehensive logging for debugging
- [X] T064 Create README with setup instructions and project overview
- [X] T065 Conduct final testing across different browsers and devices
- [X] T066 Perform accessibility audit and fix issues
- [X] T067 Optimize images and assets for web delivery
- [X] T068 Final review and documentation of the implementation
- [X] T069 Ensure API responses complete under 500ms for 95% of requests
- [X] T070 Implement performance monitoring to support up to 100 concurrent users
- [X] T071 Verify registration and login flows complete in under 60 seconds
- [X] T072 Confirm CRUD operations on tasks complete within 3 seconds with immediate visual feedback

---

## Phase 8: Bug Fixes and Improvements (2026-02-06)

**Context**: Issues identified during implementation review that need to be addressed.

- [X] T073 [US2] Fix homepage to prevent API requests when user is not logged in at phase2/frontend/app/page.tsx
- [X] T074 [US2] Fix toaster to display user-friendly error messages instead of HTTP status codes in phase2/frontend/lib/api.ts
- [X] T075 [US2] Fix mark complete API call to use correct endpoint (PATCH /api/v1/tasks/{id}/complete) per backend README.md in phase2/frontend/lib/api.ts
- [X] T076 [US2] Add update/edit functionality for tasks in phase2/frontend/components/tasks/task-card.tsx
- [X] T077 [US2] Remove date/due date option from task form since backend doesn't support it in phase2/frontend/components/tasks/task-form.tsx
- [X] T078 [US2] Replace simple "Loading..." text with interactive loading spinner/skeleton UI in phase2/frontend/app/page.tsx
- [X] T079 [US2] Improve redirect behavior when not logged in - replace text-only message with proper loading UI in phase2/frontend/app/page.tsx

## Phase 9: Additional Bug Fixes (2026-02-07)

**Context**: Additional issues discovered during testing that need to be addressed.

- [X] T080 [US2] Fix toggle complete endpoint to use query parameter (?completed=true) instead of request body in phase2/frontend/lib/api.ts
- [X] T081 [US2] Remove dueDate from Task and TaskInput type definitions in phase2/frontend/types/tasks.ts
- [X] T082 [US2] Add authentication check in useTasks hook to prevent API calls when not logged in in phase2/frontend/hooks/useTasks.ts
- [X] T083 [US2] Prevent repeated API calls on tab switch by adding hasFetched state in phase2/frontend/hooks/useTasks.ts
- [X] T084 [US2] Pass authentication state to useTasks hook to ensure proper authentication checks in phase2/frontend/app/page.tsx
- [X] T085 [US2] Fix 307 redirects by adding trailing slashes to task API endpoints in phase2/frontend/lib/api.ts