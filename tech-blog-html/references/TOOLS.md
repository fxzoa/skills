# Tools & Interfaces Reference (`tech-blog-html`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `tech-blog-html`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_html.py` | Deterministic scaffolding tool | `python3 scripts/scaffold_html.py --help` | `0`: OK, `1`: Error |
| `validate_html.py` | Archetype B 9-block technical blog validator | `python3 scripts/validate_html.py <html_file>` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `python3 -m http.server` | Local preview of technical article | `python3 -m http.server 8080` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Execute validation on technical blog articles | Skill execution protocol |
| `write_file / edit_file` | Generate hero-decorated standalone HTML tech blog | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `N/A (Self-Contained)` | External Integration | CDN-free standalone HTML with exactly one featured inline SVG diagram. |

