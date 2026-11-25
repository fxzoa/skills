# Proposal, HLD & Incident Report HTML Trigger & Smoke Test Guide

## Positive Trigger Examples
1. *"Write a formal Incident Report in standalone HTML for yesterday's Redis outage, including root cause, timeline, and remediation actions."*
2. *"Create a print-ready High-Level Design (HLD) document in paper-and-ink HTML with dual Rule.14 diagrams."*
3. *"Draft an executive architecture Proposal comparing two database migration options in clean standalone HTML."*

## Negative Trigger Examples
1. *"Write a developer-facing technical blog post with a hero banner and TL;DR card."* -> Use `tech-blog-html` instead.
2. *"Create a 11-chapter `README.html` specification with setup commands and `.env` tables."* -> Use `html-readme-architect` instead.
3. *"Generate only a standalone process flowchart or ER diagram."* -> Use `diagram-design` instead.

## Smoke Test
Verify the deterministic scripts and skill structure:
```bash
python3 -B scripts/validate_html.py --help
python3 -B scripts/validate_html.py prototype/sample.html
python3 -B ../create-new-skill/scripts/validate_skill.py .
```
Expected result: All commands exit with code `0` and `[OK]` status.
