from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from models.task import TaskCreate, TaskRead, TaskUpdate
from services.task_service import TaskService
from dependencies.auth import get_current_user
from models.user import User
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskRead])
def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """Get all tasks for the current user"""
    tasks = TaskService.get_tasks_by_user(db, current_user.id)
    return tasks

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    # Validate title length (1-200 chars)
    if len(task_create.title) < 1 or len(task_create.title) > 200:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must be between 1 and 200 characters"
        )

    # Validate description length (max 1000 chars)
    if task_create.description and len(task_create.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Description must be at most 1000 characters"
        )

    task = TaskService.create_task(db, task_create, current_user.id)
    return task

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get a specific task by ID"""
    task = TaskService.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update a specific task by ID"""
    task = TaskService.update_task(db, task_id, task_update, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete a specific task by ID"""
    success = TaskService.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    task_id: int,
    completed: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Toggle task completion status"""
    task = TaskService.toggle_task_completion(db, task_id, current_user.id, completed)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task