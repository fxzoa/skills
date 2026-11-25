# Acceptance Checklist (`create-new-skill`)

- [ ] All 11 standard parts exist (`SKILL.md`, `scripts/`, `prototype/PROTOTYPE.md`, `templates/.gitignore.tmpl`, `references/{ARCHITECTURE,CHECKLIST,GUIDE,PREREQUISITES,TOOLS,TRIGGERS,TROUBLESHOOTING}.md`).
- [ ] **Frontmatter Standard**: `SKILL.md` has valid YAML frontmatter with `name` (`kebab-case`, <= 64 chars, matching parent directory name) and `description` (<= 1,024 chars, third-person What / When / Negative Trigger).
- [ ] **Progressive Disclosure**: `SKILL.md` is concise (< 500 lines) and acts as a navigation index; all relative links resolve inside the skill directory.
- [ ] **Trigger Examples**: `references/TRIGGERS.md` defines Positive Trigger Examples, Negative Trigger Examples, and Smoke Test criteria.
- [ ] **Deterministic Codification**: Procedural workflow steps are materialized into single-command Python scripts in `scripts/` rather than relying on prompt-driven probabilistic shell execution.
- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] `references/ARCHITECTURE.md` contains valid Mermaid diagrams (`flowchart` and `sequenceDiagram`).
- [ ] `scripts/*.py` pass Python syntax compilation (`py_compile`) and `--help` execution.
- [ ] `python3 scripts/validate_skill.py <skill_dir>` exits `0` with zero errors.
- [ ] `python3 scripts/sync_skill.py --src <skill_dir> --dst /mnt/d/skills/<skill-name>-skill` reports 100% sync (exit `0`).
