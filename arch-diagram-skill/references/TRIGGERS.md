# Architecture Diagram Trigger & Smoke Test Guide

## Positive Trigger Examples
1. *"Create an architecture diagram for our multi-region Kubernetes inference cluster showing both the logical data flow and the TLS/port network topology in standalone HTML."*
2. *"Draw a cloud security and VPC architecture diagram as a self-contained HTML/SVG file without Mermaid."*
3. *"Visualize our API gateway, V8 Isolate proxy, and backend AI services using dual Rule.14 logical and physical diagrams."*

## Negative Trigger Examples
1. *"Create a sequence diagram or ER schema for our order checkout database."* -> Use `diagram-design` instead.
2. *"Write a formal High-Level Design (HLD) proposal document or incident report in HTML."* -> Use `prop-hld-ir-html` instead.
3. *"Generate a full 11-chapter project README.html with setup commands and .env tables."* -> Use `html-readme-architect` instead.

## Smoke Test
Verify the deterministic scripts and skill structure:
```bash
python3 -B scripts/validate_html.py --help
python3 -B scripts/validate_html.py prototype/sample.html
python3 -B ../create-new-skill/scripts/validate_skill.py .
```
Expected result: All commands exit with code `0` and `[OK]` status.
