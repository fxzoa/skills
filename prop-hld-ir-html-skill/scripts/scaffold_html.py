#!/usr/bin/env python3
"""Scaffold an Archetype A Proposal / HLD / Incident Report HTML."""
import argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Proposal/HLD HTML.")
    parser.add_argument("--title", required=True, help="Document Title")
    parser.add_argument("--type", choices=["proposal", "hld", "incident"], default="proposal", help="Doc Type")
    parser.add_argument("--output", required=True, help="Output HTML path")
    args = parser.parse_args()

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{args.title}</title>
  <style>
    @page {{ size: A4; margin: 20mm; }}
    body {{
      font-family: "Hiragino Mincho ProN", "Yu Mincho", serif;
      color: #111;
      background: #fff;
      line-height: 1.7;
      margin: 0; padding: 2rem;
    }}
    .sheet {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ font-size: 1.6rem; border-bottom: 2px solid #111; padding-bottom: 0.3rem; margin-bottom: 0.5rem; }}
    .meta {{ font-size: 0.85rem; color: #555; text-align: right; margin-bottom: 2rem; }}
    h2 {{ font-size: 1.2rem; border-left: 4px solid #111; padding-left: 0.5rem; margin-top: 2rem; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9rem; }}
    th, td {{ border: 1px solid #333; padding: 0.5rem; text-align: left; }}
    th {{ background: #f0f0f0; }}
  </style>
</head>
<body>
  <div class="sheet">
    <h1>{args.title}</h1>
    <div class="meta">種別: {args.type.upper()} | 作成日: 2026-11-25 | 状態: 審議中</div>

    <h2>1. 目的および背景</h2>
    <p>本文書は {args.title} における要件および技術的決定事項を記述する。</p>

    <h2>2. 方針比較および最適案</h2>
    <table>
      <thead>
        <tr><th>案</th><th>方針概要</th><th>メリット</th><th>リスク・判定</th></tr>
      </thead>
      <tbody>
        <tr><td>案A (推奨)</td><td>決定論的ツール制御</td><td>高い再現性・堅牢性</td><td>採用</td></tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[OK] Scaffolded Archetype A Doc: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
