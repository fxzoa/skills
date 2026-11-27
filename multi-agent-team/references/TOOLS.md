# Tools & Interfaces Reference (`multi-agent-team`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `multi-agent-team`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `configure_team.py` | Deterministic scaffolding tool | `python3 scripts/configure_team.py --help` | `0`: OK, `1`: Error |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `setup.sh` | Scaffold team roster configuration | `bash scripts/setup.sh` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `invoke_subagent` | Delegate tasks across role-based models (pro, flash, flash_lite) | Skill execution protocol |
| `send_message` | Inter-agent peer communication and status updates | Skill execution protocol |
| `manage_subagents` | Lifecycle monitoring and termination of subagents | Skill execution protocol |
| `swarm` | Multi-worker task boards and shared workspaces | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `Gemini Multi-Model Endpoints` | External Integration | Gemini 3.8 Flash (Coordinator), Gemini 4 Carbon (Advisor/Reviewer), Gemini 4 Hydrogen (Worker) |

