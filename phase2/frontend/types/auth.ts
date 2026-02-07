// types/auth.ts
// Authentication-related type definitions

export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData extends LoginCredentials {
  name?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
  refreshToken?: string;
}

export interface Session {
  token: string;
  user: User;
  expiresAt: Date;
  sessionId: string;
}