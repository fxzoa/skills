# Trigger & Smoke Test Reference (`kaggle-app-hosting`)

## Positive Trigger Examples
1. **CPU-Only Persistent Web App**: "Deploy a CPU-only FastAPI + SQLite web app on Kaggle Cloud with Private Dataset sync and Cloudflare Tunnel."
2. **Background Worker / Bot Hosting**: "Set up a Kaggle No-Docker CPU notebook that restores `.env` and `data/*.db` from a Private Dataset and backs up hourly via `sqlite3.backup()`."
3. **App Hosting Bundle Validation**: "Validate `kernel-metadata.json` (`enable_gpu: false`), `-notebook`/`-dataset` suffixes, and `http.rest` in my Kaggle app bundle."

## Negative Trigger Examples
1. **GPU LLM Inference on Kaggle**: "Deploy a T4 x2 `llama.cpp` or `vLLM` server on Kaggle Cloud." → Use `kaggle-notebook`.
2. **Google Colab Notebook**: "Build a Colab Studio inference notebook with `uv venv`." → Use `colab-notebook`.
3. **Colab CLI Session Control**: "Provision and monitor a Colab VM using `colab` CLI." → Use `colab-operator`.

## Smoke Test
1. Verify CLI help exits cleanly:
   ```bash
   python3 -B scripts/validate_app_hosting.py --help
   python3 -B scripts/scaffold_app_hosting.py --help
   ```
2. Scaffold a temporary CPU app hosting bundle:
   ```bash
   python3 -B scripts/scaffold_app_hosting.py --dir /tmp/test_kaggle_app --owner testuser --slug myapp
   ```
3. Run bundle validation on a complete Kaggle CPU app directory:
   ```bash
   python3 -B scripts/validate_app_hosting.py <kaggle_dir>
   ```
   Expected: exits `0` with `[OK] Validated App Hosting bundle: ...`.
