<!--
Version change: [CONSTITUTION_VERSION_OLD] -> 1.0.0
List of modified principles:
  - Phase Evolution Contract (Added)
  - Development Rules (Added)
  - Architecture & Quality Principles (Added)
  - AI & Cloud Governance (Added)
  - Authority (Added)
Added sections:
  - Phase Evolution Contract
  - AI & Cloud Governance
  - Authority
Removed sections:
  - [SECTION_2_NAME], [SECTION_3_NAME] (merged/replaced by concrete sections)
Templates requiring updates:
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
Follow-up TODOs:
  - Identify original RATIFICATION_DATE (set to 2025-12-31 as today)
-->

# Spec Constitution – Evolution of Todo

## Purpose
This project is built using **Spec-Driven Development**.
Specifications define system behavior, architecture, and evolution.
All code is generated exclusively via Claude Code using Spec-Kit Plus.

## Development Rules
- Manual code writing or editing is not allowed. All changes must originate from updated specifications.
- All changes must originate from updated specifications.
- If implementation is incorrect, the specification must be refined instead of patching the code directly.
- Each phase must be fully specified (spec, plan, tasks) before implementation begins.

## Phase Evolution Contract
The system evolves incrementally across five phases. Each phase must preserve previous behavior unless explicitly redefined:

- **Phase I**: Console application, in-memory state, single user.
- **Phase II**: Persistent storage, authentication, multi-user web app.
- **Phase III**: AI agents interacting through MCP-defined tools.
- **Phase IV**: Containerized, Kubernetes-native deployment.
- **Phase V**: Event-driven, distributed, cloud-scale architecture.

## Architecture & Quality Principles
- **Separation of Concerns**: Clear boundaries between models, services, and interfaces.
- **Predictability**: Deterministic behavior is mandatory.
- **Error Handling**: Explicit handling of all error paths; no silent failures.
- **Statelessness**: Services must be stateless from Phase III onward.
- **Idempotency**: Operations should be idempotent where applicable to ensure reliability.

## AI & Cloud Governance
- **Tool-Mediated Action**: AI agents may only act through approved tools and MCP servers.
- **Mutation Control**: Direct state mutation by agents is forbidden; all mutations must be via specifications.
- **Reproducibility**: Infrastructure must be declarative (IaC) and fully reproducible.
- **Security**: Secrets and configuration must never be hardcoded; use environment variables or secret managers.

## Authority
- **Specification Supremacy**: In any conflict, specifications override code.
- **Constitution Supremacy**: The constitution overrides all other documents and practices.
- **Code Temporality**: Code is disposable; specifications are permanent and represent the truth of the system.

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
