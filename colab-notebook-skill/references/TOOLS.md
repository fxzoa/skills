# Tools & Interfaces Reference (`colab-notebook`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `colab-notebook`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_colab_project.py` | Scaffold studio inference notebook project | `python3 scripts/scaffold_colab_project.py <dir>` | `0`: Success, `1`: Failure |
| `validate_colab_bundle.py` | Validate single-responsibility cells and external .env | `python3 scripts/validate_colab_bundle.py <dir>` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `install_llama_cpp.sh` | Provision uv venv and llama-cpp-python in Colab | `bash scripts/install_llama_cpp.sh` |
| `colab run` | Execute notebook via colab CLI | `colab run notebook.ipynb` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Run project scaffolding and bundle validation | Skill execution protocol |
| `write_file` | Generate declarative .ipynb, companion README.html, and external .env | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `Google Colab Runtime API` | External Integration | Provision and manage GPU/TPU instances on Colab Studio |
| `Cloudflare Tunnel` | External Integration | Expose FastAPI inference server to public endpoint |

