---
name: sample-skill
description: Sample standardized skill
---

# sample-skill

Execute standard operations via pre-built scripts in `scripts/`.

## Pre-Built Operations (`scripts/`)

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `example_op` | `python3 scripts/example_op.py <arg>` | Describe operation |

## Workflow Calls
1. `example_op(<arg>)` → execute core workflow.

## Trigger & Exit Criteria
- **Trigger**: Describe when to activate `sample-skill`.
- **Exit Criteria**: Describe verification passing condition.

## Anti-Patterns
- Never duplicate logic or omit validation.
