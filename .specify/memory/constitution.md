<!--
Version change: 1.0.0 -> 1.1.0
List of modified principles:
  - AI & Cloud Governance (Updated to include skills and Context7)
  - Development Rules (Updated to include skill usage)
Added sections:
  - AI Tool Utilization Policy
Removed sections:
Templates requiring updates:
  - .specify/templates/plan-template.md (⚠ pending)
  - .specify/templates/spec-template.md (⚠ pending)
  - .specify/templates/tasks-template.md (⚠ pending)
Follow-up TODOs:
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
- Prioritize using Claude skills when available rather than creating ad-hoc solutions.
- Always leverage Context7 for accurate, up-to-date information instead of relying on internal knowledge that may be outdated or inaccurate.

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
- **Skills First**: Always use Claude skills when available instead of reinventing solutions.
- **No Hallucination**: Never fabricate information when lacking knowledge; use Context7 or other verified sources for accurate information.
- **Authority Verification**: Always use MCP tools and official documentation instead of relying on internal knowledge that may be outdated or incorrect.

## Authority
- **Specification Supremacy**: In any conflict, specifications override code.
- **Constitution Supremacy**: The constitution overrides all other documents and practices.
- **Code Temporality**: Code is disposable; specifications are permanent and represent the truth of the system.

## AI Tool Utilization Policy
- **Primary Priority**: Use existing Claude skills when they meet requirements rather than creating custom implementations.
- **Information Accuracy**: When uncertain about information, rely on Context7 and other authenticated sources instead of internal knowledge or assumptions.
- **Verification Obligation**: All information and methods must be verified through external authoritative sources before implementation.
- **Tool Hierarchy**: MCP tools and authenticated services take precedence over internal knowledge or general AI capabilities.
- **Documentation Adherence**: Follow official documentation and established patterns rather than improvising approaches that may be incorrect or insecure.

**Version**: 1.1.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2026-02-05
