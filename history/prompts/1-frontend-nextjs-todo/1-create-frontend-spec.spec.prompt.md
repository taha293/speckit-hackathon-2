---
id: 1
title: create-frontend-spec
stage: spec
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: frontend-nextjs-todo
branch: 1-frontend-nextjs-todo
user: user
command: /sp.specify
labels: [frontend, authentication, todo-app, nextjs]
links:
  spec: specs/1-frontend-nextjs-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-frontend-nextjs-todo/spec.md
  - specs/1-frontend-nextjs-todo/checklists/requirements.md
tests:
  - validation of spec against template requirements
---

## Prompt

```
PHASE II — FRONTEND SPECIFICATION (NEXT.JS 16)

Objective
Implement a modern, responsive, full-featured frontend for the multi-user Todo web application using Next.js 16 App Router. All frontend work must be contained within Root/phase2/frontend. Use Better Auth for authentication and Claude skills first for implementation. All API calls must integrate with backend as described in Root/backend/README.md. Manual coding outside this folder is prohibited.

────────────────────────────────────────
Restrictons
────────────────────────────────────────

- All work in Root(the folder we are one)/phase2/frontend

────────────────────────────────────────
AUTHENTICATION
────────────────────────────────────────

Login / Signup
- Use Better Auth for email/password authentication
- On login, Better Auth must request JWT token from backend
- JWT token must be attached automatically to all API requests via Authorization header
- Handle token expiry gracefully, redirect to login if expired
- Use Claude skills for implementation wherever available

Session Management
- Persist session in local storage or secure cookie as required by Better Auth
- Auto-refresh or re-login flow if token expires

────────────────────────────────────────
API INTEGRATION
────────────────────────────────────────

- Fetch backend API details from Root/backend/README.md
- All API calls must use a centralized API client (`lib/api.ts`)
- API client must automatically attach JWT token to Authorization header
- Handle errors with proper user feedback via toast notifications
- All CRUD operations (tasks) must be fully functional and integrated with backend

Endpoints (derived from backend spec)
- All mentioned in root(the older we are on)/phase2/backend.readme.md

────────────────────────────────────────
PAGES & ROUTES
────────────────────────────────────────

Homepage (`/`)
- Modern dashboard style with task list overview
- Create new task UI component
- Task items show title, status, creation date, completion toggle, edit and delete options
- Responsive layout for desktop and mobile
- Smooth interactions with toast notifications for success/error

Login Page (`/login`)
- Modern clean UI
- Email/password input
- Login button
- Link to signup page
- Error messages displayed via toast

Signup Page (`/signup`)
- Modern clean UI
- Email/password inputs
- Signup button
- Auto-login after successful signup

404 Page (`/notfound`)
- Modern responsive design
- Clear "Page Not Found" message
- Link back to homepage
- Use modern visuals (iconography or minimal illustration)

Other Pages
- Task management page (can be part of homepage or `/tasks`)
- User profile or settings optional but must follow modern design if included

────────────────────────────────────────
UI COMPONENTS
────────────────────────────────────────

- Use Tailwind CSS for styling, no inline styles
- Use reusable components for buttons, inputs, modals, task cards, toast notifications
- All components must be responsive
- Use server components for static parts, client components for interactivity
- Toast notifications for: success, error, info
- Loading spinners or skeletons for API calls

────────────────────────────────────────
INTERACTIVITY & UX
────────────────────────────────────────

- Task creation/editing via form modal or inline editing
- Delete confirmation modal before task deletion
- Toggle task complete with immediate visual feedback
- Smooth transitions and hover effects for modern feel
- Mobile-first responsive layout
- Accessibility: proper ARIA labels, keyboard navigation support

────────────────────────────────────────
ERROR HANDLING
────────────────────────────────────────

- Login errors (invalid credentials, backend issues) → show toast
- API errors → show toast with message
- Page not found → redirect to `/notfound` if invalid route
- Form validation: required fields, max lengths, proper feedback

────────────────────────────────────────
CLAUDE SKILLS USAGE
────────────────────────────────────────

- Use Claude skills to implement components first if available
- Reference backend API from Root/backend/README.md
- No hallucinated API or features
- UI design follows modern responsive standards
- Toasts, modals, and interactivity use Claude-first implementation whenever possible

────────────────────────────────────────
SUCCESS CRITERIA
────────────────────────────────────────

- Fully functional login/signup flow with JWT
- All CRUD operations work with backend
- Task ownership enforced by backend via JWT token
- Homepage dashboard shows tasks with interactive UI
- Responsive design works on desktop and mobile
- Modern, visually appealing 404 page implemented
- Toast notifications for all user actions and errors
- Frontend contained entirely within Root/phase2/frontend
- Claude skills used wherever possible

END OF PHASE II FRONTEND SPEC
```

## Response snapshot

Successfully created the feature specification for the multi-user Todo web application frontend. The specification includes:

- Four prioritized user stories covering authentication, task management, session management, and responsive UI
- 14 functional requirements (FR-001 through FR-014) addressing authentication, task operations, API integration, and UI components
- Key entities defined (User, Task, Session)
- 8 measurable success criteria (SC-001 through SC-008) covering performance, usability, and integration

The specification adheres to the requirements by focusing on user value and business needs while avoiding implementation-specific details. Created corresponding quality checklist at specs/1-frontend-nextjs-todo/checklists/requirements.md to validate all requirements are met.

## Outcome

- ✅ Impact: Complete feature specification created for frontend implementation
- 🧪 Tests: Specification validated against template requirements with checklist
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Successfully abstracted technical requirements into user-focused specification

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin architectural planning