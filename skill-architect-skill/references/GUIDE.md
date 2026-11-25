# Operation Guide (`skill-architect`)

This guide explains how to design, scaffold, codify, and validate reusable Antigravity skills.

---

## 1. Skill Creation Lifecycle

### Phase 1: Scaffolding
Generate the standardized 10-part skill skeleton:
```bash
python3 scripts/scaffold_skill.py \
  --dir /path/to/skills/<skill-name> \
  --name <skill-name> \
  --desc "Clear one-line description"
```

### Phase 2: Deterministic Codification (Core Principle)
- **Identify Manual / Probabilistic Steps**: Review what shell commands, environment checks, file transformations, or health polling the agent performs.
- **Implement Single-Command Tools**: Encapsulate those steps into robust, deterministic Python scripts inside `scripts/` (e.g. `scripts/deploy_compose.py`).
- **Enforce Determinism**: Ensure scripts handle pre-flight checks, strict error handling, and structured JSON output. Avoid delegating operational reasoning back to the LLM prompt.

### Phase 3: Specification & Classification
- Document all tool interfaces in `references/TOOLS.md` categorized into **Command**, **Shell**, **MCP**, and **外部 API**.
- Detail system diagrams in `references/ARCHITECTURE.md` using Mermaid.
- Capture operational edge cases and fixes in `references/TROUBLESHOOTING.md`.

### Phase 4: Validation & Sync
Validate the complete 10-part bundle and sync to external repository:
```bash
# 1. Validate
python3 scripts/validate_skill.py /path/to/skills/<skill-name>

# 2. Mirror to external
rsync -av --delete /path/to/skills/<skill-name>/ /mnt/d/skills/<skill-name>-skill/

# 3. Verify byte parity
diff -r /path/to/skills/<skill-name> /mnt/d/skills/<skill-name>-skill
```
