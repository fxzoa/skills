# Acceptance Checklist (`colab-notebook`)

- [ ] `python3 scripts/validate_colab_bundle.py <dir> <notebook.ipynb>` exits `0`.
- [ ] Rule.13: External `.env` only (no `%%writefile .env`, no `google.colab.userdata`, no default fallbacks).
- [ ] 主要フェーズ（環境構築、モジュール生成、サーバー起動、トンネル起動、ログ監視）の見出し Markdown セルに、コードセルの内容を箇条書きで明記。
- [ ] Isolated `uv venv` (`/tmp/.venv`); no system `pip install`.
- [ ] `server.py` thin (`include_router` only); `routers/{health,status,chat,models}.py` separated.
- [ ] `README.html` (Rule.11 / Rule.14) and `http.rest` (`{{$dotenv ...}}`) present.

- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
