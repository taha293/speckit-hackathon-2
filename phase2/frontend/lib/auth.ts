// lib/auth.ts
// Authentication utilities for backend JWT integration

import { auth } from "@/auth"
import { redirect } from "next/navigation";

// Better Auth server configuration (JWT token management only)
export { auth };

// Redirect to login page
export function redirectToLogin() {
  if (typeof window !== 'undefined') {
    // Clear any stored JWT token on redirect
    localStorage.removeItem('backend_jwt_token');
    // Client-side redirect
    window.location.href = '/login';
  } else {
    // Server-side redirect
    redirect('/login');
  }
}

// Get the current JWT token
export function getCurrentToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('backend_jwt_token');
  }
  return null;
}

// Set the JWT token in storage
export function setCurrentToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('backend_jwt_token', token);
  }
}

// Clear the JWT token
export function clearCurrentToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('backend_jwt_token');
  }
}

// Check if user is authenticated
export function isAuthenticated(): boolean {
  return !!getCurrentToken();
}