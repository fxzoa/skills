#!/usr/bin/env python3
"""Scaffold a light-themed Architecture Diagram HTML with dual logical & physical views."""
import argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Architecture Diagram HTML.")
    parser.add_argument("--title", required=True, help="Diagram Title")
    parser.add_argument("--output", required=True, help="Output HTML path")
    args = parser.parse_args()

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{args.title}</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
      --primary: #2563eb;
      --primary-light: #eff6ff;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 2rem;
      line-height: 1.5;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 2rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 1rem;
    }}
    h1 {{ margin: 0 0 0.5rem 0; font-size: 1.75rem; }}
    .subtitle {{ color: var(--text-muted); font-size: 0.95rem; }}
    .diagram-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 2rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .diagram-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
    }}
    .diagram-title {{ font-weight: 600; font-size: 1.1rem; color: var(--primary); }}
    svg {{ width: 100%; height: auto; display: block; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{args.title}</h1>
      <div class="subtitle">Rule.14 Dual Architecture Diagram (Logical & Physical Views)</div>
    </header>

    <!-- 1. Logical / Functional View -->
    <div class="diagram-card">
      <div class="diagram-header">
        <div class="diagram-title">1. 論理機能・データフロー構成 (Logical / Functional View)</div>
      </div>
      <svg viewBox="0 0 1000 350" xmlns="http://www.w3.org/2000/svg">
        <rect width="1000" height="350" fill="#f8fafc" rx="8" />
        <rect x="50" y="100" width="180" height="150" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="6" />
        <text x="140" y="140" font-size="14" font-weight="bold" text-anchor="middle" fill="#0f172a">Client / User</text>
        <text x="140" y="170" font-size="12" text-anchor="middle" fill="#64748b">Web SPA / API</text>
        
        <path d="M 230 175 L 370 175" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)" />
        
        <rect x="380" y="80" width="240" height="190" fill="#eff6ff" stroke="#93c5fd" stroke-width="2" rx="6" />
        <text x="500" y="120" font-size="14" font-weight="bold" text-anchor="middle" fill="#1e40af">API Gateway / Proxy</text>
        <text x="500" y="150" font-size="12" text-anchor="middle" fill="#3b82f6">Authentication & Routing</text>
        
        <path d="M 620 175 L 750 175" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)" />
        
        <rect x="760" y="100" width="190" height="150" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="6" />
        <text x="855" y="140" font-size="14" font-weight="bold" text-anchor="middle" fill="#0f172a">Backend Service</text>
        <text x="855" y="170" font-size="12" text-anchor="middle" fill="#64748b">Worker / Database</text>

        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb" />
          </marker>
        </defs>
      </svg>
    </div>

    <!-- 2. Physical / Network View -->
    <div class="diagram-card">
      <div class="diagram-header">
        <div class="diagram-title">2. 物理トポロジー・通信セキュリティ構成 (Physical / Network View)</div>
      </div>
      <svg viewBox="0 0 1000 350" xmlns="http://www.w3.org/2000/svg">
        <rect width="1000" height="350" fill="#f8fafc" rx="8" />
        <rect x="40" y="40" width="920" height="270" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="4" rx="8" />
        <text x="60" y="70" font-size="13" font-weight="bold" fill="#475569">VPC Network (10.10.0.0/16)</text>
        
        <rect x="80" y="100" width="240" height="170" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="6" />
        <text x="200" y="130" font-size="13" font-weight="bold" text-anchor="middle" fill="#0f172a">Public Subnet</text>
        <text x="200" y="160" font-size="11" text-anchor="middle" fill="#64748b">Port 443 (TLS 1.3)</text>
        <text x="200" y="185" font-size="11" text-anchor="middle" fill="#2563eb">Cloudflare Tunnel</text>
        
        <rect x="680" y="100" width="240" height="170" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="6" />
        <text x="800" y="130" font-size="13" font-weight="bold" text-anchor="middle" fill="#0f172a">Private Instance (GCE)</text>
        <text x="800" y="160" font-size="11" text-anchor="middle" fill="#64748b">Docker Runtime</text>
        <text x="800" y="185" font-size="11" text-anchor="middle" fill="#059669">Port 6379 (Internal)</text>
      </svg>
    </div>
  </div>
</body>
</html>
"""
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[OK] Scaffolded Architecture Diagram: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
