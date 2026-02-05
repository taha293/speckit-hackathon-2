# Better Auth Best Practices

## Installation Best Practices

### Minimal Installation
```bash
npm install better-auth
```

### Framework-Specific Dependencies
```bash
# For Next.js projects
npm install better-auth better-auth/next-js better-auth/react

# For Express projects
npm install better-auth better-auth/node

# For Prisma projects
npm install better-auth better-auth/adapters/prisma

# For Drizzle projects
npm install better-auth better-auth/adapters/drizzle
```

## Security Best Practices

### Session Configuration
- Set appropriate expiration times (recommended: 7 days for session, 1 day for refresh)
- Enable secure cookies in production
- Use HTTPS in production environments
- Enable CSRF protection (enabled by default)
- Implement rate limiting to prevent abuse

### Database Security
- Use environment variables for database credentials
- Implement proper connection pooling
- Regularly update database drivers
- Monitor database access patterns

### Authentication Security
- Require email verification for email/password accounts
- Set strong password requirements (min length: 8, complexity recommended)
- Implement account lockout after failed attempts
- Enable 2FA for sensitive operations

## Performance Optimization

### Session Management
- Use cookie-based caching for improved performance
- Set appropriate refresh intervals to balance security and performance
- Consider storing sessions in secondary storage for high-traffic applications

### Database Optimization
- Implement proper indexing on authentication tables
- Use connection pooling appropriately
- Consider caching frequently accessed user data
- Monitor and optimize database queries

## Common Anti-Patterns to Avoid

### Security Anti-Patterns
❌ Disabling CSRF protection in production
❌ Using insecure cookies (not HttpOnly or Secure)
❌ Hardcoding credentials in configuration files
❌ Disabling rate limiting

### Configuration Anti-Patterns
❌ Setting session timeouts too long
❌ Not configuring proper database connections
❌ Overriding default security settings without understanding implications
❌ Using same configuration for development and production

## Environment Configuration

### Required Environment Variables
```env
DATABASE_URL=your_database_connection_string
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Recommended Production Settings
```typescript
{
  advanced: {
    useSecureCookies: true,
    disableOriginCheck: false,
  },
  rateLimit: {
    enabled: true,
    window: 10,
    max: 100,
  },
  session: {
    expiresIn: 604800, // 7 days
    updateAge: 86400,  // 1 day
  }
}
```