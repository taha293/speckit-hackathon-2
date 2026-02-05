# Better Auth Builder Skill

This skill helps implement authentication systems using Better Auth, a framework-agnostic authentication and authorization library for TypeScript.

## Overview

The Better Auth Builder skill provides a comprehensive solution for implementing authentication in various frameworks with different database configurations. It handles the entire setup process from installation to configuration.

## Capabilities

- **Framework Integration**: Next.js, Express.js, and generic Node.js applications
- **Database Support**: PostgreSQL, MySQL, SQLite, MongoDB, Prisma, and Drizzle
- **Authentication Methods**: Email/password, social providers (GitHub, Google, etc.)
- **Plugin Support**: Admin panel, Two-factor authentication, Username authentication
- **Security Features**: Secure cookies, CSRF protection, rate limiting, session management

## Usage

When implementing authentication with Better Auth, this skill will:

1. Install required dependencies based on your framework and database choice
2. Configure the authentication system with appropriate settings
3. Set up framework-specific integration (API routes, middleware, etc.)
4. Create client-side configuration for frontend integration
5. Provide environment variable requirements
6. Apply security best practices

## Components

- `SKILL.md`: Main skill definition with usage instructions
- `references/`: Detailed guides on core concepts, best practices, plugins, and framework integration
- `scripts/setup.sh`: Automated setup script for installing dependencies
- `assets/auth-template.ts`: Base authentication configuration template

## Prerequisites

Before using this skill, ensure you have:

- A Node.js project set up
- Appropriate database connection details
- OAuth provider credentials (for social login)
- Understanding of your framework requirements

## Architecture

This skill follows a layered approach:
- Core authentication configuration
- Framework-specific integration
- Client-side setup
- Security best practices
- Plugin integration