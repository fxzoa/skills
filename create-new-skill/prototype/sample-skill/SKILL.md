---
name: sample-skill
description: Demonstrates the standardized 11-part Antigravity skill layout and deterministic script delegation. Use when referencing a minimal compliant skill example. Do not use for production workloads.
---

# sample-skill

Execute standard operations via pre-built scripts in `scripts/`.

## Pre-Built Operations (`scripts/`)

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `example_op` | `python3 scripts/example_op.py <arg>` | Describe operation |

## Document Index
- [references/TRIGGERS.md](references/TRIGGERS.md): Positive / Negative trigger prompt examples

## Workflow Calls
1. `example_op(<arg>)` → execute core workflow.

## Trigger & Exit Criteria
- **Trigger**: Describe when to activate `sample-skill`.
- **Exit Criteria**: Describe verification passing condition.

## Anti-Patterns
- Never duplicate logic or omit validation.
