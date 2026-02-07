# Quickstart Guide: Multi-User Todo Web Application Frontend

## Prerequisites

- Node.js 18+ with npm/yarn
- Git
- Access to backend API (refer to `Root/backend/README.md` for backend setup)
- Better Auth account (if using hosted version)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd phase2/frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables
Create a `.env.local` file in the frontend directory:

```env
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1  # Adjust to your backend URL

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth  # Public URL for client-side auth
BETTER_AUTH_URL=http://localhost:3000/api/auth            # Server-side URL for auth
BETTER_AUTH_SECRET=your-super-secret-string-that-is-at-least-32-characters-long  # Secret key for auth

# Database Configuration (Choose based on your database setup)
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp  # PostgreSQL example
# MYSQL_URL=mysql://user:password@localhost:3306/todoapp        # MySQL example (if using MySQL)

# Additional Configuration (if needed)
JWT_EXPIRY_TIME=2h                                   # Token expiry duration
```

### 4. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Project Structure

```
phase2/frontend/
├── app/                        # Next.js 16 App Router pages and layouts
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Homepage/dashboard
│   ├── login/page.tsx          # Login page
│   ├── signup/page.tsx         # Signup page
│   ├── not-found.tsx           # 404 page
│   ├── globals.css             # Global styles
│   ├── middleware.ts           # Next.js middleware for auth protection
│   └── [...all]/page.tsx       # Catch-all route for 404 handling
├── components/                 # Reusable UI components
│   ├── ui/                     # Base components (buttons, inputs, etc.)
│   ├── auth/                   # Authentication components
│   ├── tasks/                  # Task management components
│   ├── layout/                 # Layout components
│   └── notifications/          # Toast notifications
├── lib/                        # Utility functions and API client
│   ├── auth.ts                 # Better Auth server-side configuration for JWT management
│   ├── auth-client.ts          # Better Auth client-side configuration for session state
│   ├── api.ts                  # Centralized API client with JWT handling
│   └── utils.ts                # General utilities
├── hooks/                      # Custom React hooks
│   ├── useAuth.ts              # Authentication state management
│   └── useTasks.ts             # Task data management
├── types/                      # TypeScript type definitions
│   ├── auth.ts                 # Authentication types
│   └── tasks.ts                # Task-related types
├── public/                     # Static assets
├── .env.example                # Environment variables template
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies and scripts
```

## Key Features Implementation

### 1. Authentication Flow
- User registration with email/password
- Login/logout functionality
- Automatic JWT token management
- Session persistence

### 2. Task Management
- Create, read, update, delete tasks
- Toggle task completion status
- View task details and edit functionality
- Responsive dashboard layout

### 3. Error Handling
- Toast notifications for success/error/info
- Proper form validation
- Network error handling
- Graceful degradation for offline scenarios

### 4. Better Auth Integration
- JWT token management (storage, refresh, and expiration handling) for tokens issued by backend
- Automatic token attachment to backend API requests
- Session state management in the frontend
- Protected routes using Next.js middleware
- Secure token storage and transmission

## API Integration

The frontend communicates with the backend for all authentication and task data operations via the centralized API client at `lib/api.ts`, with Better Auth managing JWT tokens:

- Backend handles user authentication (login/signup) and issues JWT tokens
- Better Auth manages JWT token storage, refresh, and expiration
- API client automatically attaches JWT tokens from Better Auth to backend requests
- Handles authentication errors and redirects to login when needed
- Provides consistent error response format
- Implements retry mechanisms for failed requests

## Development Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run linting
- `npm run test` - Run tests (if configured)

## Testing

Unit tests for components can be added in corresponding `__tests__` folders alongside components.
Integration tests should verify API integration and authentication flow.

## Deployment

1. Build the application: `npm run build`
2. The build output will be in the `.next` directory
3. Serve the build with a Node.js server or deploy to a platform like Vercel, Netlify, or AWS

For production deployment, ensure all environment variables are properly configured for the target environment.