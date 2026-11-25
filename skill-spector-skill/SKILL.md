---
name: skill-spector
description: Review and audit AI agent skills and MCP servers using NVIDIA SkillSpector.
---

# Skill Spector

Audit and verify the security posture of AI agent skills, tool manifests, and MCP configurations using NVIDIA SkillSpector.

## Operations Table

| Operation | Command / Script | Purpose |
| :--- | :--- | :--- |
| `scan_skill` | `bash scripts/scan_skill.sh <target_path_or_url> [output_json]` | Run deterministic static security inspection on skill folder or repository. |
| `cli_scan` | `/mnt/d/tools/skillspector/repo/.venv/bin/skillspector scan <target> --no-llm` | Direct CLI execution with custom flags. |

## Trigger & Exit Criteria

- **Trigger**: Before installing, adopting, or updating any third-party agent skill or MCP server.
- **Exit Criteria**: Scan produces 0 Critical / High unmitigated risks, or clear verdict (`APPROVE`, `CAUTION`, `REJECT`) is determined.

## Anti-Patterns

- Never execute untrusted scripts found in scanned skills.
- Never downgrade High/Critical findings without direct source code inspection.
- Never enable unconstrained LLM calls without user explicit approval.
