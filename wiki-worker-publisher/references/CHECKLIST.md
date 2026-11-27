# Acceptance Checklist (`wiki-worker-publisher`)

- [ ] All 11 standard parts exist (`SKILL.md`, `scripts/`, `prototype/PROTOTYPE.md`, `templates/.gitignore.tmpl`, `references/{ARCHITECTURE,CHECKLIST,GUIDE,PREREQUISITES,TOOLS,TRIGGERS,TROUBLESHOOTING}.md`).
- [ ] `SKILL.md` frontmatter `name` matches directory name (`kebab-case`, <= 64 chars) and `description` covers What / When / Negative triggers (<= 1024 chars).
- [ ] `SKILL.md` is concise (< 500 lines) with valid internal relative links.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
- [ ] `references/TRIGGERS.md` defines Positive & Negative trigger prompt examples.
- [ ] `references/TOOLS.md` covers Command, Shell, MCP, and 外部 API.
- [ ] `prototype/PROTOTYPE.md` clarifies reusable vs project-specific parts.
- [ ] Scripts pass `validate_skill.py` (syntax, `--help`, and structure checks).
