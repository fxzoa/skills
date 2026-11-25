---
name: html-readme-architect
description: Create standalone light-mode HTML technical specifications and README.html without Mermaid or external CDNs (Rule.11 / Rule.12 Archetype C).
---

# HTML README & Specification Architect

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Build modern, light-mode, self-contained `README.html` technical specifications (Rule.11 / Rule.12 Archetype C / Rule.14).

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_html` | `python3 scripts/scaffold_html.py ...` | Deterministic code-driven generator |
| `validate_html` | `python3 scripts/validate_html.py <file.html>` | Verifies standalone HTML (zero external CDNs, zero Mermaid). |

## Standard Structure (11 Chapters)
1. **Overview & Objectives** — Purpose, scope, badges, summary cards.
2. **Architecture Diagrams (Rule.14)** — Inline SVG pair: (1) High-Level Logical + (2) Infra/Network Physical (ports, TLS, boundaries).
3. **Data Processing Flow** — Inline SVG flow + step cards.
4. **Core Components** — CSS Grid module/class cards.
5. **Public APIs / Event Specs** — Endpoint/method specification table.
6. **External Integrations** — External services and protocols.
7. **Configuration & Secrets** — Complete `.env` variable table (secrets redacted).
8. **Prerequisites** — OS, GPU/VRAM, RAM, runtime, permissions.
9. **Setup & Run Verification** — Copy-pasteable install, run, and healthcheck commands.
10. **Constraints & Recovery** — Notice boxes for operational limits and recovery steps.
11. **Related Services** — Cross-links to companion services/files.

## Design System
- Light slate background (`#f8fafc`), white cards (`#ffffff`), crisp borders (`#e2e8f0`), high-contrast slate text (`#0f172a`), and inline `<svg>` with `<defs>` markers.

## Trigger & Exit Criteria
- **Trigger**: Creating or updating `README.html` or technical HTML specifications.
- **Exit Criteria**: All 11 chapters and dual Rule.14 inline SVGs included, and `validate_html(<file.html>)` exits `0`.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never use Mermaid.js, external CDNs, or omit `.env` variables from Chapter 07.
