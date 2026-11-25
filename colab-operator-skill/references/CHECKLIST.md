# Acceptance Checklist (`colab-operator`)

- [ ] Named session created (`colab new -s <session>`).
- [ ] External `.env` uploaded to `/content/.env` before executing notebook.
- [ ] `bash scripts/check_colab_run.sh <session>` shows healthy server and tunnel logs.
- [ ] All `http.rest` endpoints verified.
- [ ] Session stopped via `bash scripts/stop_colab.sh <session>` after verification.

- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
