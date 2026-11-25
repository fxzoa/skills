---
name: architecture-diagram
description: Create professional, light-themed architecture diagrams as standalone HTML files with inline SVG graphics.
license: MIT
metadata:
  version: "1.1"
  author: Cocoon AI (hello@cocoon-ai.com)
---

# Architecture Diagram Standards

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Create standalone, light-mode HTML/SVG architecture diagrams (Rule.11 / Rule.14 compliant).

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_html` | `python3 scripts/scaffold_html.py ...` | Deterministic code-driven generator |
| `validate_html` | `python3 scripts/validate_html.py <file.html>` | Verifies standalone HTML (zero external CDNs, zero Mermaid). |

## Design & Layout Rules
- **Theme & Typography**: Light background (`#f8fafc` / `#ffffff`), high-contrast slate text (`#0f172a`), subtle borders (`#e2e8f0`), and clean sans-serif + monospace fonts.
- **Dual Diagrams (Rule.14)**: When documenting system architecture, pair **(1) High-Level Logical Diagram** (users, gateways, AI backends, flows) and **(2) Infra/Network Physical Diagram** (runtimes, TLS, ports, network boundaries, auth paths, storage).
- **SVG Standards**: Use inline `<svg viewBox="0 0 1000 ...">` with `<defs>` arrow markers, distinct color-coded layer containers, bold node titles, and clear directional connectors.
- **Self-Contained**: Zero external CDNs, zero Mermaid.js, zero external scripts.

## Trigger & Exit Criteria
- **Trigger**: Requests for system, infrastructure, cloud, security, or network topology diagrams.
- **Exit Criteria**: Standalone HTML/SVG generated from `templates/base.html.tmpl` and `validate_html(<file.html>)` exits `0`.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never embed Mermaid.js or external CDN links in HTML deliverables (Rule.11).
- Never omit the physical/network diagram when producing system architecture docs (Rule.14).
