#!/usr/bin/env python3
"""Scaffold a Rule.11/Rule.12 Archetype C README.html technical specification."""
import argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold README.html.")
    parser.add_argument("--title", required=True, help="Project Name / Title")
    parser.add_argument("--output", default="README.html", help="Output path (default: README.html)")
    args = parser.parse_args()

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{args.title} - Technical Specification</title>
  <style>
    :root {{
      --bg: #ffffff;
      --surface: #f8fafc;
      --border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
      --primary: #2563eb;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0; padding: 2rem; color: var(--text); background: var(--bg); line-height: 1.6;
    }}
    .doc-container {{ max-width: 1000px; margin: 0 auto; }}
    h1 {{ border-bottom: 2px solid var(--primary); padding-bottom: 0.5rem; }}
    h2 {{ border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; margin-top: 2rem; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
    th, td {{ border: 1px solid var(--border); padding: 0.75rem; text-align: left; }}
    th {{ background: var(--surface); }}
    pre {{ background: var(--surface); padding: 1rem; border-radius: 6px; border: 1px solid var(--border); overflow-x: auto; }}
    svg {{ max-width: 100%; height: auto; }}
  </style>
</head>
<body>
  <div class="doc-container">
    <h1>{args.title}</h1>
    <p>Technical Specification & System Documentation (Rule.11 / Archetype C Standard)</p>

    <h2>1. Overview & Architecture</h2>
    <svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
      <rect width="800" height="200" fill="#f8fafc" rx="8" />
      <rect x="50" y="50" width="200" height="100" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="6" />
      <text x="150" y="105" text-anchor="middle" font-weight="bold">Core Service</text>
    </svg>

    <h2>2. Quick Start</h2>
    <pre><code># Installation & Launch Commands
git clone &lt;repo&gt;
cd &lt;project&gt;
docker compose up -d</code></pre>

    <h2>3. Configuration Parameters</h2>
    <table>
      <thead>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr><td>PORT</td><td>8080</td><td>Service bind port</td></tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[OK] Scaffolded README.html: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
