# Kaggle CPU App Hosting Prototype Architecture

This directory holds reference skeletons (`kaggle/kernel-metadata.json`, `kaggle/http.rest`) for deploying CPU-only persistent web apps and workers on Kaggle Cloud.

## Reusable Core Design vs. Project-Specific Replacements

| Layer / Component | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Project) |
|:---|:---|:---|
| **Kernel Metadata** | CPU-only flags (`enable_gpu: false`, `enable_tpu: false`, `enable_internet: true`), `-notebook` / `-dataset` ID suffixes | Owner username, project slug (`<owner>/<slug>-notebook`), and Private Dataset source slug (`<owner>/<slug>-dataset`) |
| **Storage & Isolation** | `/tmp` for `uv venv`, runtimes, and `cloudflared`; `/kaggle/working` for `.env`, `data/*.db`, `scripts/`, `logs/`, and `tunnel_url.*` | Application repository URL, Python dependencies, and system packages |
| **State & DB Sync** | `scripts/sync_dataset.py` using `sqlite3.backup()` + `kaggle datasets version -r zip` (+60s initial, then hourly) | SQLite database filename (`--db-name`), dataset staging directory, and `KAGGLE_API_TOKEN` / `kaggle.json` credentials |
| **Environment & Tunnel** | Strict external `.env` loading (`/kaggle/working/.env` → `/kaggle/input/<dataset-slug>/.env` → `.env`), `named` or `quick` Cloudflare Tunnel | App-specific `.env` secrets, `TUNNEL_TOKEN` / `TUNNEL_HOSTNAME` (for named tunnel), and `PORT` |
| **Companion Files** | `http.rest` (`{{$dotenv ...}}`), `README.html` (Rule.11/14 dual inline SVGs), `.gitignore` (`templates/.gitignore.tmpl`), `tail -f` final cell | App-specific API routes in `http.rest` and service healthcheck path (`/health`) |
