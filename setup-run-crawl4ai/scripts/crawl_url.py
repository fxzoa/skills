#!/usr/bin/env python3
"""crawl_url.py: 1-click deterministic scraping CLI tool utilizing local Crawl4AI Docker."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


def load_env_vars(env_file: Path) -> dict[str, str]:
    vars_map = {}
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                vars_map[k.strip()] = v.strip().strip("'\"")
    return vars_map


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape URL using local Crawl4AI container.")
    parser.add_argument("url", help="Target URL to crawl")
    parser.add_argument("--base-url", help="Crawl4AI Base URL")
    parser.add_argument("--token", help="Crawl4AI API Token")
    parser.add_argument("--env-file", default="/mnt/d/conf/.env", help="Path to .env file")
    parser.add_argument("--output", "-o", help="Save markdown/html to output file")
    parser.add_argument("--format", choices=["markdown", "html", "json"], default="markdown", help="Output format")
    args = parser.parse_args()

    env_path = Path(args.env_file).resolve()
    env_vars = load_env_vars(env_path)

    base_url = args.base_url or os.getenv("CRAWL4AI_BASE_URL") or env_vars.get("CRAWL4AI_BASE_URL", "http://127.0.0.1:11235")
    token = args.token or os.getenv("CRAWL4AI_API_TOKEN") or env_vars.get("CRAWL4AI_API_TOKEN", "")

    endpoint = f"{base_url.rstrip('/')}/crawl"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = json.dumps({"urls": [args.url]}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if not data.get("success"):
                print(f"ERROR: {data}", file=sys.stderr)
                return 1

            res = data.get("results", [{}])[0]
            content = ""
            if args.format == "json":
                content = json.dumps(res, indent=2)
            elif args.format == "html":
                content = res.get("html", "")
            else:
                content = res.get("markdown", "") or res.get("cleaned_html", "")

            if args.output:
                Path(args.output).write_text(content, encoding="utf-8")
                print(f"[+] Output saved to: {args.output}")
            else:
                print(content)
            return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
