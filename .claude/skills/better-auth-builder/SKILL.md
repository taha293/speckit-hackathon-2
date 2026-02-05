---
name: better-auth-builder
description: |
  This skill should be used when users need to implement authentication using Better Auth.
  Helps set up authentication systems with email/password, social providers, database integration,
  plugins, and framework integration.
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Better Auth Builder

This skill creates comprehensive authentication setups using Better Auth, a framework-agnostic authentication and authorization library for TypeScript. It handles installation, configuration, database setup, social providers, plugins, and framework integration.

## What This Skill Does

- Sets up Better Auth with various database adapters (PostgreSQL, MySQL, SQLite, MongoDB, Prisma, Drizzle)
- Configures email/password authentication
- Integrates social login providers (GitHub, Google, etc.)
- Adds authentication plugins (Admin, 2FA, Username)
- Creates middleware for route protection
- Sets up client-side integration for React/Next.js
- Implements security best practices

## What This Skill Does NOT Do

- Test authentication flows in production environments
- Deploy authentication systems to hosting platforms
- Manage OAuth credentials or secrets
- Handle UI/UX design beyond authentication components

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Framework type (Next.js, Express, etc.), existing database setup, project structure |
| **Conversation** | User's specific authentication requirements, social providers needed, plugin requirements |
| **Skill References** | Database adapters, security configurations, framework integration patterns |
| **User Guidelines** | Project-specific conventions, security requirements, team standards |

Ensure all required context is gathered before implementing.

---

## Clarifications

Before implementing, I need to understand:

**1. Target Framework** - "Which framework are you using?"
- Next.js App Router (most common)
- Express.js server
- Other (specify)

**2. Database Setup** - "What database are you currently using or planning to use?"
- PostgreSQL with direct connection
- MySQL with direct connection
- SQLite with direct connection
- MongoDB with adapter
- Prisma ORM
- Drizzle ORM
- Other (specify)

**3. Authentication Methods** - "Which authentication methods do you need?"
- Email and password only
- Social providers only (GitHub, Google, etc.)
- Both email/password and social providers

**4. Plugin Requirements** - "Do you need any authentication plugins?"
- None (basic setup)
- Admin panel plugin
- Two-factor authentication (2FA)
- Username authentication
- Multiple plugins (specify)

**5. Environment** - "Where is this being implemented?"
- New project (full setup)
- Existing project (integration)

---

## Output Specification

This skill produces:

### Files Created/Modified:
- `lib/auth.ts` - Server-side auth configuration
- `lib/auth-client.ts` - Client-side auth configuration
- `middleware.ts` - Route protection middleware (Next.js)
- `app/api/auth/[...all]/route.ts` - API route handler (Next.js)
- `package.json` - With better-auth dependencies
- Framework-specific integration files

### Standards:
- ✅ Uses TypeScript with proper typing
- ✅ Implements security best practices (secure cookies, CSRF protection)
- ✅ Follows framework-specific patterns (Next.js App Router, Express middleware)
- ✅ Includes environment variable validation
- ✅ Configures proper session management

### Checklist:
- [ ] Authentication methods properly configured
- [ ] Database connection established
- [ ] Social providers configured (if requested)
- [ ] Session management configured
- [ ] Rate limiting enabled
- [ ] Secure cookie settings applied
- [ ] Framework-specific middleware implemented
- [ ] Client-side integration created

---

## Database Integration Patterns

Based on your database choice, this skill implements the appropriate adapter:

### Direct Database Connections
```typescript
// PostgreSQL
import { betterAuth } from "better-auth";
import { createPool } from "mysql2/promise";

export const auth = betterAuth({
    database: createPool({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME,
    }),
});
```

### Prisma Adapter
```typescript
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
export const auth = betterAuth({
    database: prismaAdapter(prisma, {
        provider: "postgresql", // or "mysql", "sqlite"
    }),
});
```

### Drizzle Adapter
```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db"; // your drizzle instance

export const auth = betterAuth({
    database: drizzleAdapter(db, {
        provider: "pg", // or "mysql", "sqlite"
    }),
});
```

---

## Authentication Configuration

### Email and Password
```typescript
{
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    minPasswordLength: 8,
  },
}
```

### Social Providers
```typescript
{
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
}
```

---

## Security Best Practices Applied

This skill automatically applies these security measures:

- Secure cookies with HttpOnly and Secure flags
- CSRF protection enabled by default
- Rate limiting to prevent abuse
- Proper session expiration and refresh
- IP address tracking for security
- Cross-subdomain cookie handling when needed

---

## Implementation Workflow

The skill follows this sequence:

1. **Install Dependencies** - Add better-auth and related packages
2. **Configure Database** - Set up database adapter based on user choice
3. **Set Authentication Methods** - Enable requested auth methods
4. **Add Plugins** - Integrate requested plugins
5. **Framework Integration** - Create middleware and route handlers
6. **Client Setup** - Configure client-side integration
7. **Environment Variables** - Document required environment variables

Each step validates configuration before proceeding to ensure a working setup.