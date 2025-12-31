# Research: Phase 1 Todo CLI

This document outlines technical decisions for the Phase 1 implementation of the Todo CLI.

## Decision: Python CLI Framework
- **Chosen**: Standard Library (`sys.argv`, `input()`) + `rich` (for formatted output).
- **Rationale**: Phase 1 is a simple console app. Using standard library for input loops and `rich` for tables/colors provides a professional CLI feel without complexity.
- **Alternatives considered**: `click`, `argparse`. Rejected `click` as the spec requires a continuous loop of prompts (`input()`) rather than just command-line arguments.

## Decision: Task Storage
- **Chosen**: In-memory list of Task objects/dataclasses.
- **Rationale**: Mandatory constraint for Phase 1. Dataclasses provide type-safe data modeling.
- **Alternatives considered**: Simple dictionaries. Rejected as dataclasses offer better structure and readability.

## Decision: Task ID Generation
- **Chosen**: Atomic counter in a TaskManager class.
- **Rationale**: Ensures unique, auto-incrementing IDs as required by FR-003.
- **Alternatives considered**: UUIDs. Rejected as the spec explicitly asks for integers.

## Decision: Testing Framework
- **Chosen**: `pytest`.
- **Rationale**: Industry standard for Python testing; easy to mock stdin/stdout for CLI testing.
- **Alternatives considered**: `unittest`.

## Decision: Dependency Management
- **Chosen**: `uv`.
- **Rationale**: Explicit constraint for the project.
