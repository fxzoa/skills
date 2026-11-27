# Colab Operator Prototype Architecture

This directory holds reference environment configuration (`.env.example`) for operating remote Google Colab GPU/TPU sessions via the `colab` CLI.

## Reusable Core Design vs. Project-Specific Replacements

| Layer / Component | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Project) |
|:---|:---|:---|
| **Session Provisioning** | `scripts/deploy_colab.sh` idempotent session creation, file upload, and headless `colab exec` execution | Session name (`<session>`), GPU tier (`T4`, `L4`, `A100`), and target `.ipynb` or `.py` payload |
| **Autonomous Monitoring** | `scripts/schedule_colab_monitor.py` periodic status/log polling and error classification (OOM, port conflict, missing CUDA libs) | Polling interval (`-i`), health check endpoint URL (`-u`), and project-specific log patterns |
| **Self-Healing Loop** | Deterministic patch-and-redeploy cycle for OOM (`N_GPU_LAYERS`, quantization), port freeing (`fuser -k -n tcp`), and `LD_LIBRARY_PATH` | Model quantization parameters, VRAM limits, and application-specific recovery thresholds |
| **Auth & Secrets** | Headless-only CLI discipline + ADC (`gcloud auth application-default login`) verification via `colab whoami` | External `.env` file uploaded to `/content/.env`, `TUNNEL_TOKEN`, `LLM_API_KEY`, and Google Cloud project/account credentials |
| **Lifecycle Teardown** | `scripts/stop_colab.sh` (`colab stop`) and `http.rest` endpoint verification (`/healthz`, `/api/v1/status`, `/v1/models`) | Verification endpoints and post-run artifact download paths |
