# Better Auth Plugins Reference

## Available Plugins

Better Auth includes several optional plugins to extend functionality:

### Admin Plugin
The admin plugin provides an administrative interface for managing users and authentication data.

```typescript
import { betterAuth } from "better-auth";
import { admin } from "better-auth/plugins";

export const auth = betterAuth({
    // ...other config
    plugins: [
        admin()
    ]
});
```

Features:
- User management interface
- Authentication data inspection
- Administrative controls

### Two-Factor Authentication (2FA) Plugin
Enables two-factor authentication for enhanced security.

```typescript
import { betterAuth } from "better-auth";
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
    // ...other config
    plugins: [
        twoFactor()
    ]
});
```

Features:
- TOTP-based two-factor authentication
- Backup code generation
- QR code support for mobile apps

### Username Plugin
Adds username authentication alongside email authentication.

```typescript
import { betterAuth } from "better-auth";
import { username } from "better-auth/plugins";

export const auth = betterAuth({
    emailAndPassword: {
        enabled: true,
    },
    plugins: [
        username()
    ]
});
```

Features:
- Username-based login
- Custom username validation
- Support for alphanumeric usernames with underscores and dots

### Custom Username Validation
```typescript
import { betterAuth } from "better-auth";
import { username } from "better-auth/plugins";

const auth = betterAuth({
    emailAndPassword: {
        enabled: true,
    },
    plugins: [
        username({
            usernameValidator: (username) => {
                if (username === "admin") {
                    return false;
                }
                return true;
            }
        })
    ]
});
```

## Plugin Combinations

Multiple plugins can be used together:

```typescript
import { betterAuth } from "better-auth";
import { admin, twoFactor, username } from "better-auth/plugins";

export const auth = betterAuth({
    database: new Pool({
        connectionString: process.env.DATABASE_URL,
    }),
    emailAndPassword: {
        enabled: true,
    },
    socialProviders: {
        google: {
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
        },
        github: {
            clientId: process.env.GITHUB_CLIENT_ID!,
            clientSecret: process.env.GITHUB_CLIENT_SECRET!,
        }
    },
    plugins: [
        admin(),
        twoFactor(),
        username()
    ]
});
```

## Plugin Security Considerations

When using plugins:
- Review the permissions each plugin requires
- Understand data access patterns
- Configure rate limiting appropriately
- Monitor for security updates
- Test plugin functionality thoroughly