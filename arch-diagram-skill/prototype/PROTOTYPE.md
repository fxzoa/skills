# Architecture Diagram Prototype Specification

This directory contains `sample.html`, a minimal reference prototype illustrating standalone light-mode HTML/SVG architecture diagrams compliant with Rule.11 (zero external CDNs, zero Mermaid) and Rule.14 (dual logical + physical/network diagrams).

## Reusable Core Design vs. Project-Specific Replacements

| Layer | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Deliverable) |
|:---|:---|:---|
| **HTML Shell** | `<!DOCTYPE html>`, UTF-8 meta, responsive viewport, single-file `<style>` block (`templates/base.html.tmpl`) | `<title>`, document header, system name, author/version metadata |
| **Theme & Typography** | Light slate canvas (`#f8fafc`), white cards (`#ffffff`), `#0f172a` ink, `#e2e8f0` borders, sans-serif + monospace stack | Accent palette per architectural tier (e.g., client, gateway, AI backend, storage) |
| **Dual-Diagram Layout (Rule.14)** | Paired section structure: (1) High-Level Logical Diagram + (2) Infra/Network Physical Diagram | Specific services, runtimes (Docker, V8 Isolate), TLS boundaries, ports, auth token paths |
| **SVG Primitives** | Responsive `<svg viewBox="0 0 1000 ...">`, `<defs>` arrow markers, rounded layer containers, bold node titles | Node coordinates, connector paths, protocol labels (`HTTPS/443`, `gRPC`), legend items |
| **Validation & Scaffolding** | `scripts/scaffold_html.py` and `scripts/validate_html.py` | Output HTML filename and target project path |
