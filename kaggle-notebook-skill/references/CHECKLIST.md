# Acceptance Checklist (`kaggle-notebook`)

- [ ] Directory matches `prototype/` layout (`kaggle/`, `kaggle_public_model/`, `kaggle_private_dataset/`).
- [ ] IDs use required suffixes: `-notebook` (`kernel-metadata.json`), `-model` (`model-metadata.json`), `-dataset` (`dataset-metadata.json`).
- [ ] `python3 scripts/validate_kaggle_bundle.py <kaggle_dir>` exits `0`.
- [ ] Rule.13: No `%%writefile .env`, no `os.getenv(..., default)`, `LLM_API_KEY` printed unmasked.
- [ ] Heavy artifacts isolated to `/tmp/` (`VENV_DIR=/tmp/.venv`, `MODELS_DIR=/tmp/models`).
- [ ] `README.html` (Rule.11 / Rule.14 dual inline SVGs) and `http.rest` (`{{$dotenv ...}}`, all endpoints) present.
- [ ] No `while True:` loops at notebook end; batch run reaches `KernelWorkerStatus.COMPLETE`.

- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
