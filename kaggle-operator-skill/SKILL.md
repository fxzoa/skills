---
name: kaggle-operator
description: Operate Kaggle Cloud environments via the `kaggle` CLI: verify/publish dependencies, push notebooks, monitor execution via autonomous schedulers, and run a self-healing loop on errors.
---

# Skill: Kaggle Cloud Session & Deployment Operator

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Execute Kaggle Cloud operations via pre-built scripts in `scripts/`.

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `deploy_kaggle` | `python3 scripts/deploy_kaggle.py <kaggle_dir> [--model-work-dir <dir>]` | Verifies `dataset_sources` / `model_sources` on Kaggle Cloud, runs `publish_kaggle_dataset.sh create` / `publish_kaggle_model.sh` if missing, then runs `kaggle kernels push`. |
| `check_kaggle_run` | `bash scripts/check_kaggle_run.sh <kaggle_dir> [output_dir]` | Checks `kaggle kernels status` and downloads logs via `kaggle kernels output` on `ERROR` or `COMPLETE`. |
| `schedule_kaggle_monitor` | `python3 scripts/schedule_kaggle_monitor.py -k <kaggle_dir> [-o <out_dir>] [-i 30] [-u <health_url>]` | Periodic batch status scheduler that polls execution, downloads output logs, diagnoses errors (OOM 137, missing modules, 404), and triggers the self-healing loop. |

## Execution Constraints
- **Batch Mode (`papermill`)**: `kaggle kernels push` runs asynchronously (no persistent REPL); notebooks must use log snapshots instead of `while True:` to reach `KernelWorkerStatus.COMPLETE`.
- **Lightweight `/kaggle/working`**: Keep `.venv` and 20GB+ models in `/tmp/` so `kaggle kernels output` downloads only logs.

## Execution Pipeline
1. `deploy_kaggle(<kaggle_dir>)` — ensures all Dataset/Model dependencies exist on Kaggle Cloud, then pushes the notebook.
2. `schedule_kaggle_monitor(<kaggle_dir>, ...)` — execute periodic status & log checks using the pre-built scheduler script.
3. **Autonomous Self-Healing Loop (On Error)**:
   - When the scheduler detects OOM (Error 137), missing packages, or resource 404s:
   - Analyze downloaded diagnostic logs, patch notebook/config locally, and re-run `deploy_kaggle(...)`.
4. **On `COMPLETE`**: verify all endpoints in `http.rest` (`/healthz`, `/api/v1/status`, `/v1/models`, `/v1/chat/completions`, etc.) before reporting success.

## Trigger & Exit Criteria
- **Trigger**: Deploying or debugging a Kaggle notebook, model, or dataset via `kaggle` CLI.
- **Exit Criteria**: Dependencies exist on Kaggle Cloud, `schedule_kaggle_monitor` reaches `COMPLETE`, and all `http.rest` endpoints pass.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never run `kaggle kernels push` before verifying/creating `dataset_sources` and `model_sources`.
- Never ignore `409 Conflict` slug/title mismatches or store large model downloads in a small tmpfs `/tmp` (use `/mnt/d/tmp`).
- Never poll status ad-hoc without using the pre-built scheduler script (`schedule_kaggle_monitor.py`).
