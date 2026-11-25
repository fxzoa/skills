# Acceptance Checklist (`kaggle-app-hosting`)

- [ ] `kernel-metadata.json` has `enable_gpu: false`, `enable_tpu: false`, `enable_internet: true`, and `-notebook` / `-dataset` suffixes.
- [ ] `python3 scripts/validate_app_hosting.py <kaggle_dir>` exits `0`.
- [ ] Heavy runtimes/caches isolated in `/tmp/`; only `.env`, `data/*.db`, `scripts/`, `logs/`, `tunnel_url.*` in `/kaggle/working`.
- [ ] `sync_dataset.py` uses `sqlite3.backup()` and `kaggle datasets version -r zip`.
- [ ] Rule.13: No `%%writefile .env`, no `os.getenv(..., default)`, `prepare_dataset.py` validates required keys.
- [ ] `.gitignore` (from `templates/.gitignore.tmpl`), `README.html` (Rule.11 / Rule.14), and `http.rest` (`{{$dotenv ...}}`) present.

- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
