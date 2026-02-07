# Todo Application Frontend

A modern, responsive, full-featured frontend for the multi-user Todo web application using Next.js 16 App Router with Better Auth for JWT token management.

## Features

- User registration and authentication with email/password
- Secure JWT token management via Better Auth
- Task management (Create, Read, Update, Delete)
- Responsive design for desktop and mobile
- Toast notifications for user feedback
- Form validation and error handling
- Protected routes and session management

## Tech Stack

- Next.js 16 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Better Auth
- @better-auth/next-js

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Access to backend API (see backend documentation)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phase2/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Copy environment variables:
```bash
cp .env.example .env.local
```

4. Update `.env.local` with your configuration:
```env
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_SECRET=your-super-secret-string-that-is-at-least-32-characters-long

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp
```

### Running the Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

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
├── contexts/                   # React context providers
│   └── SessionContext.tsx      # Session state management
├── public/                     # Static assets
├── .env.example                # Environment variables template
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies and scripts
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run linting

## API Integration

The frontend communicates with the backend for all authentication and task data operations via the centralized API client at `lib/api.ts`, with Better Auth managing JWT tokens:

- Backend handles user authentication (login/signup) and issues JWT tokens
- Better Auth manages JWT token storage, refresh, and expiration
- API client automatically attaches JWT tokens from Better Auth to backend requests
- Handles authentication errors and redirects to login when needed

## Security

- Secure JWT token storage and transmission
- Protected routes using Next.js middleware
- Input validation and sanitization
- CSRF protection via Better Auth

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request
