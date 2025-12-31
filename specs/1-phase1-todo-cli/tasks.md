# Tasks: Phase 1 Todo CLI

**Input**: Design documents from `/specs/1-phase1-todo-cli/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/service_interface.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Phase 1: Setup

**Purpose**: Project initialization and structure.

- [x] T001 Initialize `phase1` project structure and add `rich` dependency via `uv add rich` in `phase1/`
- [x] T002 [P] Create `phase1/src/phase1/__init__.py` and `phase1/src/phase1/models.py` per data-model.md
- [x] T003 [P] Create `phase1/tests/__init__.py` and empty test files

## Phase 2: Foundational

**Purpose**: Core logic and service layer required for all user stories.

- [x] T004 Implement `Task` dataclass in `phase1/src/phase1/models.py`
- [x] T005 Implement `TodoService` with in-memory storage in `phase1/src/phase1/service.py`
- [x] T006 Implement `list_tasks` functionality in `phase1/src/phase1/service.py`
- [x] T007 [P] Create CLI loop skeleton in `phase1/src/phase1/main.py` with `rich` console initialization

## Phase 3: User Story 1 - Add and List Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks and view them.

**Independent Test**: Add two tasks via CLI, then list them and verify titles, IDs (1, 2) and "incomplete" status are shown correctly.

- [x] T008 [US1] Implement `add` method in `phase1/src/phase1/service.py`
- [x] T009 [US1] Implement `add` command handler in `phase1/src/phase1/main.py`
- [x] T010 [US1] Implement `list` command handler using `rich.table` in `phase1/src/phase1/main.py`
- [x] T011 [P] [US1] Create unit tests for add/list in `phase1/tests/test_service.py`

**Checkpoint**: User Story 1 (MVP) is fully functional and testable.

## Phase 4: User Story 2 - Manage Task Status (Priority: P2)

**Goal**: Allow users to toggle status between complete and incomplete.

**Independent Test**: Select a task ID, use the `complete` command, toggle to complete, and verify status change in `list`.

- [x] T012 [US2] Implement `set_status` method in `phase1/src/phase1/service.py`
- [x] T013 [US2] Implement `complete` command handler in `phase1/src/phase1/main.py` with status prompt
- [x] T014 [P] [US2] Create unit tests for status tagging in `phase1/tests/test_service.py`

**Checkpoint**: Tasks can now be managed through their full lifecycle (incomplete <-> complete).

## Phase 5: User Story 3 - Update and Delete Tasks (Priority: P3)

**Goal**: Enable task modification and removal.

**Independent Test**: Update a task title, then delete the task and verify it's gone from `list`.

- [x] T015 [US3] Implement `update` and `delete` methods in `phase1/src/phase1/service.py`
- [x] T016 [US3] Implement `update` command handler in `phase1/src/phase1/main.py`
- [x] T017 [US3] Implement `delete` command handler in `phase1/src/phase1/main.py` with confirmation prompt
- [x] T018 [P] [US3] Create unit tests for update/delete in `phase1/tests/test_service.py`

**Checkpoint**: All specified task management operations are complete.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Error handling and final cleanup.

- [x] T019 Implement global exception handling for CLI loop in `phase1/src/phase1/main.py`
- [x] T020 [P] Add input validation for empty titles in `phase1/src/phase1/main.py`
- [x] T021 [P] Document usage in `phase1/README.md`

## Dependencies & Execution Order

1. **Setup (Phase 1)** -> **Foundational (Phase 2)** (Linear)
2. **Foundational (Phase 2)** -> **User Story 1 (Phase 3)** (Blocking)
3. **User Story 1 (Phase 3)** -> **User Story 2 (Phase 4)** & **User Story 3 (Phase 5)** (Incremental)
4. **All Stories** -> **Polish (Phase 6)**

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Setup and Foundational logic.
2. Implement Add and List functionality.
3. Validate MVP.

### Parallel Opportunities
- T011, T014, T018 (Tests) can be written in parallel once service interfaces are settled.
- T002 and T003 can be run in parallel during Setup.
