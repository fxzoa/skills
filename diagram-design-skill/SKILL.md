---
name: diagram-design
description: Create branded technical, process, architecture, flow, ER, sequence, timeline, and data diagrams as standalone HTML/SVG/PNG.
license: MIT
metadata:
  version: "2.6"
---

# Diagram Design Standards

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control
Procedural steps (shell synthesis, parameter guessing, manual polling) must NOT rely on probabilistic prompt-driven execution.
All procedural workflows must be materialized into single-command, deterministic Python scripts in `scripts/`.


Generate crisp, branded, standalone HTML/SVG diagrams across architecture, process, data, and lifecycle domains.

## Pre-Built Operations (`scripts/`)
Detailed tool interfaces are specified in [references/TOOLS.md](references/TOOLS.md).


| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_html` | `python3 scripts/scaffold_html.py ...` | Deterministic code-driven generator |
| `validate_html` | `python3 scripts/validate_html.py <file.html>` | Verifies standalone HTML (zero external CDNs, zero Mermaid). |

## Core Diagram Standards
- **Diagram Selection**: Match diagram type to intent (Flowchart/Sequence for execution, ER/Schema for data, Quadrant/Matrix for decisions, Gantt/Timeline for schedules, Architecture/Deployment for systems).
- **Visual Clarity**: Light-mode canvas (`#ffffff` / `#f8fafc`), consistent color palette per layer, generous padding, zero overlapping labels, and explicit legends.
- **Inline SVG**: Use responsive `<svg viewBox="...">` with `<defs>` markers, rounded containers (`rx="8"`–`12"`), and clear directional paths.
- **Imports**: When converting `.drawio`, Mermaid, or `.excalidraw` inputs, normalize into clean, self-contained inline SVG.

## Trigger & Exit Criteria
- **Trigger**: Requests for technical, process, ER, sequence, data, or lifecycle diagrams.
- **Exit Criteria**: Standalone HTML/SVG deliverable created and `validate_html(<file.html>)` exits `0`.

## Anti-Patterns
- **Never rely on probabilistic prompt-driven orchestration**: Materialize procedural steps into deterministic `scripts/*.py`.
- Never embed Mermaid.js or external CDN scripts in final HTML output (Rule.11).
- Never overcrowd a single SVG; split complex views into focused diagrams.
