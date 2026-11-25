# Tools & Interfaces Reference (`skill-architect`)

This document defines tool interfaces, CLI options, and execution protocols for the `skill-architect` skill.
Tools are organized into four execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_skill.py` | 10-part skill skeleton generator | `python3 scripts/scaffold_skill.py --dir <dir> --name <name> --desc "<desc>"` | `0`: Success |
| `validate_skill.py` | 10-part skill architecture linter | `python3 scripts/validate_skill.py <skill_dir>` | `0`: Valid, `1`: Invalid |

### 1.1 `scaffold_skill.py`
Generates the complete 10-part Antigravity skill skeleton including `references/TOOLS.md` with 4-category layout.
- **Arguments**:
  - `--dir`: Target directory for the new skill.
  - `--name`: Skill identifier name (kebab-case).
  - `--desc`: Concise one-line description for frontmatter.

### 1.2 `validate_skill.py`
Validates that a skill directory strictly adheres to standard files, directories, mermaid diagrams, and the 4 tool categories in `references/TOOLS.md`.
- **Arguments**:
  - `<skill_dir>`: Absolute or relative path to the skill directory.

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `rsync` | Mirror validated skill bundle to external directory | `rsync -av --delete <src>/ /mnt/d/skills/<name>-skill/` |
| `diff` | Verify exact byte-level parity between local & external | `diff -r <src> /mnt/d/skills/<name>-skill` |
| `chmod` | Ensure scripts have executable permissions | `chmod +x scripts/*.py` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Protocol |
|:---|:---|:---|
| `run_command` | Execute `scaffold_skill.py`, `validate_skill.py`, and `rsync` | Standard validation execution |
| `read_file` | Read existing skills, references, and checklists | Rule.16 Pre-Read enforcement |
| `write_file` / `edit_file` | Populate scripts, templates, and reference docs | Safe code/document delivery |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol | Endpoint | Auth | Purpose |
|:---|:---|:---|:---|:---|
| N/A | - | - | - | `skill-architect` operates entirely via local file system and CLI scripts. |
