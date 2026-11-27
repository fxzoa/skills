# HTML README & Specification Prototype

This directory contains `sample.html`, a minimal reference prototype for standalone light-mode `README.html` technical specifications compliant with Rule.11, Rule.12 (Archetype C), and Rule.14.

## Reusable Core Design vs. Project-Specific Replacements

| Layer | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Deliverable) |
|:---|:---|:---|
| **HTML Shell** | `<!DOCTYPE html>`, UTF-8 meta, single-file `<style>`, sticky/clean navigation (`templates/base.html.tmpl`) | Project name, `<title>`, version badges, repository links |
| **11-Chapter Skeleton** | Fixed chapter structure (Overview, Dual Architecture, Flow, Components, APIs, Integrations, `.env`, Prerequisites, Setup, Constraints, Related Services) | Project-specific prose, module cards, endpoint tables, and `.env` variable definitions |
| **Design System** | Light slate background (`#f8fafc`), white cards (`#ffffff`), `#e2e8f0` borders, `#0f172a` text | Brand accent color, service-specific status badges, notice callouts |
| **Inline SVG Diagrams** | Rule.14 dual SVG containers (Logical + Physical/Network) and data-flow SVG with `<defs>` markers | System components, ports, TLS boundaries, storage nodes, and request flows |
| **Validation & Scaffolding** | `scripts/scaffold_html.py` and `scripts/validate_html.py` | Output `README.html` path and project-specific healthcheck commands |
