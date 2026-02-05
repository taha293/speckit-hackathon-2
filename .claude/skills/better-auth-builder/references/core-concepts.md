# Better Auth Reference Guide

## Core Concepts

Better Auth is a framework-agnostic authentication and authorization library for TypeScript that provides:

- **Email/Password Authentication** - Traditional username and password authentication
- **Social Login** - Integration with OAuth providers (Google, GitHub, etc.)
- **Session Management** - Automatic session handling with refresh mechanisms
- **Database Adapters** - Support for multiple databases and ORMs
- **Plugins System** - Extensible functionality through plugins

## Authentication Methods

### Email and Password
- Enables traditional sign-in with email and password
- Configurable password requirements (length, complexity)
- Optional email verification requirement
- Password reset functionality

### Social Providers
- Supports popular OAuth providers (Google, GitHub, Facebook, etc.)
- Easy configuration with client credentials
- Automatic user account linking

## Database Support

Better Auth supports multiple database configurations:

### Direct Connections
- PostgreSQL via node-postgres/mysql2
- MySQL via mysql2/promise
- SQLite via sqlite3
- MongoDB via native driver

### ORM/Query Builder Adapters
- Prisma ORM adapter
- Drizzle ORM adapter
- Direct MongoDB adapter

## Security Features

- **Secure Cookies** - HttpOnly and Secure flags by default
- **CSRF Protection** - Built-in CSRF token validation
- **Rate Limiting** - Prevents brute-force attacks
- **IP Tracking** - Monitor and log IP addresses
- **Session Validation** - Regular session integrity checks

## Framework Integration

Better Auth provides specific integrations for:
- Next.js (App Router and Pages Router)
- Express.js
- Node.js standalone
- React client-side