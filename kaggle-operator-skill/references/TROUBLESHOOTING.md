# Troubleshooting (`kaggle-operator`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `403 Client Error: Forbidden` on `models get` / `datasets status` | Resource does not exist yet on Kaggle Cloud | `deploy_kaggle.py` auto-runs `publish_kaggle_model.sh` / `publish_kaggle_dataset.sh create` |
| `409 Conflict` on `kernels push` | `id` slug and `title` mismatch in `kernel-metadata.json` | Ensure `id: "<owner>/<slug>-notebook"` and `title: "<slug>-notebook"` match |
| `ModuleNotFoundError: huggingface_hub` on local host | Host `python3` lacks `huggingface_hub` | `download_model.py` falls back to `curl -fSL -C -` automatically |
| `Read-only file system: ~/.config/kaggle` in sandbox | Sandbox blocks `~/.config/kaggle` & network | Run `kaggle` CLI commands with `BypassSandbox: true` |
