# Proposal, HLD & Incident Report HTML Prototype

This directory contains `sample.html`, a minimal reference prototype for formal, decision-oriented IT documents in standalone HTML using the "paper & ink" aesthetic (Rule.11 / Rule.12 Archetype A).

## Reusable Core Design vs. Project-Specific Replacements

| Layer | Reusable Core Design (Keep Across Projects) | Project-Specific Replacements (Customize Per Deliverable) |
|:---|:---|:---|
| **HTML Shell & Print CSS** | `<!DOCTYPE html>`, UTF-8 meta, `@media print` rules (`break-inside: avoid`), clean typography (`templates/base.html.tmpl`) | Document `<title>`, document ID/date, author, classification/audience |
| **Paper & Ink Palette** | White/warm-paper background (`#ffffff` / `#fafaf9`), deep ink (`#1c1917`), monochrome borders, vermilion (`#dc2626`) risk accent | Risk/severity badges, decision status labels, critical path highlights |
| **Document Layout** | Upfront Executive Summary / Root Cause & Action table, responsive comparison tables, zero emojis/gradients | Proposal options, HLD requirements, or Incident timeline, root cause, and remediation items |
| **Inline SVG Diagrams** | Monochrome + vermilion inline SVGs with explicit legends (including Rule.14 dual diagrams for HLDs) | Target architecture components, failure points, blast radius, and network boundaries |
| **Validation & Scaffolding** | `scripts/scaffold_html.py` and `scripts/validate_html.py` | Deliverable HTML filename and document type (Proposal / HLD / Incident Report) |
