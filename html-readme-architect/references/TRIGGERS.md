# HTML README Architect Trigger & Smoke Test Guide

## Positive Trigger Examples
1. *"Create a standalone `README.html` technical specification for this repository covering architecture, APIs, `.env` configuration, and setup verification."*
2. *"Update our service's `README.html` to include all 11 standard chapters and Rule.14 dual inline SVG diagrams."*
3. *"Generate a light-mode HTML API and operations reference manual with zero external CDNs."*

## Negative Trigger Examples
1. *"Write an engaging 9-block technical blog post introducing our new feature."* -> Use `tech-blog-html` instead.
2. *"Create a formal Incident Report or Executive Proposal in paper-and-ink HTML."* -> Use `prop-hld-ir-html` instead.
3. *"Draw only a standalone system topology SVG diagram without API or `.env` documentation."* -> Use `architecture-diagram` instead.

## Smoke Test
Verify the deterministic scripts and skill structure:
```bash
python3 -B scripts/validate_html.py --help
python3 -B scripts/validate_html.py prototype/sample.html
python3 -B ../create-new-skill/scripts/validate_skill.py .
```
Expected result: All commands exit with code `0` and `[OK]` status.
