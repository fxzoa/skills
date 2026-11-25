---
name: prop-hld-ir-html
description: Creates formal Proposals, High-Level Designs (HLD), and Incident Reports as clean, print-ready standalone HTML documents using a paper-and-ink aesthetic (Rule.11 / Rule.12 Archetype A). Use when producing decision-oriented IT documents with executive summaries, risk highlights, and monochrome-plus-vermilion inline SVGs. Do not use for tech blog posts (use tech-blog-html), 11-chapter README.html specs (use html-readme-architect), or standalone flowcharts (use diagram-design).
---

# Proposal, HLD & Incident Report HTML Architect

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Produce formal, decision-oriented IT documents in standalone HTML using a "paper & ink" aesthetic (Rule.11 / Rule.12 Archetype A).

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_html` | `python3 scripts/scaffold_html.py ...` | Deterministic code-driven generator |
| `validate_html` | `python3 scripts/validate_html.py <file.html>` | Verifies standalone HTML (zero external CDNs, zero Mermaid). |

## Design & Content Standards
- **Audience**: Decision-makers who need fast, unambiguous conclusions. Lead with an Executive Summary / Root Cause & Action table.
- **Aesthetic (Paper & Ink)**: White/warm-paper background (`#ffffff` / `#fafaf9`), deep ink text (`#1c1917`), monochrome borders, and **vermilion (`#dc2626`)** accents only for critical risks/highlights.
- **No Decorative Noise**: Strictly forbid gradients, emojis, and flashy icon cards.
- **Visuals & Print**: Use clean responsive tables, `@media print` CSS (`break-inside: avoid`), and monochrome + vermilion inline SVGs with explicit legends (including Rule.14 dual diagrams for HLDs).

## Trigger & Exit Criteria
- **Trigger**: Requests for Proposals, HLDs, Architecture Designs, or Incident/Investigation Reports.
- **Exit Criteria**: Standalone HTML generated and `validate_html(<file.html>)` exits `0`.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never use emojis, CSS gradients, Mermaid.js, or external CDN scripts (Rule.11 / Rule.12).
- Never bury conclusions at the bottom; place decisions and action items upfront.

## Document Index
- [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) — Reusable paper-and-ink HTML/print CSS core design vs. project-specific replacements.
- [references/TRIGGERS.md](references/TRIGGERS.md) — Positive/negative trigger examples and smoke test steps.
- [references/TOOLS.md](references/TOOLS.md) — Deterministic script interfaces (`scaffold_html.py`, `validate_html.py`).
