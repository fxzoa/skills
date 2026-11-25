# Diagram Design Prototype Specification

This directory contains `sample.html`, a minimal reference prototype illustrating branded, self-contained HTML/SVG diagrams across process, data, and lifecycle domains without external CDNs or Mermaid.js (Rule.11).

## Reusable Core Design vs. Project-Specific Replacements

| Layer | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Deliverable) |
|:---|:---|:---|
| **HTML Shell** | `<!DOCTYPE html>`, UTF-8 meta, responsive viewport, embedded `<style>` (`templates/base.html.tmpl`) | `<title>`, diagram title, subtitle, and contextual caption |
| **Visual System** | Light-mode canvas (`#ffffff` / `#f8fafc`), generous padding, consistent layer colors, explicit legend box | Color assignments mapped to project-specific domains or actor roles |
| **Diagram Archetype** | Inline `<svg viewBox="...">` with `<defs>` markers and rounded containers (`rx="8"`–`12"`) | Diagram type (Flowchart, Sequence, ER/Schema, Quadrant/Matrix, Timeline/Gantt) |
| **Content & Labels** | Non-overlapping label placement rules and directional path styling | Entities, steps, state transitions, cardinality, or timeline milestones |
| **Validation & Scaffolding** | `scripts/scaffold_html.py` and `scripts/validate_html.py` | Target output HTML path and converted `.drawio` / `.excalidraw` source data |
