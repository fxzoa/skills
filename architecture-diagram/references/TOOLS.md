# Tools & Interfaces Reference (`architecture-diagram`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `architecture-diagram`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_html.py` | Deterministic scaffolding tool | `python3 scripts/scaffold_html.py --help` | `0`: OK, `1`: Error |
| `validate_html.py` | Light-mode HTML & inline SVG validator | `python3 scripts/validate_html.py <html_file>` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `python3 -m http.server` | Local preview server for HTML diagrams | `python3 -m http.server 8080` |
| `google-chrome --headless` | Headless verification & rendering test | `google-chrome --headless --screenshot output.html` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Run validate_html.py to verify HTML/SVG compliance | Skill execution protocol |
| `read_file` | Inspect architecture specs and input data | Skill execution protocol |
| `write_file / edit_file` | Generate standalone light-mode HTML diagram files | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `N/A (Self-Contained)` | External Integration | Rule.11 strictly prohibits external CDNs, Mermaid, and remote runtime scripts. |

