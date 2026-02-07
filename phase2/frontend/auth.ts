// auth.ts
// Better Auth server-side configuration - JWT token management only
// This will manage JWT tokens received from the backend API, not perform authentication

import { betterAuth } from 'better-auth';
import { nextCookies } from 'better-auth/next-js';

// Initialize Better Auth with JWT-only configuration
const authInstance = betterAuth({
  // Disable email/password authentication since backend handles it
  emailAndPassword: {
    enabled: false, // Disabled - backend handles user registration/login
  },
  socialProviders: {
    // No social providers needed - backend handles auth
  },
  plugins: [
    nextCookies() // Enable cookies in server actions
  ],
  // JWT configuration to work with backend tokens
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days - matches backend expiration
  },
  baseURL: process.env.BETTER_AUTH_BASE_URL || "http://localhost:3000",
});

export const auth = authInstance;