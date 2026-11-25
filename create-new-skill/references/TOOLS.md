# Tools & Interfaces Reference (`create-new-skill`)

This document defines tool interfaces, CLI options, and execution protocols for the `create-new-skill` skill.
Tools are organized into four execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_skill.py` | 11-part skill skeleton generator | `python3 scripts/scaffold_skill.py --dir <dir> --name <name> --desc "<desc>"` | `0`: Success, `1`: Failure |
| `validate_skill.py` | 11-part skill architecture & standard linter | `python3 scripts/validate_skill.py <skill_dir>` | `0`: Valid, `1`: Invalid |
| `sync_skill.py` | Validate, diff, and safely mirror skill bundle | `python3 scripts/sync_skill.py --src <dir> --dst <dir> [--apply] [--delete]` | `0`: Synced/Clean, `1`: Error |

### 1.1 `scaffold_skill.py`
Generates the complete 11-part Antigravity skill skeleton including `references/TRIGGERS.md` and `references/TOOLS.md` with 4-category layout.
- **Arguments**:
  - `--dir`: Target directory for the new skill.
  - `--name`: Skill identifier name (`kebab-case`, <= 64 chars, must match directory basename).
  - `--desc`: Trigger-optimized description (What, When, Negative triggers; <= 1024 chars).

### 1.2 `validate_skill.py`
Validates that a skill directory strictly adheres to Agent Skills standards and Antigravity conventions, collecting and reporting all errors at once:
- YAML frontmatter (`name`, `description` length/format, `name` == directory name)
- `SKILL.md` line count (< 500 lines) and required sections
- Relative Markdown link integrity (no broken links or `../` directory escapes)
- Required directories & 11-part files (including `references/TRIGGERS.md`)
- Mermaid diagrams in `references/ARCHITECTURE.md` and 4 tool categories in `references/TOOLS.md`
- Python syntax compilation (`py_compile`) and `--help` smoke check for `scripts/*.py`
- **Arguments**:
  - `<skill_dir>`: Absolute or relative path to the skill directory.

### 1.3 `sync_skill.py`
Runs `validate_skill.py` on `--src`, compares files against `--dst`, and optionally applies synchronization.
- **Arguments**:
  - `--src`: Source skill directory.
  - `--dst`: Target destination skill directory (e.g. `/mnt/d/skills/<name>-skill`).
  - `--apply`: Copy new and modified files to `--dst`.
  - `--delete`: Remove files present only in `--dst` (requires `--apply`).
  - `--skip-validation`: Skip pre-sync `validate_skill.py` check.

---

## 2. Shell コマンド (OS & Infrastructure)

> [!NOTE]
> スキル同期は原則として `scripts/sync_skill.py` を使用してください（アドホックな `rsync` / `diff` の手動実行は非推奨）。

| Shell Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `python3` | Run deterministic `scripts/*.py` operators | `python3 scripts/validate_skill.py <skill_dir>` |
| `chmod` | Ensure scripts have executable permissions | `chmod +x scripts/*.py` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Protocol |
|:---|:---|:---|
| `run_command` | Execute `scaffold_skill.py`, `validate_skill.py`, and `sync_skill.py` | Standard validation & sync execution |
| `read_file` | Read existing skills, references, and checklists | Rule.16 Pre-Read enforcement |
| `write_file` / `edit_file` | Populate scripts, templates, and reference docs | Safe code/document delivery |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol | Endpoint | Auth | Purpose |
|:---|:---|:---|:---|:---|
| N/A | - | - | - | `create-new-skill` operates entirely via local file system and CLI scripts. |
