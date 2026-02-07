// hooks/useAuth.ts
// Custom React hook for authentication state management
// Works with backend API for authentication and Better Auth for JWT token management

import { useState, useCallback } from 'react';
import { useSession } from '@/lib/auth-client';
import { authApi } from '@/lib/api';

export const useAuth = () => {
  const { data: session, isPending: loading, error: sessionError } = useSession();
  const [error, setError] = useState<string | null>(null);

  // Login function - calls backend API directly
  const login = useCallback(async (email: string, password: string) => {
    try {
      setError(null);

      // Call backend API for login
      const result = await authApi.login(email, password);

      if (result.error) {
        throw new Error(result.error);
      }

      // Store the JWT token received from backend
      if (result.data?.access_token && typeof window !== 'undefined') {
        localStorage.setItem('backend_jwt_token', result.data.access_token);
      }

      return { success: true, data: result.data };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  }, []);

  // Signup function - calls backend API directly
  const signup = useCallback(async (email: string, password: string, name?: string) => {
    try {
      setError(null);

      // Call backend API for signup
      const result = await authApi.signup(email, password, name);

      if (result.error) {
        throw new Error(result.error);
      }

      return { success: true, data: result.data };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Signup failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  }, []);

  // Logout function - clears stored JWT token
  const logout = useCallback(async () => {
    try {
      setError(null);
      // Clear the stored JWT token
      if (typeof window !== 'undefined') {
        localStorage.removeItem('backend_jwt_token');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Logout failed';
      setError(errorMessage);
    }
  }, []);

  // Check auth status - checks if JWT token exists
  const checkAuth = useCallback(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('backend_jwt_token');
      return !!token;
    }
    return false;
  }, []);

  return {
    user: session?.user || null, // User data from session if available
    loading,
    error: error || sessionError?.message || null,
    isAuthenticated: typeof window !== 'undefined' && !!localStorage.getItem('backend_jwt_token'), // Check if JWT token exists
    login,
    signup,
    logout,
    checkAuth,
  };
};