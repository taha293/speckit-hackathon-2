# Better Auth Integration Research

## Better Auth Overview

Better Auth is a framework-agnostic authentication and authorization library for TypeScript that provides:

- Email/password authentication
- Social provider integration (Google, GitHub, etc.)
- Multi-session management
- Secure session handling
- Database integration (PostgreSQL, MySQL, SQLite, MongoDB, Prisma, Drizzle)
- Extensible plugin system
- Framework integration (Next.js, Express, etc.)

## Why Better Auth URLs in Environment Variables

The Better Auth URLs need to be in environment variables for several reasons:

### NEXT_PUBLIC_BETTER_AUTH_URL
- Used by the frontend client to communicate with the Better Auth API
- Needs to be accessible to the browser/client-side code
- Typically points to the deployed API endpoint (e.g., https://api.yourapp.com/auth)

### BETTER_AUTH_URL
- Used server-side for internal communication
- Points to the internal Better Auth endpoint
- May be different from the public URL in containerized environments

### BETTER_AUTH_SECRET
- Secret key used to sign JWTs and secure the authentication system
- Must never be exposed to the client
- Should be a strong random string

## Integration Strategy

### Server-Side Setup (auth.ts)
```typescript
import { betterAuth } from "better-auth";
import { nextJs } from "@better-auth/next-js";

// Database adapter would be configured based on project requirements
export const auth = betterAuth({
  database: {
    // Database configuration based on selected adapter
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },
  socialProviders: {
    // GitHub, Google, etc. if needed
  },
});

export const {
  get session,
  signIn,
  signOut,
  signUp,
  updateSession,
} = nextJs(auth);
```

### Client-Side Setup (auth-client.ts)
```typescript
import { createAuthClient } from "better-auth/client";
import { nextClient } from "@better-auth/next-js/client";

export const {
  signOut,
  useSession,
  signIn,
  signUp,
  getClientSession,
} = nextClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000/api/auth",
});
```

### Next.js Middleware for Route Protection
```typescript
import { auth } from "@/lib/auth";

export default auth();

export const config = {
  matcher: ["/dashboard/:path*", "/api/auth/:path*"],
};
```

## Required Environment Variables

```env
# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth  # Public URL for client-side
BETTER_AUTH_URL=http://localhost:3000/api/auth           # Server-side URL
BETTER_AUTH_SECRET=your-super-secret-string-that-is-at-least-32-characters-long

# Database Configuration (based on selected adapter)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## Benefits of Using Better Auth

1. **Simplified Implementation**: Reduces boilerplate code for authentication
2. **Security**: Built-in security best practices (CSRF protection, secure cookies, etc.)
3. **Flexibility**: Supports multiple database adapters and authentication methods
4. **Type Safety**: Full TypeScript support
5. **Framework Agnostic**: Can work with Next.js, Express, etc.
6. **Plugin System**: Extensible functionality for admin panels, 2FA, etc.