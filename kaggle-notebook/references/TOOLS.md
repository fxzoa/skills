# Tools & Interfaces Reference (`kaggle-notebook`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `kaggle-notebook`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_kaggle_project.py` | Scaffold T4x2 inference kernel with external .env | `python3 scripts/scaffold_kaggle_project.py <dir>` | `0`: Success, `1`: Failure |
| `validate_kaggle_bundle.py` | Verify quiet execution and .env validation logic | `python3 scripts/validate_kaggle_bundle.py <dir>` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `install_llama_cpp.sh` | Install GPU-accelerated wheels in Kaggle runner | `bash scripts/install_llama_cpp.sh` |
| `kaggle kernels push` | Push kernel bundle to Kaggle GPU | `kaggle kernels push -p <dir>` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Execute bundle validation and Kaggle CLI commands | Skill execution protocol |
| `write_file` | Author kernel metadata, notebook JSON, and companion configs | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `Kaggle Kernels API` | External Integration | Push code, start GPU sessions, and query build status |
| `Cloudflare Tunnel` | External Integration | Expose web UI / inference endpoints |

