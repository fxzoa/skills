# Acceptance Checklist (`kaggle-operator`)

- [ ] `kernel-metadata.json` `id` and `title` match and end with `-notebook`.
- [ ] All `dataset_sources` and `model_sources` verified or created on Kaggle Cloud before `kaggle kernels push`.
- [ ] `python3 scripts/deploy_kaggle.py <kaggle_dir>` succeeds without `403`/`409` errors.
- [ ] `bash scripts/check_kaggle_run.sh <kaggle_dir>` confirms `KernelWorkerStatus.COMPLETE`.
- [ ] All `http.rest` endpoints (`/healthz`, `/api/v1/status`, `/v1/models`, `/v1/chat/completions`) verified.

- [ ] `references/TOOLS.md` strictly covers all 4 tool classifications: **Command**, **Shell**, **MCP**, and **外部 API**.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
