# Tools & Interfaces Reference (`kaggle-app-hosting`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `kaggle-app-hosting`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_app_hosting.py` | Scaffold persistent CPU web app kernel with SQLite sync | `python3 scripts/scaffold_app_hosting.py <dir>` | `0`: Success, `1`: Failure |
| `validate_app_hosting.py` | Verify CPU-only and tunnel configuration compliance | `python3 scripts/validate_app_hosting.py <dir>` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `kaggle datasets version` | Synchronize SQLite / state datasets to private Kaggle dataset | `kaggle datasets version -p <dir> -m 'sync'` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Run scaffolding, validation, and dataset sync | Skill execution protocol |
| `write_file` | Generate app runner notebook and sync scripts | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `Kaggle Datasets API` | External Integration | Private dataset versioning for state persistence |
| `Cloudflare Tunnel (cloudflared)` | External Integration | Persistent ingress for hosted web applications |

