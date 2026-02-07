'use client';

import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { TaskForm } from '@/components/tasks/task-form';
import { TaskList } from '@/components/tasks/task-list';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, loading: authLoading, isAuthenticated, checkAuth } = useAuth();
  const router = useRouter();

  useEffect(() => {
    const checkAuthentication = async () => {
      const authenticated = await checkAuth();
      if (!authenticated) {
        router.push('/login');
      }
    };

    checkAuthentication();
  }, [checkAuth, router]);

  // Show loading state with spinner if auth is still being checked
  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
          <p className="text-lg text-gray-700">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  // If not authenticated, show loading state while redirecting
  if (!isAuthenticated && !authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
          <p className="text-lg text-gray-700">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  // Only render the dashboard content if authenticated
  return <AuthenticatedDashboard user={user} />;
}

function AuthenticatedDashboard({ user }: { user: any }) {
  const { tasks, loading: tasksLoading, createTask, deleteTask, toggleTaskCompletion, updateTask } = useTasks(true);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
          {user && (
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user.name || user.email}</span>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left column - Task creation form */}
          <div className="lg:w-1/3">
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Create New Task</h2>
              <TaskForm onCreateTask={createTask} />
            </div>
          </div>

          {/* Right column - Task list */}
          <div className="lg:w-2/3">
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Your Tasks</h2>

              {tasksLoading ? (
                <div className="space-y-4">
                  {/* Skeleton loading UI */}
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="animate-pulse border rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <div className="h-4 w-4 bg-gray-300 rounded"></div>
                        <div className="flex-1 space-y-2">
                          <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <TaskList
                  tasks={tasks}
                  onDelete={deleteTask}
                  onToggleComplete={toggleTaskCompletion}
                  onUpdate={updateTask}
                />
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}