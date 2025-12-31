from typing import List, Optional
from .models import Task

class TaskNotFoundError(Exception):
    """Raised when a task with a given ID is not found."""
    pass

class TodoService:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def list_tasks(self) -> List[Task]:
        """Returns all tasks in memory."""
        return self._tasks

    def add(self, title: str, description: Optional[str] = None) -> Task:
        """Adds a new task with an auto-incremented ID."""
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieves a task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found.")

    def set_status(self, task_id: int, completed: bool) -> Task:
        """Updates task completion status."""
        task = self.get_task(task_id)
        task.completed = completed
        return task

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """Updates task title and/or description."""
        task = self.get_task(task_id)
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        return task

    def delete(self, task_id: int) -> None:
        """Deletes a task by ID."""
        task = self.get_task(task_id)
        self._tasks.remove(task)
