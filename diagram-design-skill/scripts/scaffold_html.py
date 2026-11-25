#!/usr/bin/env python3
"""Scaffold a standalone technical diagram HTML with inline SVG."""
import argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Technical Diagram HTML.")
    parser.add_argument("--title", required=True, help="Diagram Title")
    parser.add_argument("--output", required=True, help="Output HTML path")
    args = parser.parse_args()

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{args.title}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f8fafc;
      margin: 0;
      padding: 2rem;
      display: flex;
      justify-content: center;
    }}
    .diagram-container {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 2rem;
      max-width: 1000px;
      width: 100%;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    h1 {{ margin: 0 0 1.5rem 0; font-size: 1.5rem; color: #0f172a; text-align: center; }}
    svg {{ width: 100%; height: auto; }}
  </style>
</head>
<body>
  <div class="diagram-container">
    <h1>{args.title}</h1>
    <svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
      <rect width="800" height="300" fill="#f8fafc" rx="8" />
      <rect x="50" y="80" width="180" height="140" fill="#ffffff" stroke="#94a3b8" stroke-width="2" rx="6" />
      <text x="140" y="130" font-size="14" font-weight="bold" text-anchor="middle">Step 1: Input</text>
      
      <path d="M 230 150 L 310 150" stroke="#3b82f6" stroke-width="2" />
      
      <rect x="310" y="80" width="180" height="140" fill="#eff6ff" stroke="#3b82f6" stroke-width="2" rx="6" />
      <text x="400" y="130" font-size="14" font-weight="bold" text-anchor="middle" fill="#1e40af">Step 2: Process</text>
      
      <path d="M 490 150 L 570 150" stroke="#3b82f6" stroke-width="2" />
      
      <rect x="570" y="80" width="180" height="140" fill="#ffffff" stroke="#94a3b8" stroke-width="2" rx="6" />
      <text x="660" y="130" font-size="14" font-weight="bold" text-anchor="middle">Step 3: Output</text>
    </svg>
  </div>
</body>
</html>
"""
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[OK] Scaffolded Diagram: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
