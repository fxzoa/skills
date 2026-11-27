# Diagram Design Trigger & Smoke Test Guide

## Positive Trigger Examples
1. *"Create a branded sequence diagram and state flowchart for our OAuth2 token refresh pipeline as standalone HTML/SVG."*
2. *"Design an ER diagram and decision matrix for our billing microservice in a light-mode HTML file."*
3. *"Convert this `.drawio` / Mermaid process flowchart into a clean, self-contained inline SVG diagram."*

## Negative Trigger Examples
1. *"Create a dual logical and physical/network system architecture diagram with ports and TLS boundaries."* -> Use `architecture-diagram` instead.
2. *"Write a 9-block technical blog post announcing our new caching engine."* -> Use `tech-blog-html` instead.
3. *"Build a PowerPoint presentation deck (.pptx) for our quarterly roadmap."* -> Use `pptx-generator` instead.

## Smoke Test
Verify the deterministic scripts and skill structure:
```bash
python3 -B scripts/validate_html.py --help
python3 -B scripts/validate_html.py prototype/sample.html
python3 -B ../create-new-skill/scripts/validate_skill.py .
```
Expected result: All commands exit with code `0` and `[OK]` status.
