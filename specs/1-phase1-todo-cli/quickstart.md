# Quickstart: Phase 1 Todo CLI

## Prerequisites
- Python 3.13+
- `uv` installed

## Installation

```bash
cd phase1
uv sync
```

## Running the Application

There are two ways to run the application:

### Method 1: Via Script (Recommended)
```bash
cd phase1
uv run todo
```

### Method 2: Via Module
```bash
cd phase1
set PYTHONPATH=src
uv run python -m phase1.main
```

## Running Tests

```bash
uv run pytest
```

## Usage Example

1. **Add a task**: Enter `add`, then follow prompts for title and description.
2. **List tasks**: Enter `list` to see IDs and status.
3. **Toggle status**: Enter `complete`, provide the ID, and follow status prompts.
4. **Exit**: Enter `exit`.
