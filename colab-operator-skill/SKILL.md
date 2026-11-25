---
name: colab-operator
description: Operate Google Colab environments via the `colab` CLI to provision GPU/TPU sessions, execute notebooks or scripts, monitor logs with autonomous schedulers, and run a self-healing loop on errors. Use when provisioning, running, monitoring, or stopping remote Colab VMs via CLI. Do NOT use for authoring Colab notebook code/cells (use colab-notebook) or Kaggle kernel deployments (use kaggle-notebook / kaggle-app-hosting).
---

# Skill: Colab Session Operator

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Operate Google Colab VMs via pre-built scripts in `scripts/`.

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `deploy_colab` | `bash scripts/deploy_colab.sh <session> <nb.ipynb\|script.py> [T4\|L4\|A100]` | Provisions named session (if missing), executes notebook/script remotely, and prints session status. |
| `check_colab_run` | `bash scripts/check_colab_run.sh <session>` | Fetches `colab status` and `colab log` for the active session. |
| `schedule_colab_monitor` | `python3 scripts/schedule_colab_monitor.py -s <session> [-i 15] [-u <health_url>]` | Periodic status & log scheduler that monitors progress, diagnoses errors (OOM, port conflict, missing modules), and triggers the self-healing loop. |
| `stop_colab` | `bash scripts/stop_colab.sh <session>` | Terminates the Colab VM session (`colab stop`) to stop compute unit billing. |

## Execution Constraints
- **Persistent Kernel**: Variables and state under `/content` persist across `colab exec` calls within the same `-s <session>`.
- **Headless Only**: Never run interactive commands (`colab repl`, `colab console`, `colab auth`, `colab drivemount`).
- **ADC Auth**: If auth expires, re-mint via `gcloud auth application-default login --scopes=openid,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/colaboratory` and verify with `colab whoami`.

## Execution Pipeline
1. `deploy_colab(<session>, <nb.ipynb>, <gpu>)` — ensure external `.env` is uploaded, then launch notebook.
2. `schedule_colab_monitor(<session>, ...)` — execute periodic status & log checks using the pre-built scheduler script.
3. **Autonomous Self-Healing Loop (On Error)**:
   - When the scheduler detects OOM (code -9 / cgroup OOM), port conflicts (`fuser -k -n tcp`), missing CUDA libs (`LD_LIBRARY_PATH`), or syntax errors:
   - Analyze diagnostics output, patch locally, re-deploy with adjusted parameters (e.g., lower quantization, adjusted `N_GPU_LAYERS`), and re-run.
4. **On Ready**: verify all endpoints in `http.rest` (`/healthz`, `/api/v1/status`, `/v1/models`, `/v1/chat/completions`). Always call `stop_colab(<session>)` when finished.

## Trigger & Exit Criteria
- **Trigger**: Provisioning, executing, or debugging a Colab GPU/TPU session via `colab` CLI.
- **Exit Criteria**: Notebook executes cleanly, scheduler confirms `ready`, `http.rest` checks pass, and `stop_colab(<session>)` terminates the VM.

## Document Index
- [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) — Reusable Colab CLI operator patterns vs. session-specific replacements.
- [references/TRIGGERS.md](references/TRIGGERS.md) — Positive/negative trigger examples and smoke tests.
- [references/TOOLS.md](references/TOOLS.md) — Detailed CLI interfaces for `scripts/`.
- [references/CHECKLIST.md](references/CHECKLIST.md) — Session verification and teardown checklist.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never invoke interactive CLI commands (`colab repl`, `colab console`, `colab auth`, `colab drivemount`).
- Never leave a rented GPU/TPU session running after verification completes.
- Never poll logs ad-hoc without using the pre-built scheduler script (`schedule_colab_monitor.py`).
