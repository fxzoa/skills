# Tools & Interfaces Reference (`kaggle-operator`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `kaggle-operator`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `deploy_kaggle.py` | Deterministic deployment of kernels to Kaggle Cloud | `python3 scripts/deploy_kaggle.py <dir>` | `0`: Success, `1`: Failure |
| `schedule_kaggle_monitor.py` | Autonomous scheduler for polling kernel runs | `python3 scripts/schedule_kaggle_monitor.py` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `check_kaggle_run.sh` | Fetch kernel status and execution error logs | `bash scripts/check_kaggle_run.sh <kernel>` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `schedule` | Cron-based autonomous watchdog for long-running Kaggle jobs | Skill execution protocol |
| `run_command` | Execute deployment scripts and self-healing error analysis | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `Kaggle Kernels & Output API` | External Integration | Retrieve live output logs and execution error traces |

