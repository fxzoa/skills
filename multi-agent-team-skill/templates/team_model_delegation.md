# Global Multi-Agent Team & Model Delegation Rules

## 1. Role & Model Hierarchy
Always delegate tasks to specialized subagents or swarm workers based on capability and cost:
- **Coordinator / Main (`Gemini 3.8 Flash` / `inherit`)**: User interaction, orchestration, core code implementation.
- **Advisor / Architect (`Gemini 4 Carbon` / `pro`)**: Architecture design, tradeoff analysis, system design brainstorming.
- **Reviewer / Auditor (`Gemini 4 Carbon` / `pro`)**: Strict code review, security audits, type checking, Rule.06/09 compliance.
- **Worker / Researcher (`Gemini 4 Hydrogen` / `flash_lite`)**: Fast file searches, parallel data processing, lightweight checks.

## 2. Delegation Execution
- **Parallel Research**: Decompose broad research or multi-file inspections into `Gemini 4 Hydrogen` (`flash_lite`) subagents (`invoke_subagent` / `swarm`).
- **Critical Reviews & Decisions**: Invoke a `Gemini 4 Carbon` (`pro`) subagent before finalizing large architectural decisions or after major code changes.
- **Conciseness**: Keep inter-agent communications concise and structured.
