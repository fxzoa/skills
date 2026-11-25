# Trigger & Smoke Test Reference (`colab-notebook`)

## Positive Trigger Examples
1. **New Colab Inference Notebook**: "Create a Google Colab Studio notebook to serve a GGUF model with `llama-server`, FastAPI routers, Cloudflare Tunnel, and `http.rest`."
2. **Refactor Existing Colab Notebook**: "Update this `.ipynb` for Colab to use external `.env` validation (Rule.13), `uv venv` isolation, and a `tail -f` streaming log final cell."
3. **Colab Bundle Validation**: "Review and validate my Colab inference project bundle (`README.html`, `http.rest`, `.env.example`, `.ipynb`) before deployment."

## Negative Trigger Examples
1. **Remote Colab CLI Operations**: "Provision a Colab A100 VM, run `colab exec`, and monitor logs via `colab` CLI." → Use `colab-operator`.
2. **Kaggle GPU Inference**: "Deploy a T4 x2 LLM inference server on Kaggle Cloud via `kaggle kernels push`." → Use `kaggle-notebook`.
3. **Kaggle CPU Web App**: "Host a persistent CPU-only FastAPI + SQLite app on Kaggle Cloud." → Use `kaggle-app-hosting`.

## Smoke Test
1. Verify CLI help exits cleanly:
   ```bash
   python3 -B scripts/validate_colab_bundle.py --help
   python3 -B scripts/scaffold_colab_project.py --help
   ```
2. Scaffold a temporary bundle and inspect generated `.env.example` and `http.rest`:
   ```bash
   python3 -B scripts/scaffold_colab_project.py --dir /tmp/test_colab --model-name test-model
   ```
3. Run bundle validation on a complete Colab project directory:
   ```bash
   python3 -B scripts/validate_colab_bundle.py <project_dir> <notebook.ipynb>
   ```
   Expected: exits `0` with `[OK] Validated Colab bundle: ...`.
