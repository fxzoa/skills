# Troubleshooting (`kaggle-operator`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `403 Client Error: Forbidden` on `datasets status` | Resource does not exist yet on Kaggle Cloud | `deploy_kaggle.py` auto-runs `publish_kaggle_dataset.sh create` |
| `409 Conflict` on `kernels push` | `id` slug and `title` mismatch in `kernel-metadata.json` | Ensure `id: "<owner>/<slug>-notebook"` and `title: "<slug>-notebook"` match |
| `Read-only file system: ~/.config/kaggle` in sandbox | Sandbox blocks `~/.config/kaggle` & network | Run `kaggle` CLI commands with `BypassSandbox: true` |
