# Tools & Interfaces Reference (`colab-operator`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `colab-operator`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `schedule_colab_monitor.py` | Schedule autonomous polling monitor via cron/timer | `python3 scripts/schedule_colab_monitor.py` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `deploy_colab.sh` | Push notebook and start execution on Colab | `bash scripts/deploy_colab.sh <notebook>` |
| `check_colab_run.sh` | Poll run status and fetch execution logs | `bash scripts/check_colab_run.sh <run_id>` |
| `stop_colab.sh` | Halt running Colab session to prevent quota leakage | `bash scripts/stop_colab.sh <run_id>` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `schedule` | Trigger periodic health checks and log monitoring | Skill execution protocol |
| `run_command` | Execute deployment scripts and handle self-healing loop | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `Colab Session Management API` | External Integration | Start, monitor, and terminate remote sessions |

