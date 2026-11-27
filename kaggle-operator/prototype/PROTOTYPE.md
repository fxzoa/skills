# PROTOTYPE.md: Reusable Core vs. Project-Specific Replacements (`kaggle-operator`)

This document defines the boundary between reusable core assets and project-specific replacements for `kaggle-operator`.

---

## 1. Prototype Structure

```text
prototype/
└── kernel-metadata.json   # Sample Kaggle kernel metadata (GPU, dataset sources, model_sources: [])
```

---

## 2. Reusable Core vs. Project-Specific Replacements

| Component | Reusable Core Design (Keep As-Is) | Project-Specific Replacements (Customize Per Project) |
|:---|:---|:---|
| **Deployment Pipeline (`scripts/deploy_kaggle.py`)** | Deterministic verification of `dataset_sources`, auto-publishing missing datasets, and `kaggle kernels push` orchestration. | `<kaggle_dir>` path and Kaggle account credentials (`~/.kaggle/kaggle.json`). |
| **Monitoring & Self-Healing (`scripts/schedule_kaggle_monitor.py`, `scripts/check_kaggle_run.sh`)** | Periodic status polling, automatic log download on `ERROR`/`COMPLETE`, and OOM (137) / 404 / missing-module diagnosis loop. | Output log directory (`-o`), polling interval (`-i`), and healthcheck endpoint URL (`-u`) matching your notebook's exposed server. |
| **Kernel Metadata (`prototype/kernel-metadata.json`, `templates/kernel-metadata.json.tmpl`)** | JSON schema (`kernel_type: notebook`, `enable_gpu`, `enable_internet`, `dataset_sources`, `model_sources: []`). | `id`, `title`, `code_file` (`.ipynb` filename), and specific `dataset_sources` slugs. |
| **Execution Constraints** | Batch `papermill` log-snapshot pattern (no `while True:` blocking), and storing `.venv` and downloaded models in Kaggle `/tmp/` to keep `/kaggle/working` lightweight. | Specific Python packages, model IDs, and API routes verified in `http.rest`. |
