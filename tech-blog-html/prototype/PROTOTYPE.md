# Tech Blog HTML Prototype Specification

This directory contains `sample.html`, a minimal reference prototype for engaging, standalone light-mode technical blog posts structured around the 9-block layout (Rule.11 / Rule.12 Archetype B).

## Reusable Core Design vs. Project-Specific Replacements

| Layer | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Deliverable) |
|:---|:---|:---|
| **HTML Shell** | `<!DOCTYPE html>`, UTF-8 meta, single-file `<style>`, light-mode reading column (`templates/base.html.tmpl`) | Article `<title>`, publication date, author, reading-time metadata |
| **9-Block Structure** | Hero Eyecatch, TL;DR Card, Problem, Core Concept + 1 SVG, Comparison Table, Hands-On Example, Benchmarks, Caveats, Conclusion | Topic narrative, 3-bullet TL;DR, before/after comparison rows, code snippets, benchmark numbers |
| **Visual Styling** | Controlled hero gradient, clean card borders, restrained heading emojis, syntax-ready `<pre><code>` styling | Hero color theme, topic-specific badges, callout notes |
| **Curated Single SVG** | Centered responsive inline `<svg viewBox="...">` container with `<defs>` markers (strictly 1 diagram per post) | Conceptual illustration explaining the core mechanism or architecture shift |
| **Validation & Scaffolding** | `scripts/scaffold_html.py` and `scripts/validate_html.py` | Output blog HTML path and article slug |
