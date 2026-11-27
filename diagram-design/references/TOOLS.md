# Tools & Interfaces Reference (`diagram-design`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `diagram-design`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_html.py` | Deterministic scaffolding tool | `python3 scripts/scaffold_html.py --help` | `0`: OK, `1`: Error |
| `validate_html.py` | Technical diagram SVG and HTML validator | `python3 scripts/validate_html.py <html_file>` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `python3 -m http.server` | Local preview of rendered technical diagrams | `python3 -m http.server 8080` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Execute validate_html.py against output HTML diagrams | Skill execution protocol |
| `write_file / edit_file` | Materialize branded SVG and HTML technical diagrams | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `N/A (Self-Contained)` | External Integration | All visual diagrams must be standalone inline SVG without external CDNs. |

