# Tech Blog HTML Trigger & Smoke Test Guide

## Positive Trigger Examples
1. *"Write a technical blog post in standalone HTML introducing our new zero-copy inference pipeline using the 9-block structure."*
2. *"Create an engineering release announcement HTML page with a TL;DR card, comparison table, benchmarks, and one curated inline SVG."*
3. *"Turn these benchmark notes into a reader-friendly HTML tech article for engineers evaluating adoption."*

## Negative Trigger Examples
1. *"Create a formal High-Level Design (HLD) or Incident Report with no emojis or gradients."* -> Use `prop-hld-ir-html` instead.
2. *"Build a comprehensive 11-chapter `README.html` specification with `.env` and prerequisite tables."* -> Use `html-readme-architect` instead.
3. *"Create a standalone system architecture diagram or ER schema."* -> Use `architecture-diagram` or `diagram-design` instead.

## Smoke Test
Verify the deterministic scripts and skill structure:
```bash
python3 -B scripts/validate_html.py --help
python3 -B scripts/validate_html.py prototype/sample.html
python3 -B ../create-new-skill/scripts/validate_skill.py .
```
Expected result: All commands exit with code `0` and `[OK]` status.
