#!/usr/bin/env python3
"""Scaffold a standardized Antigravity skill directory conforming to 10-part skill architecture."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold standardized skill bundle.")
    parser.add_argument("--dir", required=True, help="Target skill directory")
    parser.add_argument("--name", required=True, help="Skill name (kebab-case)")
    parser.add_argument("--desc", required=True, help="One-line skill description")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    for sub in ["scripts", "prototype", "templates", "references"]:
        (base / sub).mkdir(parents=True, exist_ok=True)

    (base / "SKILL.md").write_text(
        f"""---
name: {args.name}
description: {args.desc}
---

# {args.name}

Execute standard operations via pre-built scripts in `scripts/`.
Detailed tool interfaces, CLI options, and classifications are documented in [references/TOOLS.md](references/TOOLS.md).

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.

## Pre-Built Operations (`scripts/`)

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `example_op` | `python3 scripts/example_op.py <arg>` | Describe operation | [TOOLS.md](references/TOOLS.md) |

## Workflow Calls
1. `example_op(<arg>)` → execute core workflow.

## Trigger & Exit Criteria
- **Trigger**: Describe when to activate `{args.name}`.
- **Exit Criteria**: Describe verification passing condition.

## Anti-Patterns
- Never rely on probabilistic prompt-driven orchestration: materialize procedural steps into deterministic `scripts/*.py`.
- Never duplicate logic or omit validation.
- Never omit `references/TOOLS.md` or skip the 4-part tool classifications (`Command`, `Shell`, `MCP`, `外部 API`).
""",
        encoding="utf-8",
    )

    (base / "templates" / ".gitignore.tmpl").write_text(
        ".env\n.env.*\n!.env.example\n*.pem\n*.key\nlogs/\ntmp/\n__pycache__/\n*.pyc\n",
        encoding="utf-8",
    )

    (base / "references" / "TOOLS.md").write_text(
        f"""# Tools & Interfaces Reference (`{args.name}`)

This document defines tool interfaces, CLI signatures, and protocol classifications for `{args.name}`.
Tools are organized by execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `example_op.py` | Core workflow operator | `python3 scripts/example_op.py <arg>` | `0`: Success, `1`: Failure |

### 1.1 `example_op.py`
- **Arguments**:
  - `<arg>`: Description
- **Output**: Description

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose | Example |
|:---|:---|:---|
| `bash` | Script execution harness | `bash -c "..."` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Execute pre-built scripts in `scripts/` | Main tool execution |
| `read_file` | Read specifications, configs, and inputs | File inspection |
| `write_file` / `edit_file` | Generate or patch artifacts | Code generation |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol | Endpoint | Auth | Purpose |
|:---|:---|:---|:---|:---|
| N/A | HTTP/REST | - | - | External integrations (if any) |
""",
        encoding="utf-8",
    )

    (base / "references" / "ARCHITECTURE.md").write_text(
        f"""# Architecture & Specifications (`{args.name}`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  Input[Input / Config] --> Script[scripts/]
  Script --> Output[Deliverables]
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant Agent
  participant Script as scripts/
  Agent->>Script: Invoke pre-built operation
  Script-->>Agent: Verified result
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Env** | `EXAMPLE_VAR` | Example config |

## 4. Deliverables
- Standard output artifacts
""",
        encoding="utf-8",
    )

    (base / "references" / "CHECKLIST.md").write_text(
        f"# Acceptance Checklist (`{args.name}`)\n\n- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.\n- [ ] Scripts pass validation.\n- [ ] Deliverables verified.\n- [ ] TOOLS.md covers Command, Shell, MCP, and 外部 API.\n",
        encoding="utf-8",
    )
    (base / "references" / "GUIDE.md").write_text(
        f"# Operation Guide (`{args.name}`)\n\n1. Run `scripts/` operations.\n2. Verify against `CHECKLIST.md` and `references/TOOLS.md`.\n",
        encoding="utf-8",
    )
    (base / "references" / "PREREQUISITES.md").write_text(
        f"# Prerequisites (`{args.name}`)\n\n- Python >= 3.10\n",
        encoding="utf-8",
    )
    (base / "references" / "TROUBLESHOOTING.md").write_text(
        f"# Troubleshooting (`{args.name}`)\n\n| Symptom | Root Cause | Fix |\n|:---|:---|:---|\n| Example error | Cause | Fix |\n",
        encoding="utf-8",
    )

    print(f"[OK] Scaffolded 10-part skill '{args.name}' in {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
