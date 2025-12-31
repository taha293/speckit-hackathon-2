# Service Interface: Todo Service

Since Phase 1 is a single-process CLI, these "contracts" define the internal service interface boundaries.

## Commands (Input)

### `add(title: str, description: Optional[str]) -> Task`
- **Pre-conditions**: `title` must not be empty.
- **Post-conditions**: New task created with unique ID.

### `list_tasks() -> List[Task]`
- **Returns**: All tasks currently in memory.

### `update(task_id: int, title: Optional[str], description: Optional[str]) -> Task`
- **Errors**: Throws `TaskNotFoundError` if ID invalid.

### `set_status(task_id: int, completed: bool) -> Task`
- **Errors**: Throws `TaskNotFoundError` if ID invalid.

### `delete(task_id: int) -> None`
- **Errors**: Throws `TaskNotFoundError` if ID invalid.
