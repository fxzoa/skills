# Troubleshooting (`create-new-skill`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `chmod` fails on `~/.gemini/...` in sandbox | Home config dir is read-only to shell in sandbox | Run `chmod +x` on `/mnt/d/skills/` copy or use `python3 script.py` |
| `validate_skill.py` fails on `ARCHITECTURE.md` | Missing Mermaid code fence | Add `flowchart` and `sequenceDiagram` blocks |
