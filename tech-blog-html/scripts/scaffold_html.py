#!/usr/bin/env python3
"""Scaffold a Rule.11/Rule.12 Archetype B 9-block Technical Blog HTML."""
import argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Tech Blog HTML.")
    parser.add_argument("--title", required=True, help="Article Title")
    parser.add_argument("--output", required=True, help="Output HTML path")
    args = parser.parse_args()

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{args.title}</title>
  <style>
    :root {{ --primary: #0284c7; --bg: #f8fafc; --text: #1e293b; }}
    body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 2rem; }}
    .article {{ max-width: 860px; margin: 0 auto; background: #fff; padding: 2.5rem; border-radius: 8px; border: 1px solid #e2e8f0; }}
    .hero {{ border-bottom: 2px solid var(--primary); padding-bottom: 1rem; margin-bottom: 2rem; }}
    .tldr-card {{ background: #f0f9ff; border-left: 4px solid var(--primary); padding: 1rem; margin-bottom: 2rem; }}
    svg {{ max-width: 100%; height: auto; margin: 2rem 0; }}
  </style>
</head>
<body>
  <article class="article">
    <div class="hero">
      <h1>{args.title}</h1>
      <p>9-Block Technical Feature Article</p>
    </div>
    <div class="tldr-card">
      <strong>TL;DR:</strong> 記事の要約とキーポイントをここに記載します。
    </div>
    <h2>厳選アーキテクチャ図解</h2>
    <svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
      <rect width="800" height="200" fill="#f8fafc" rx="8" />
      <text x="400" y="105" text-anchor="middle" font-size="16" fill="#0284c7" font-weight="bold">Technical Flow Overview</text>
    </svg>
  </article>
</body>
</html>
"""
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[OK] Scaffolded Tech Blog: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
