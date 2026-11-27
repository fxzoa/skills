# PROTOTYPE.md: Reusable Core vs. Project-Specific Replacements (`multi-agent-team`)

This document defines the boundary between reusable core assets and project-specific replacements for `multi-agent-team`.

---

## 1. Prototype Structure

```text
prototype/
└── team.json   # Sample team configuration payload
```

---

## 2. Reusable Core vs. Project-Specific Replacements

| Component | Reusable Core Design (Keep As-Is) | Project-Specific Replacements (Customize Per Project) |
|:---|:---|:---|
| **Role & Model Delegation (`templates/team_model_delegation.md`)** | Four-role separation: Coordinator (`inherit`), Advisor (`pro`), Reviewer (`pro`), and Worker (`flash_lite`). | Project-specific model IDs or custom role overrides in workspace `AGENTS.md`. |
| **Team Configurator (`scripts/configure_team.py`, `scripts/setup.sh`)** | Deterministic script interface for generating and applying team delegation rules. | Target project root path, team name (`prototype/team.json`), and local workspace rule file paths. |
| **Orchestration Workflow** | Parallelizability assessment, explicit subagent scope/output contracts, result aggregation, and Reviewer verification gate. | Domain-specific subtask breakdown, target file lists, and acceptance criteria per task. |
