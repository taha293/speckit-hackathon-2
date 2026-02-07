// components/tasks/task-list.tsx
// Task list component to display multiple tasks

'use client';

import { Task } from '@/types/tasks';
import { TaskCard } from './task-card';

interface TaskListProps {
  tasks: Task[];
  onDelete: (id: string) => Promise<{ success: boolean; error?: string }>;
  onToggleComplete: (id: string) => Promise<{ success: boolean; error?: string }>;
  onUpdate?: (id: string, data: { title: string; description?: string }) => Promise<{ success: boolean; error?: string }>;
}

export const TaskList = ({ tasks, onDelete, onToggleComplete, onUpdate }: TaskListProps) => {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onDelete={onDelete}
          onToggleComplete={onToggleComplete}
          onUpdate={onUpdate}
        />
      ))}
    </div>
  );
};