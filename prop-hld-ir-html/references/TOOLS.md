# Tools & Interfaces Reference (`prop-hld-ir-html`)

This document defines tool interfaces, CLI options, execution protocols, and classifications for `prop-hld-ir-html`.
All tools are structured into four primary execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `scaffold_html.py` | Deterministic scaffolding tool | `python3 scripts/scaffold_html.py --help` | `0`: OK, `1`: Error |
| `validate_html.py` | Archetype A print-ready document validator | `python3 scripts/validate_html.py <html_file>` | `0`: Success, `1`: Failure |

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose in Skill | Example Invocation |
|:---|:---|:---|
| `google-chrome --headless --print-to-pdf` | Generate print-ready PDF from HTML | `google-chrome --headless --print-to-pdf=doc.pdf doc.html` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Verify HTML and generate PDF snapshots | Skill execution protocol |
| `write_file / edit_file` | Author ink-and-paper monochrome proposals and HLDs | Skill execution protocol |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol / Type | Purpose & Scope |
|:---|:---|:---|
| `N/A (Self-Contained)` | External Integration | Offline-first, zero CDN, inline SVG only. |

