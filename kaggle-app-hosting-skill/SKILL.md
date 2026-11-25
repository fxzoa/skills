---
name: kaggle-app-hosting
description: Deploy CPU-only (No-Docker) persistent web apps and workers on Kaggle Cloud with Private Dataset .env/SQLite sync and Cloudflare Tunnel exposure.
---

# Skill: Kaggle Cloud CPU App Hosting & Persistent Sync Standards

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Deploy CPU-only (`enable_gpu: false`, `enable_tpu: false`, `enable_internet: true`) persistent services on Kaggle Cloud (for GPU LLM servers, use `kaggle-notebook`).

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_app_hosting` | `python3 scripts/scaffold_app_hosting.py --dir <dir> --owner <user> --slug <slug> [--notebook-file <ipynb>] [--db-name <db>]` | Generates CPU-only `kernel-metadata.json`, `kaggle_private_dataset/` (with `sqlite3.backup()`), and `http.rest` with `-notebook` / `-dataset` suffixes. |
| `validate_app_hosting` | `python3 scripts/validate_app_hosting.py <kaggle_dir>` | Validates CPU-only metadata, `-notebook`/`-dataset` suffixes, Rule.13, JSON syntax, `%%writefile` Python AST, and companion files. |

## Workflow Calls
1. `scaffold_app_hosting(...)` → initialize `kaggle/`, `kaggle_private_dataset/`, and `http.rest` (raw skeletons in `templates/`).
2. Build the 10-cell `<app>_kaggle.ipynb`:
   - **Cells 1–4**: Pre-flight dump & dirs (`/tmp` for runtimes/venv/caches; `/kaggle/working` for `.env`, `data/*.db`, `scripts/`, `logs/`, `tunnel_url.*`) → external `.env` strict check (Rule.13) & DB restore → install runtime + `cloudflared` in `/tmp` → clone/install app.
   - **Cells 5–7**: `%%writefile` `scripts/sync_dataset.py` (`sqlite3.backup()` + `kaggle datasets version -r zip` at +60s then hourly, supporting `KAGGLE_API_TOKEN` & `kaggle.json`), `scripts/start_services.sh` (idempotent `pkill`/`fuser`, `nohup ... &`), and `scripts/healthcheck.py` (poll `127.0.0.1:<PORT>/health`, 30–90s).
   - **Cells 8–10**: Run `start_services.sh` + `healthcheck.py` → start Cloudflare Tunnel (`named` via `--token` or `quick` regex extract, saving `tunnel_url.txt`/`.json`) → `tail -n 30 -f` logs.
3. Generate `README.html` (Rule.11 / Rule.14) and `http.rest`, then run `validate_app_hosting(<kaggle_dir>)`.

## Operational Constraints & Traps
- **Inherited `kaggle-notebook` Standards**:
  - **Strict External `.env` (Rule.13)**: Never use `%%writefile .env` or `os.getenv("KEY", "default")`. Load `/kaggle/working/.env` → `/kaggle/input/<dataset-slug>/.env` → `.env`; pre-validate keys in `prepare_dataset.py` before upload.
  - **Isolation & Quiet Execution**: Use `UV_SYSTEM_PYTHON=0 uv venv` in `/tmp/`, run `uv cache clean`, clean temps in `try-finally`, and apply quiet flags (`apt-get -qq`, `uv pip -q`, `curl -fsSL`, `git -q`, `PYTHONWARNINGS="ignore"`).
  - **Logs & Companion Files**: Log requests with **JST (`UTC+9`)** and real IP (`CF-Connecting-IP` → `X-Forwarded-For` → `client.host`). Include `.gitignore` (`templates/.gitignore.tmpl`), `README.html` (Rule.11 / Rule.14 dual inline SVGs), and `http.rest` (all endpoints via `{{$dotenv ...}}`).
- **Named vs. Quick Tunnel**: For `named` only, require `TUNNEL_TOKEN` (`TUNNEL_MODE=named`), omit `TUNNEL_URL` from `.env`, and reference `https://{{$dotenv TUNNEL_HOSTNAME}}` in `http.rest`.
- **`kaggle datasets create` Trap**: May exit 0 with `already in use`; always use `kaggle datasets version -p <stage> -m "<msg>" -r zip` for updates.
- **GitHub Clone Security**: Use Public repos (or PAT) for unattended clone; gitignore `.env*` (`!.env.example`), `*.db*`, `logs/`, `tmp/`, `.venv/`, `tunnel_url.*` before publishing.
- **Running Output & Stop**: While `RUNNING` (`tail -f`), `kaggle kernels output` won't expose live files—check Kaggle UI Logs tab or Private Dataset download. Stop kernels via Kaggle Web UI (**Cancel Run**).

## Trigger & Exit Criteria
- **Trigger**: Deploying CPU-only persistent web apps/workers on Kaggle Cloud with Private Dataset sync.
- **Exit Criteria**: `validate_app_hosting(<kaggle_dir>)` exits `0`, Tunnel responds HTTP 200, and `sync_dataset.py` backs up state cleanly.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never enable GPU/TPU (`enable_gpu: false, enable_tpu: false`), never use `kaggle datasets create` for updates, and never expose `.env` / `*.db` in Public repos (use `templates/.gitignore.tmpl`).
