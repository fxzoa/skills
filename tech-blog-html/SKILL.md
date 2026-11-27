---
name: tech-blog-html
description: Creates engaging technical blog posts and feature announcements as standalone light-mode HTML using the 9-block structure with one curated inline SVG (Rule.11 / Rule.12 Archetype B). Use when writing developer-facing articles, release notes, or benchmark evaluations. Do not use for formal HLDs/proposals/incident reports (use prop-hld-ir-html), 11-chapter README.html specs (use html-readme-architect), or standalone diagrams (use architecture-diagram or diagram-design).
---

# Tech Blog HTML Architect

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Write clear, reader-friendly technical blog posts in standalone HTML for engineers evaluating whether a new technology/feature applies to them.

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_html` | `python3 scripts/scaffold_html.py ...` | Deterministic code-driven generator |
| `validate_html` | `python3 scripts/validate_html.py <file.html>` | Verifies standalone HTML (zero external CDNs, zero Mermaid). |

## 9-Block Structure & Visual Rules
1. **Hero Eyecatch** (controlled gradient allowed) + Title.
2. **TL;DR Card** (3-bullet summary upfront).
3. **Problem / Background** (why this matters).
4. **Core Concept + 1 Curated Inline SVG Diagram** (keep to **one** intuitive diagram for the entire article).
5. **Comparison Table** (before vs. after / alternatives).
6. **Hands-On Example** (minimal copy-pasteable code).
7. **Benchmarks / Real Results**.
8. **Caveats / When Not to Use**.
9. **Conclusion & Next Steps**.
- Headings may use restrained emojis; keep body clean, light-mode, and zero-CDN.
- **Layout Width**: Set the main container width to `90%` of the full viewport width (e.g., `width: 90%; max-width: 90vw; margin: 0 auto;`).

## Trigger & Exit Criteria
- **Trigger**: Writing technical blogs, release announcements, or feature introductions in HTML.
- **Exit Criteria**: 9-block standalone HTML with 1 curated inline SVG created, and `validate_html(<file.html>)` exits `0`.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never embed Mermaid.js or external CDN scripts (Rule.11).
- Never overload the post with multiple complex diagrams (limit to 1 curated SVG).

## Document Index
- [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) — Reusable 9-block HTML/CSS core design vs. project-specific replacements.
- [references/TRIGGERS.md](references/TRIGGERS.md) — Positive/negative trigger examples and smoke test steps.
- [references/TOOLS.md](references/TOOLS.md) — Deterministic script interfaces (`scaffold_html.py`, `validate_html.py`).
