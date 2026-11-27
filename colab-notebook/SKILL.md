---
name: colab-notebook
description: Build and validate Google Colab Studio inference notebooks with external .env validation (Rule.13), single-responsibility %%writefile cells, uv venv isolation, router separation, companion README.html / http.rest, and a mandatory tail -f streaming log final cell. Use when creating, updating, or reviewing Colab inference .ipynb bundles. Do NOT use for remote Colab CLI session control (use colab-operator) or Kaggle deployments (use kaggle-notebook / kaggle-app-hosting).
---

# Colab Studio Notebook Standards

## Core Principles: 最上位設計原則
1. **Deterministic Code-driven Control over Probabilistic Control**:
   Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution. All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.
2. **Mandatory `tail -f` Streaming Log Final Cell (最上位必須要件)**:
   重要機能（FastAPI サーバー、llama-server、Cloudflare Tunnel 等）がバックグラウンドプロセスとして起動している場合、**ノートブックの最終セルはスナップショットで即終了してはならず、必ず重要機能のログを `tail -f` 形式（ストリーミング監視）でリアルタイム表示し続ける実装**にすること。
   - `KEEP_ALIVE_MINUTES`（外部 `.env` 連動）によるセッション維持と Colab の無通信切断防止。
   - クライアントアクセス、実IP、推論レイテンシの可視化。
   - セル手動停止（`KeyboardInterrupt`）時にバックグラウンドプロセスを道連れにせずログ監視のみをクリーンに終了するグレースフル制御。

Execute standard Colab Studio scaffolding and validation via pre-built scripts in `scripts/`.

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_colab_project` | `python3 scripts/scaffold_colab_project.py --dir <dir> --model-name <model>` | Generates `.env.example` and `http.rest` (`{{$dotenv ...}}` dynamic references). |
| `validate_colab_bundle` | `python3 scripts/validate_colab_bundle.py <dir> <notebook.ipynb>` | Validates Rule.13 (`no %%writefile .env`, no `google.colab.userdata`), JSON syntax, `%%writefile` Python AST, mandatory `tail -f` final cell, and companion files. |
| `install_llama_cpp` | `bash scripts/install_llama_cpp.sh` | Installs official `ggml-org/llama.cpp` Ubuntu x64 CUDA 13 prebuilt binaries under `/opt/llama.cpp` (no CMake source build). |

## Workflow Calls
1. `scaffold_colab_project(--dir, --model-name)` → create `.env.example` and `http.rest` (raw skeletons in `templates/`), then populate external `.env`.
2. Build `<name>.ipynb` following the 24-step layout (`nvidia-smi` & resource check → external `.env` validation → `apt-get` / `cloudflared` / `uv venv` → `%%writefile` `core/{config,logger,state,engine}.py` & `routers/{health,status,chat,models}.py` & `server.py` → Uvicorn launch → `/api/v1/status` polling → Cloudflare Tunnel → API test → **mandatory `tail -f` live log streaming cell**).
3. Generate `README.html` (via `readme-html-skill`, Rule.11 / Rule.14 dual inline SVGs) and `http.rest` (all endpoints for local & tunnel).
4. `validate_colab_bundle(<dir>, <notebook.ipynb>)` → must pass before delivery.

## Implementation Constraints
- **External `.env` Only (Rule.13)**: Never use `%%writefile .env`, `google.colab.userdata`, or `os.getenv("KEY", "default")`. Halt if `TUNNEL_HOST`, `TUNNEL_PORT`, `TUNNEL_HOSTNAME`, `LLM_API_KEY`, or `MODEL_NAME` are missing; print `LLM_API_KEY` directly.
- **Isolation & No Source Build**: Use `UV_SYSTEM_PYTHON=0 uv venv --allow-existing --python {sys.executable} {VENV_DIR}` and run `{VENV_DIR}/bin/python` / `uvicorn`. For `llama.cpp`, use prebuilt CUDA wheels (`cu124` + `LD_LIBRARY_PATH`) or `install_llama_cpp()`.
- **Cells & Routers**: One task per cell; use `%%writefile <path>` (no Python string writes). Keep `server.py` thin (`include_router` only) and split `routers/{health,status,chat,models}.py`.
- **Markdown Phase Overview (必須要件)**: 主要フェーズ（「環境構築」「モジュール生成」「サーバー起動」「トンネル起動」「ログ監視」）の直前にある見出し Markdown セルには、**コードセルの実行内容と目的を箇条書き（Bullet Points）で明記すること**。これにより、Colab Studio の目次（TOC）および利用者が各セルの責務と挙動を即座に把握できるようにする。
- **Mandatory Final Cell Layout**: The final cell MUST implement `tail -f` streaming from `logs/server.log` (or main backend logs) using file seeking (`seek(0, os.SEEK_END)`) or loop reading with `KEEP_ALIVE_MINUTES` timeout and `KeyboardInterrupt` handling.
- **Resilience & Logging**: Catch model load exceptions into `ServerState` (`/api/v1/status`). Pre-free ports (`fuser -k -n tcp`, `pkill -9`), clean `/tmp` in `try-finally`, run `uv cache clean`, use quiet flags (`-qq`, `-q`, `-fsSL`, `PYTHONWARNINGS="ignore"`), and log requests with **JST (`UTC+9`)**, real client IP (`CF-Connecting-IP` → `X-Forwarded-For` → `client.host`), and 120-char input preview.

## Trigger & Exit Criteria
- **Trigger**: Creating, updating, or reviewing a Google Colab Studio inference notebook.
- **Exit Criteria**: `validate_colab_bundle(<dir>, <notebook.ipynb>)` exits `0` and `references/CHECKLIST.md` passes.

## Document Index
- [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) — Reusable Colab Studio architecture vs. project-specific replacements.
- [references/TRIGGERS.md](references/TRIGGERS.md) — Positive/negative trigger examples and smoke tests.
- [references/TOOLS.md](references/TOOLS.md) — Detailed CLI interfaces for `scripts/`.
- [references/CHECKLIST.md](references/CHECKLIST.md) — Pre-delivery verification checklist.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- **Never terminate the notebook with a static log snapshot or empty completion cell**: If background servers are running, the final cell must always stream live logs.
- Never use `%%writefile .env`, `google.colab.userdata`, `os.getenv(..., default)`, system `pip install`, or CMake `llama.cpp` source builds.
- Never write Python source files from string variables (`open().write()`); always use `%%writefile`.
