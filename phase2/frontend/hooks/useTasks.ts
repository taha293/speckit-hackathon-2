// hooks/useTasks.ts
// Custom React hook for task data management

import { useState, useEffect, useCallback } from 'react';
import { tasksApi } from '@/lib/api';
import { Task, TaskInput } from '@/types/tasks';

export const useTasks = (isAuthenticated: boolean = false) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasFetched, setHasFetched] = useState(false);

  // Load tasks
  const loadTasks = useCallback(async () => {
    // Don't make API call if not authenticated
    if (!isAuthenticated) {
      setTasks([]);
      setLoading(false);
      setHasFetched(false);
      return;
    }

    // Check if user is authenticated before making API call
    const token = typeof window !== 'undefined'
      ? localStorage.getItem('backend_jwt_token')
      : null;

    if (!token) {
      // Don't make API call if no token
      setTasks([]);
      setLoading(false);
      setHasFetched(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await tasksApi.getAll();

      if (response.error) {
        throw new Error(response.error);
      }

      if (response.data) {
        // Backend returns tasks array directly
        setTasks(Array.isArray(response.data) ? response.data : []);
      } else {
        setTasks([]);
      }
      setHasFetched(true);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load tasks';
      setError(errorMessage);
      setHasFetched(true);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  // Initialize tasks only once when authenticated
  useEffect(() => {
    // Only fetch if authenticated and haven't fetched yet
    if (isAuthenticated && !hasFetched) {
      loadTasks();
    }
  }, [isAuthenticated, hasFetched, loadTasks]);

  // Create task
  const createTask = useCallback(async (taskData: TaskInput) => {
    try {
      setLoading(true);
      setError(null);

      const response = await tasksApi.create(taskData);

      if (response.error) {
        throw new Error(response.error);
      }

      if (response.data) {
        // Add the new task to the list - cast to Task type
        setTasks(prev => [...prev, response.data as Task]);
        return { success: true, task: response.data as Task };
      }

      throw new Error('Failed to create task');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create task';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, []);

  // Update task
  const updateTask = useCallback(async (id: string, taskData: Partial<TaskInput>) => {
    try {
      setError(null);

      const response = await tasksApi.update(id, taskData);

      if (response.error) {
        throw new Error(response.error);
      }

      if (response.data) {
        setTasks(prev => prev.map(t => t.id === id ? response.data as Task : t));
        return { success: true, task: response.data as Task };
      }

      throw new Error('Failed to update task');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  }, []);

  // Toggle task completion
  const toggleTaskCompletion = useCallback(async (id: string) => {
    try {
      setError(null);

      // Find the current task
      const currentTask = tasks.find(t => t.id === id);
      if (!currentTask) {
        throw new Error('Task not found');
      }

      // Use the PATCH endpoint to toggle completion
      const response = await tasksApi.toggleCompletion(id, !currentTask.completed);

      if (response.error) {
        throw new Error(response.error);
      }

      if (response.data) {
        setTasks(prev => prev.map(t => t.id === id ? response.data as Task : t));
        return { success: true, task: response.data as Task };
      }

      throw new Error('Failed to toggle task completion');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to toggle task completion';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  }, [tasks]);

  // Delete task
  const deleteTask = useCallback(async (id: string) => {
    try {
      setError(null);

      const response = await tasksApi.delete(id);

      if (response.error) {
        throw new Error(response.error);
      }

      setTasks(prev => prev.filter(task => task.id !== id));
      return { success: true };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete task';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  }, []);

  // Get task by ID
  const getTaskById = useCallback((id: string) => {
    return tasks.find(task => task.id === id) || null;
  }, [tasks]);

  return {
    tasks,
    loading,
    error,
    loadTasks,
    createTask,
    updateTask,
    toggleTaskCompletion,
    deleteTask,
    getTaskById,
  };
};