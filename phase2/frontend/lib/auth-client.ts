// lib/auth-client.ts
// Better Auth client-side configuration for JWT token management
// This manages JWT tokens received from the backend API

'use client';

import { createAuthClient } from "better-auth/react";

// Initialize Better Auth client to work with backend JWT tokens
export const authClient = createAuthClient({
  // Base URL for the auth endpoints (these are used for Better Auth's own API calls)
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  // We don't rely on Better Auth's built-in session management for authentication,
  // since the backend handles it, so we just initialize it minimally
});

// Export the hooks and methods
export const { useSession, signIn, signUp, signOut } = authClient;