# Trigger & Smoke Test Reference (`kaggle-notebook`)

## Positive Trigger Examples
1. **Kaggle GPU LLM Server**: "Build a Kaggle T4 x2 LLM inference notebook bundle with FastAPI, `llama-server`, Cloudflare Tunnel, and `kaggle_private_dataset`."
2. **Kaggle Bundle Scaffolding**: "Scaffold `kernel-metadata.json`, `kaggle_public_model/`, `kaggle_private_dataset/`, and `http.rest` with `-notebook`/`-model`/`-dataset` suffixes."
3. **Kaggle Notebook Validation**: "Validate my Kaggle GPU notebook bundle for Rule.13 compliance, `%%writefile` Python AST, and mandatory `tail -f` final cell."

## Negative Trigger Examples
1. **Kaggle CPU-Only Web App**: "Host a CPU-only (`enable_gpu: false`) SQLite web app on Kaggle Cloud." → Use `kaggle-app-hosting`.
2. **Google Colab Notebook**: "Create a Colab Studio inference notebook." → Use `colab-notebook`.
3. **Colab CLI Operations**: "Start and monitor a Colab VM via `colab` CLI." → Use `colab-operator`.

## Smoke Test
1. Verify CLI help exits cleanly:
   ```bash
   python3 -B scripts/validate_kaggle_bundle.py --help
   python3 -B scripts/scaffold_kaggle_project.py --help
   ```
2. Scaffold a temporary Kaggle GPU bundle:
   ```bash
   python3 -B scripts/scaffold_kaggle_project.py --dir /tmp/test_kaggle_gpu --owner testuser --slug myllm --hf-repo org/repo --model-file model.gguf
   ```
3. Run bundle validation on a complete Kaggle GPU bundle directory:
   ```bash
   python3 -B scripts/validate_kaggle_bundle.py <kaggle_dir>
   ```
   Expected: exits `0` with `[OK] Validated Kaggle bundle: ...`.
