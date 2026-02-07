// lib/api.ts
// API client with JWT token handling for backend integration

import { redirectToLogin } from '@/lib/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

// Helper function to convert HTTP status codes to user-friendly messages
function getErrorMessage(status: number, defaultMessage?: string): string {
  const errorMessages: Record<number, string> = {
    400: 'Invalid request. Please check your input and try again.',
    401: 'Your session has expired. Please log in again.',
    403: 'You do not have permission to perform this action.',
    404: 'The requested resource was not found.',
    409: 'This action conflicts with existing data.',
    422: 'The data provided is invalid. Please check and try again.',
    429: 'Too many requests. Please wait a moment and try again.',
    500: 'Server error. Please try again later.',
    502: 'Service temporarily unavailable. Please try again later.',
    503: 'Service temporarily unavailable. Please try again later.',
    504: 'Request timeout. Please try again.',
  };

  return errorMessages[status] || defaultMessage || 'An unexpected error occurred. Please try again.';
}

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  body?: any;
  headers?: Record<string, string>;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

class ApiClient {
  async request<T>(endpoint: string, options: ApiOptions = {}): Promise<ApiResponse<T>> {
    try {
      const { method = 'GET', body, headers = {} } = options;

      // Get the JWT token from localStorage (received from backend)
      const token = typeof window !== 'undefined'
        ? localStorage.getItem('backend_jwt_token')
        : null;

      const config: RequestInit = {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...(token && { Authorization: `Bearer ${token}` }),
          ...headers,
        },
      };

      if (body) {
        config.body = JSON.stringify(body);
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

      let data;
      try {
        data = await response.json();
      } catch (error) {
        // If response is not JSON (e.g., for DELETE operations), continue
        if (response.status !== 204) {
          console.warn('Non-JSON response:', await response.text());
        }
      }

      // Handle 401 Unauthorized - token may be expired
      if (response.status === 401) {
        console.error('Unauthorized access - redirecting to login');
        // Clear the invalid token
        if (typeof window !== 'undefined') {
          localStorage.removeItem('backend_jwt_token');
        }
        redirectToLogin();
        return {
          error: getErrorMessage(401),
          status: response.status,
        };
      }

      if (!response.ok) {
        // Use backend error message if available, otherwise use user-friendly message
        const userFriendlyError = data?.detail || data?.message || getErrorMessage(response.status);
        return {
          error: userFriendlyError,
          status: response.status,
        };
      }

      return {
        data,
        status: response.status,
      };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error occurred',
        status: 0,
      };
    }
  }

  async get<T>(endpoint: string, headers?: Record<string, string>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET', headers });
  }

  async post<T>(endpoint: string, body?: any, headers?: Record<string, string>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'POST', body, headers });
  }

  async put<T>(endpoint: string, body?: any, headers?: Record<string, string>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'PUT', body, headers });
  }

  async patch<T>(endpoint: string, body?: any, headers?: Record<string, string>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'PATCH', body, headers });
  }

  async delete<T>(endpoint: string, headers?: Record<string, string>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE', headers });
  }
}

export const apiClient = new ApiClient();

// Specific API functions for authentication
export const authApi = {
  login: (email: string, password: string) =>
    // Use raw fetch for login since we don't have a token yet
    fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const userFriendlyError = errorData?.detail || errorData?.message || getErrorMessage(response.status);
        return {
          error: userFriendlyError,
          status: response.status,
        };
      }
      const data = await response.json();
      return {
        data,
        status: response.status,
      };
    }),

  signup: (email: string, password: string, name?: string) =>
    // Use raw fetch for signup since we don't have a token yet
    fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, name }),
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const userFriendlyError = errorData?.detail || errorData?.message || getErrorMessage(response.status);
        return {
          error: userFriendlyError,
          status: response.status,
        };
      }
      const data = await response.json();
      return {
        data,
        status: response.status,
      };
    }),
};

// Specific API functions for tasks
export const tasksApi = {
  getAll: () => apiClient.get('/tasks/'),

  getById: (id: string) => apiClient.get(`/tasks/${id}`),

  create: (taskData: { title: string; description?: string; completed?: boolean }) =>
    apiClient.post('/tasks/', taskData),

  update: (id: string, taskData: Partial<{ title: string; description?: string; completed?: boolean }>) =>
    apiClient.put(`/tasks/${id}`, taskData),

  // PATCH endpoint to toggle task completion - uses query parameter
  toggleCompletion: (id: string, completed: boolean) =>
    apiClient.patch(`/tasks/${id}/complete?completed=${completed}`),

  delete: (id: string) => apiClient.delete(`/tasks/${id}`),
};