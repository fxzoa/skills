---
name: multi-agent-team
description: Orchestrate and configure multi-model AI teams (Coordinator, Advisor, Reviewer, Worker) across Antigravity projects.
---

# Multi-Agent Team Orchestration

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Configure and run parallel multi-model agent teams with clear role separation (`inherit` / `pro` / `flash_lite`).

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `configure_team` | `python3 scripts/configure_team.py ...` | Deterministic code-driven generator |
| `team_scripts` | `ls scripts/` | Inspect available team orchestration helpers and templates in `templates/`. |

## Role & Model Delegation (Rule.15)
- **Coordinator (`inherit` / Flash)**: User alignment, task decomposition, and primary implementation.
- **Advisor (`pro`)**: Architecture design and critical technical decisions.
- **Reviewer (`pro`)**: Strict code review, security audits, and verification.
- **Worker (`flash_lite`)**: Broad codebase searches, parallel checks, and batch data tasks.

## Workflow
1. Assess parallelizability before starting; split independent research, edits, and checks across subagents.
2. Spawn workers with explicit scope, target files, and expected output format.
3. Aggregate results, resolve conflicts, and verify before final report.

## Trigger & Exit Criteria
- **Trigger**: Tasks requiring parallel multi-agent delegation or team rule configuration.
- **Exit Criteria**: All delegated subtasks complete, verified, and `references/CHECKLIST.md` passes.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never spawn redundant agents for trivial single-step lookups.
- Never skip Reviewer (`pro`) verification on critical architecture or security changes.
