# Acceptance Checklist (`skill-architect`)

- [ ] All 10 standard parts exist (`SKILL.md`, `scripts/`, `prototype/`, `templates/.gitignore.tmpl`, `references/{TOOLS,ARCHITECTURE,CHECKLIST,GUIDE,PREREQUISITES,TROUBLESHOOTING}.md`).
- [ ] **Deterministic Codification**: Procedural workflow steps are materialized into single-command Python scripts in `scripts/` rather than relying on prompt-driven probabilistic shell execution.
- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] `references/ARCHITECTURE.md` contains valid Mermaid diagrams (`flowchart` and `sequenceDiagram`).
- [ ] `scripts/*.py` pass python syntax compilation (`py_compile`).
- [ ] `validate_skill.py` exits `0` with zero errors.
- [ ] External `/mnt/d/skills/<skill-name>-skill/` matches local skill bundle with zero `diff -r` divergence.
