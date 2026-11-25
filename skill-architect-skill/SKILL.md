---
name: skill-architect
description: Scaffold and validate standardized Antigravity skills with scripts/, prototype/, templates/, and references/ (Architecture, Checklist, Guide, Prerequisites, Troubleshooting, Tools), and sync to external /mnt/d/skills.
---

# Skill Architect Standards

Create, standardize, and validate reusable agent skills via pre-built scripts in `scripts/`.
All tool interfaces, CLI options, and classifications are formally specified in [references/TOOLS.md](references/TOOLS.md).

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control

> [!IMPORTANT]
> **Probabilistic Prompt-driven Orchestration is strictly prohibited for procedural workflows.**
> When an agent relies on prompt instructions to manually synthesize multi-step shell commands, parse unstructured text, or guess operational parameters, it introduces probabilistic failure modes.
> 
> **Architectural Imperative**:
> Any workflow step requiring reasoning, file manipulation, environment checking, remote transport, or health verification **MUST be materialized and codified into a deterministic, single-command Python script (`scripts/*.py`)**. The agent's role is to invoke the deterministic tool and inspect its verified output—not to execute the procedure manually.

## Pre-Built Operations (`scripts/`)

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `scaffold_skill` | `python3 scripts/scaffold_skill.py --dir <dir> --name <name> --desc "<desc>"` | Generates the full 10-part skill skeleton (`SKILL.md`, `scripts/`, `prototype/`, `templates/.gitignore.tmpl`, `references/{ARCHITECTURE,CHECKLIST,GUIDE,PREREQUISITES,TROUBLESHOOTING,TOOLS}.md`). | [TOOLS.md#11](references/TOOLS.md#11-scaffold_skillpy) |
| `validate_skill` | `python3 scripts/validate_skill.py <skill_dir>` | Validates presence of all 10 standard parts, Mermaid diagrams in `ARCHITECTURE.md`, 4-part categories in `TOOLS.md`, and syntax of all scripts. | [TOOLS.md#12](references/TOOLS.md#12-validate_skillpy) |

## Standard Skill Resource Layout (10-Part Standard)
```text
<skill-name>/
├── SKILL.md                        # Concise instructions + Core Philosophy + function-call table + Trigger/Exit + Anti-Patterns
├── scripts/                        # Deterministic automation scripts/tools (materializing prompt procedures into code)
├── prototype/                      # Minimal concrete folder/file skeleton
├── templates/                      # .gitignore.tmpl + parameterized *.tmpl skeletons
└── references/
    ├── TOOLS.md                    # Tool interfaces classified by Command, Shell, MCP, and 外部 API
    ├── ARCHITECTURE.md             # Mermaid architecture & sequence diagrams + env/API table + deliverables
    ├── CHECKLIST.md                # Acceptance checklist (including deterministic script verification)
    ├── GUIDE.md                    # Step-by-step creation/operation guide
    ├── PREREQUISITES.md            # Required tools, versions, and credentials
    └── TROUBLESHOOTING.md          # Known errors, root causes, and fixes
```

## Workflow Calls
1. `scaffold_skill(--dir, --name, --desc)` → generate standard 10-part skeleton.
2. Identify procedural steps and **codify them into deterministic Python scripts** in `scripts/`.
3. Populate `prototype/` and `references/` (including 4-category `TOOLS.md`).
4. `validate_skill(<skill_dir>)` → must exit `0` before syncing to `/mnt/d/skills/<skill-name>-skill/`.

## Trigger & Exit Criteria
- **Trigger**: Creating a new skill or auditing/standardizing an existing skill.
- **Exit Criteria**: `validate_skill(<skill_dir>)` exits `0`, all procedural operations are codified in `scripts/`, and external `/mnt/d/skills/<skill-name>-skill` matches via `diff -u`.

## Anti-Patterns
- **Never rely on Probabilistic Prompt-driven Orchestration**: Do not leave procedural steps for the agent to manually synthesize ad-hoc shell commands or reason out interactively. Materialize them into deterministic `scripts/*.py`.
- **Never leave verbose prose instructions where a `scripts/` call or table belongs.**
- **Never omit `references/TOOLS.md` or skip the 4 tool categories (`Command`, `Shell`, `MCP`, `外部 API`).**
- **Never omit `templates/.gitignore.tmpl`, `references/TROUBLESHOOTING.md`, or Mermaid diagrams in `references/ARCHITECTURE.md`.**
