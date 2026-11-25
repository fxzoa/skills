# Operation Guide (`create-new-skill`)

This guide explains how to design, scaffold, codify, validate, and sync reusable Antigravity skills.

---

## 1. Skill Creation Lifecycle

### Phase 1: Scaffolding
Generate the standardized 11-part skill skeleton:
```bash
python3 scripts/scaffold_skill.py \
  --dir /path/to/skills/<skill-name> \
  --name <skill-name> \
  --desc "Describes what the skill does in third person. Use when <trigger condition>. Do not use for <negative trigger>."
```

### Phase 2: Deterministic Codification (Core Principle)
- **Identify Manual / Probabilistic Steps**: Review what shell commands, environment checks, file transformations, or health polling the agent performs.
- **Implement Single-Command Tools**: Encapsulate those steps into robust, deterministic Python scripts inside `scripts/` (e.g. `scripts/deploy_compose.py`).
- **Enforce Determinism**: Ensure scripts handle pre-flight checks, strict error handling, `--help` support, and structured output. Avoid delegating operational reasoning back to the LLM prompt.

### Phase 3: Specification, Triggers & Classification
- Document all tool interfaces in `references/TOOLS.md` categorized into **Command**, **Shell**, **MCP**, and **外部 API**.
- Detail system diagrams in `references/ARCHITECTURE.md` using Mermaid.
- Define **Positive / Negative Trigger Examples** and smoke test criteria in `references/TRIGGERS.md`.
- Capture operational edge cases and fixes in `references/TROUBLESHOOTING.md`.
- Keep `SKILL.md` under 500 lines as a clean navigation index.

### Phase 4: Validation & Sync
Validate the complete 11-part bundle and sync deterministically via `sync_skill.py`:
```bash
# 1. Validate locally
python3 scripts/validate_skill.py /path/to/skills/<skill-name>

# 2. Dry-run diff against external directory
python3 scripts/sync_skill.py \
  --src /path/to/skills/<skill-name> \
  --dst /mnt/d/skills/<skill-name>-skill

# 3. Apply synchronization (add --delete if exact mirror is required)
python3 scripts/sync_skill.py \
  --src /path/to/skills/<skill-name> \
  --dst /mnt/d/skills/<skill-name>-skill \
  --apply
```
