# Phase 1: Evolution of Todo CLI

A simple, in-memory, console-based Todo application built with Python 3.13 and `uv`. This is the first phase of the Evolution of Todo project, focused on core logic and CLI interactions.

## Features

- **In-Memory Storage**: Fast, transient storage for tasks (single-user).
- **Rich CLI**: Beautifully formatted tables and prompts using the `rich` library.
- **Task Management**:
  - `add`: Create new tasks with optional descriptions.
  - `list`: View all tasks with IDs, titles, and color-coded status.
  - `complete`: Tag tasks as "complete" or "incomplete".
  - `update`: Modify task titles and descriptions.
  - `delete`: Remove tasks with confirmation.
- **Self-Documenting**: Type `help` inside the app for a list of commands.

## Prerequisites

- [Python 3.13+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package manager)

## Setup

1. **Clone the repository** (if you haven't already).
2. **Navigate to the phase 1 directory**:
   ```bash
   cd phase1
   ```
3. **Sync dependencies**:
   ```bash
   uv sync
   ```

## Running the Application

Run the following command from within the `phase1` directory:

```bash
uv run todo
```

Alternatively, if you haven't installed it as a package yet, you can run:
```bash
set PYTHONPATH=src
uv run python -m phase1.main
```

## Running Tests

Verify the business logic with `pytest`:

```bash
uv run pytest
```

## Project Structure

- `src/phase1/main.py`: CLI loop and command handlers.
- `src/phase1/service.py`: Core business logic (TodoService).
- `src/phase1/models.py`: Data classes (Task).
- `tests/`: Unit tests for the service layer.

## Constitution & SDS

This project follows **Spec-Driven Development (SDD)**. All changes originate from the specifications located in the `specs/` directory at the repository root.
