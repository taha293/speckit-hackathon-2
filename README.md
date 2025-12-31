# Evolution of Todo

[![Spec-Driven Development](https://img.shields.io/badge/Methodology-Spec--Driven%20Development-blueviolet)](https://github.com/anthropics/claude-code)
[![Python 3.13](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![Package Manager: uv](https://img.shields.io/badge/Package%20Manager-uv-orange)](https://github.com/astral-sh/uv)

A reference implementation demonstrating the iterative growth of a system using **Spec-Driven Development (SDD)**. The project evolves through five distinct architectural phases, prioritizing specification as the immutable source of truth while treating code as a disposable artifact.

## 🚀 Project Vision

The system is designed to showcase how a simple concept—a Todo list—can scale from a local console application to a cloud-native, event-driven distributed system without losing architectural integrity. Each phase is independently specified and implemented, ensuring a clean transition and preservation of requirements.

---

## 🗺️ Roadmap & Evolution

| Phase | Milestone | Focus Area | Status |
| :--- | :--- | :--- | :--- |
| **Phase I** | **CLI Foundation** | In-memory, single-user, rich console interface. | ✅ **Released** |
| **Phase II** | **Web & Persistence** | Multi-user support, authentication, and persistent storage. | ⏳ Planned |
| **Phase III** | **AI Agent Fabric** | Integration via MCP (Model Context Protocol). | ⏳ Planned |
| **Phase IV** | **Orchestration** | Containerization and Kubernetes-native architecture. | ⏳ Planned |
| **Phase V** | **Cloud-Scale** | Event-driven, distributed, serverless infrastructure. | ⏳ Planned |

---

## 🛠️ Methodology & Governance

This project adheres to a strict **Constitution-first** approach. Every architectural decision and implementation step is governed by the [Project Constitution](.specify/memory/constitution.md).

### Core Principles
- **Spec-Driven Execution**: No line of code is written manually. All code is generated via [Spec-Kit Plus](https://github.com/anthropics/claude-code) based on verified specifications.
- **Verification Loop**: Implementation follows a rigorous flow: `Spec` → `Plan` → `Tasks` → `Analyze` → `Implement`.
- **Traceability**: Every exchange is recorded as a **Prompt History Record (PHR)**, providing 100% visibility into the "how" and "why" of the system's evolution.

---

## 🏁 Getting Started (Phase I)

To execute the current stable release:

```bash
# Clone and navigate to the phase 1 directory
cd phase1

# Sync environment and dependencies
uv sync

# Launch the interactive CLI
uv run todo
```

For comprehensive documentation on internal logic and testing, refer to the [Phase I Technical README](./phase1/README.md).

---

## 🏛️ Project Governance

- 📜 **Constitution**: [Constitution v1.0.0](.specify/memory/constitution.md) - The foundational laws of the repo.
- 📂 **Specifications**: Found in the [`/specs`](./specs) directory.
- 🕒 **History**: Audit trails available in [`/history/prompts`](./history/prompts).

---
*Created with SDD methodology. Code is disposable; specifications are permanent.*
