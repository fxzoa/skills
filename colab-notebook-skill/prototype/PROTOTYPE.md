# Colab Studio Prototype Architecture

This directory holds reference skeletons (`.env.example`, `http.rest`) for building Google Colab Studio inference notebooks.

## Reusable Core Design vs. Project-Specific Replacements

| Layer / Component | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Project) |
|:---|:---|:---|
| **Notebook Lifecycle** | 24-step single-responsibility cell structure (`nvidia-smi` → `.env` check → `uv venv` → `%%writefile` modules → Uvicorn → Tunnel → `tail -f` final cell) | Model download commands, system `apt-get` packages, and inference engine flags (`llama-server`, `vLLM`, `transformers`) |
| **Environment & Secrets** | Strict external `.env` validation (Rule.13: halt on missing/empty keys, no `%%writefile .env`, no `google.colab.userdata`, no default fallbacks) | Actual `.env` values (`TUNNEL_HOST`, `TUNNEL_PORT`, `TUNNEL_HOSTNAME`, `TUNNEL_TOKEN`, `LLM_API_KEY`, `MODEL_NAME`, `KEEP_ALIVE_MINUTES`) |
| **Server & Routing** | Thin `server.py` (`include_router` only), `core/{config,logger,state,engine}.py`, `routers/{health,status,chat,models}.py`, JST (`UTC+9`) + real IP logging | Feature-specific routers (e.g., `/v1/embeddings`, `/v1/audio`), custom `ServerState` fields, and engine-specific request/response adapters |
| **Companion Files** | `http.rest` using `{{$dotenv ...}}` dynamic variables, `README.html` (Rule.11/14 dual inline SVGs), `.gitignore` | Endpoint payloads in `http.rest`, project-specific architecture diagrams, and sample model names |
| **Streaming Keep-Alive** | Final cell `tail -f` / `SEEK_END` streaming log monitor with `KEEP_ALIVE_MINUTES` timeout and graceful `KeyboardInterrupt` | Log file path (`logs/server.log` vs. multi-process logs) and session timeout duration |
