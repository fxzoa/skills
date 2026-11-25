---
name: kaggle-notebook
description: Build, deploy, and validate large LLM inference server bundles (FastAPI + Cloudflare Tunnel + mandatory tail -f final cell) on Kaggle GPU (T4 x2 / 32GB VRAM) via `kaggle kernels push`. Use when creating or reviewing Kaggle GPU LLM inference notebooks. Do NOT use for CPU-only Kaggle web apps (use kaggle-app-hosting) or Google Colab notebooks (use colab-notebook / colab-operator).
---

# Kaggle LLM Studio Standards

## Core Principles: 最上位設計原則
1. **Deterministic Code-driven Control over Probabilistic Control**:
   Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution. All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.
2. **Mandatory `tail -f` Streaming Log Final Cell (最上位必須要件)**:
   重要機能（FastAPI サーバー、llama-server、Cloudflare Tunnel 等）がバックグラウンドプロセスとして起動している場合、**ノートブックの最終セルはスナップショットで即終了してはならず、必ず重要機能のログを `tail -f` 形式（ストリーミング監視）で表示し続ける実装**にすること。
   - `KEEP_ALIVE_MINUTES`（外部 `.env` 連動、Kaggle 上限考慮）によるセッション維持。
   - クライアントアクセス、実IP、推論レイテンシの可視化。
   - セル手動停止（`KeyboardInterrupt`）時にバックグラウンドプロセスを道連れにせずログ監視のみをクリーンに終了するグレースフル制御。

Execute standard Kaggle bundle tasks via pre-built scripts in `scripts/` instead of manual boilerplate generation.

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_kaggle_project` | `python3 scripts/scaffold_kaggle_project.py --dir <dir> --owner <user> --slug <slug> --hf-repo <repo> --model-file <file> [--notebook-file <ipynb>] [--instance-slug <inst>]` | Generates `kernel-metadata.json`, `kaggle_public_model/`, `kaggle_private_dataset/`, and `http.rest` with `-notebook` / `-model` / `-dataset` suffixes. |
| `validate_kaggle_bundle` | `python3 scripts/validate_kaggle_bundle.py <kaggle_dir>` | Validates ID suffixes, JSON syntax, `%%writefile` Python AST, Rule.13 compliance, mandatory `tail -f` final cell, and required files (`README.html`, `http.rest`, `.env.example`). |
| `install_llama_cpp` | `bash scripts/install_llama_cpp.sh` | Installs official `ggml-org/llama.cpp` Ubuntu x64 CUDA 13 prebuilt binaries under `/opt/llama.cpp` (no CMake build). |

## Workflow Calls
1. `scaffold_kaggle_project(...)` → initialize directory layout (`18_strata_inkling2_mini/kaggle/` reference; raw skeletons in `templates/`).
2. Write `<name>_kaggle.ipynb` + `.env` / `.env.example` + `README.html` (via `readme-html-skill`, Rule.11 / Rule.14 dual inline SVGs) + `http.rest` (**final cell: mandatory `tail -f` streaming log cell**).
3. `validate_kaggle_bundle(<kaggle_dir>)` → must pass before handoff or push.

## Notebook Implementation Constraints
- **Isolation**: `VENV_DIR=/tmp/.venv` (`uv venv` + explicit `{VENV_DIR}/bin/python`), `MODELS_DIR=/tmp/models`; keep only code and `logs/` in `/kaggle/working`.
- **Env & Startup**: Dump OS, Python, `nvidia-smi`, `nvcc`, and engine versions first. Load external `.env` (`/kaggle/working/.env` → `/kaggle/input/<dataset-slug>/.env` → `.env`); forbid `%%writefile .env` and `os.getenv(..., default)`; print `LLM_API_KEY` unmasked.
- **Cells & Server**: One task per cell; use `%%writefile <path>` (no Python string writes). Bind FastAPI on `TUNNEL_PORT` and engine on `TUNNEL_PORT + 1`. Split `server.py` (`include_router` only) into `routers/{health,status,models,chat,<feature>}.py`.
- **Mandatory Final Cell Layout**: The final cell MUST implement `tail -f` streaming from `logs/server.log` (or main backend logs) using file seeking (`seek(0, os.SEEK_END)`) or loop reading with `KEEP_ALIVE_MINUTES` timeout and `KeyboardInterrupt` handling.
- **Resilience & Batch Exit**: Wrap model load in `try-except` → `ServerState` (`/api/v1/status`). Pre-free ports (`fuser -k -n tcp`, `pkill -9`), clean `/tmp` in `try-finally`, run `uv cache clean`. Use quiet flags (`-qq`, `-q`, `-fsSL`, `PYTHONWARNINGS="ignore"`), and JST (`UTC+9`) + real IP logs.
- **HF & Tunnel**: Verify HF filenames via `huggingface.co/api/models/<repo>/tree/main`. For Named Tunnel only, require `TUNNEL_TOKEN` and reference `https://{{$dotenv TUNNEL_HOSTNAME}}` in `http.rest` (omit `TUNNEL_URL`).

## Trigger & Exit Criteria
- **Trigger**: Creating, updating, or reviewing a Kaggle GPU LLM inference notebook bundle.
- **Exit Criteria**: `validate_kaggle_bundle(<kaggle_dir>)` exits `0` and `references/CHECKLIST.md` passes.

## Document Index
- [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) — Reusable Kaggle GPU LLM architecture vs. project-specific replacements.
- [references/TRIGGERS.md](references/TRIGGERS.md) — Positive/negative trigger examples and smoke tests.
- [references/TOOLS.md](references/TOOLS.md) — Detailed CLI interfaces for `scripts/`.
- [references/CHECKLIST.md](references/CHECKLIST.md) — Pre-delivery verification checklist.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- **Never terminate the notebook with a static log snapshot or empty completion cell**: If background servers are running, the final cell must always stream live logs.
- Never use `%%writefile .env`, `os.getenv(..., default)`, system `pip install`, CMake `llama.cpp` builds, or infinite unmonitored loops.
- Never store `.venv` or 20GB+ models in `/kaggle/working`, and never commit `.env` / secrets (use `templates/.gitignore.tmpl`).
