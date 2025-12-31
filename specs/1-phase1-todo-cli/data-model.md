# Data Model: Phase 1 Todo CLI

## Entities

### Task
Represents a single todo item.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | int | Unique auto-incrementing identifier | Required, > 0 |
| title | str | Brief summary of the task | Required, mixed case |
| description | str | Optional detailed notes | Optional |
| completed | bool | Current completion status | Default: false |

## State Transitions

- **Creation**: `id` assigned, `completed` set to `False`.
- **Status Change**: `completed` can be toggled between `True` and `False` via the `complete` command.
- **Update**: `title` or `description` modified; `id` remains constant.
- **Deletion**: Task record removed from in-memory collection.
