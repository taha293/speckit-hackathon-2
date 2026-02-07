// types/tasks.ts
// Task-related type definitions

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
  userId: string;
}

export interface TaskInput {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskResponse {
  task: Task;
}

export interface TasksResponse {
  tasks: Task[];
}