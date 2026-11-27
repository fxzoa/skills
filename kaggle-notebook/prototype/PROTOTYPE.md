# Kaggle GPU LLM Notebook Prototype Architecture

This directory holds reference skeletons (`kaggle/kernel-metadata.json`, `kaggle/http.rest`) for deploying GPU-accelerated LLM inference servers on Kaggle Cloud.

## Reusable Core Design vs. Project-Specific Replacements

| Layer / Component | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Project) |
|:---|:---|:---|
| **Bundle & Metadata** | `kernel-metadata.json`, `kaggle_private_dataset/`, and enforced `-notebook` / `-dataset` suffixes (`model_sources: []`) | Kaggle owner, slug, GPU configuration (`T4 x2`), and Hugging Face repo / model filename (`--hf-repo`, `--model-file`) |
| **Storage & Isolation** | `VENV_DIR=/tmp/.venv` (`uv venv`), `MODELS_DIR=/tmp/models` (direct download), `/kaggle/working` restricted to server code and `logs/` | Inference engine (`llama-server` CUDA 13 prebuilt, `vLLM`, `transformers`) and model weights |
| **Environment & Secrets** | Strict external `.env` loading (`/kaggle/working/.env` → `/kaggle/input/<dataset-slug>/.env` → `.env`, Rule.13), unmasked `LLM_API_KEY` check | Project `.env` secrets (`LLM_API_KEY`, `TUNNEL_TOKEN`, `TUNNEL_HOSTNAME`, `MODEL_NAME`, `KEEP_ALIVE_MINUTES`) |
| **Server & Streaming** | Thin `server.py` on `TUNNEL_PORT`, engine on `TUNNEL_PORT + 1`, `routers/{health,status,models,chat}.py`, mandatory `tail -f` final cell | Model-specific chat templates, custom feature routers, and `KEEP_ALIVE_MINUTES` (within Kaggle session limits) |
| **Companion Files** | `http.rest` (`{{$dotenv ...}}`), `README.html` (Rule.11/14 dual inline SVGs), `.gitignore` (`templates/.gitignore.tmpl`) | Model IDs and prompt payloads in `http.rest`, plus project-specific architecture SVGs |
