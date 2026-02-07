// components/tasks/task-card.tsx
// Task card component for displaying individual tasks

'use client';

import { Task } from '@/types/tasks';
import { formatDate } from '@/lib/utils';
import { useToast } from '@/components/notifications/toast';
import { useState } from 'react';

interface TaskCardProps {
  task: Task;
  onDelete: (id: string) => Promise<{ success: boolean; error?: string }>;
  onToggleComplete: (id: string) => Promise<{ success: boolean; error?: string }>;
  onUpdate?: (id: string, data: { title: string; description?: string }) => Promise<{ success: boolean; error?: string }>;
}

export const TaskCard = ({ task, onDelete, onToggleComplete, onUpdate }: TaskCardProps) => {
  const { addToast } = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    const result = await onDelete(task.id);
    if (!result.success) {
      addToast(result.error || 'Failed to delete task', 'error');
    } else {
      addToast('Task deleted successfully', 'success');
    }
  };

  const handleToggleComplete = async () => {
    const result = await onToggleComplete(task.id);
    if (!result.success) {
      addToast(result.error || 'Failed to update task', 'error');
    } else {
      const message = task.completed
        ? 'Task marked as incomplete'
        : 'Task marked as complete';
      addToast(message, 'success');
    }
  };

  const handleSaveEdit = async () => {
    if (!onUpdate) {
      addToast('Update functionality not available', 'error');
      return;
    }

    if (!editTitle.trim()) {
      addToast('Task title cannot be empty', 'error');
      return;
    }

    const result = await onUpdate(task.id, {
      title: editTitle.trim(),
      description: editDescription.trim() || undefined,
    });

    if (!result.success) {
      addToast(result.error || 'Failed to update task', 'error');
    } else {
      addToast('Task updated successfully', 'success');
      setIsEditing(false);
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="border rounded-lg p-4 shadow-sm bg-white border-gray-200">
        <div className="space-y-3">
          <div>
            <label htmlFor={`edit-title-${task.id}`} className="block text-sm font-medium text-gray-700 mb-1">
              Title
            </label>
            <input
              id={`edit-title-${task.id}`}
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Task title"
            />
          </div>
          <div>
            <label htmlFor={`edit-description-${task.id}`} className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id={`edit-description-${task.id}`}
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              rows={3}
              className="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Task description (optional)"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <button
              onClick={handleCancelEdit}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
            <button
              onClick={handleSaveEdit}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`border rounded-lg p-4 shadow-sm ${task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}`}>
      <div className="flex justify-between items-start">
        <div className="flex items-start flex-1">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleComplete}
            className="mt-1 h-4 w-4 text-indigo-600 rounded focus:ring-indigo-500"
          />
          <div className="ml-3 flex-1">
            <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className="mt-1 text-sm text-gray-600">{task.description}</p>
            )}
            <p className="mt-1 text-xs text-gray-500">
              Created: {formatDate(task.createdAt)}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2 ml-4">
          <button
            onClick={() => setIsEditing(true)}
            className="text-indigo-600 hover:text-indigo-900 focus:outline-none"
            aria-label="Edit task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
          <button
            onClick={handleDelete}
            className="text-red-600 hover:text-red-900 focus:outline-none"
            aria-label="Delete task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};