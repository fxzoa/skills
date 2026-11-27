# Acceptance Checklist (`kaggle-notebook`)

- [ ] Directory matches `prototype/` layout (`kaggle/`, `kaggle_private_dataset/`).
- [ ] IDs use required suffixes: `-notebook` (`kernel-metadata.json`), `-dataset` (`dataset-metadata.json`).
- [ ] 主要フェーズ（環境構築、モジュール生成、サーバー起動、トンネル起動、ログ監視）の見出し Markdown セルに、コードセルの内容を箇条書きで明記。
- [ ] Models are downloaded directly to `/tmp/models/` (`model_sources: []` in `kernel-metadata.json`, no Kaggle Public Models).
- [ ] `python3 scripts/validate_kaggle_bundle.py <kaggle_dir>` exits `0`.
- [ ] Rule.13: No `%%writefile .env`, no `os.getenv(..., default)`, `LLM_API_KEY` printed unmasked.
- [ ] Heavy artifacts isolated to `/tmp/` (`VENV_DIR=/tmp/.venv`, `MODELS_DIR=/tmp/models`).
- [ ] `README.html` (Rule.11 / Rule.14 dual inline SVGs) and `http.rest` (`{{$dotenv ...}}`, all endpoints) present.
- [ ] No `while True:` loops at notebook end; batch run reaches `KernelWorkerStatus.COMPLETE`.

- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
