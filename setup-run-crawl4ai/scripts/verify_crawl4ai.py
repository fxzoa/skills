#!/usr/bin/env python3
"""verify_crawl4ai.py: Deterministic verification of Crawl4AI container, health, and scraping."""

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
    parser = argparse.ArgumentParser(description="Verify Crawl4AI local container status and scraping capability.")
    parser.add_argument("--base-url", help="Crawl4AI Base URL (e.g. http://127.0.0.1:11235)")
    parser.add_argument("--token", help="Crawl4AI API Token")
    parser.add_argument("--env-file", default="/mnt/d/conf/.env", help="Path to .env file")
    parser.add_argument("--test-url", default="https://example.com", help="Test URL to scrape")
    args = parser.parse_args()

    env_path = Path(args.env_file).resolve()
    env_vars = load_env_vars(env_path)

    base_url = args.base_url or os.getenv("CRAWL4AI_BASE_URL") or env_vars.get("CRAWL4AI_BASE_URL", "http://127.0.0.1:11235")
    token = args.token or os.getenv("CRAWL4AI_API_TOKEN") or env_vars.get("CRAWL4AI_API_TOKEN", "")

    print(f"[*] Testing Crawl4AI health at: {base_url}/health")
    try:
        health_req = urllib.request.Request(f"{base_url.rstrip('/')}/health")
        with urllib.request.urlopen(health_req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") == "ok":
                print(f"[+] Health check OK: version {data.get('version')}")
            else:
                print(f"[!] Warning: Unexpected health response: {data}")
    except Exception as e:
        print(f"[ERROR] Failed to connect to health endpoint: {e}", file=sys.stderr)
        return 1

    print(f"[*] Performing test scrape on: {args.test_url}")
    crawl_endpoint = f"{base_url.rstrip('/')}/crawl"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = json.dumps({"urls": [args.test_url]}).encode("utf-8")
    req = urllib.request.Request(crawl_endpoint, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                results = data.get("results", [])
                if results and "html" in results[0]:
                    print("[SUCCESS] Crawl4AI container is 100% operational!")
                    return 0
                else:
                    print("[!] Warning: Scrape succeeded but returned no content.")
                    return 1
            else:
                print(f"[ERROR] Scrape returned failure: {data}", file=sys.stderr)
                return 1
    except Exception as e:
        print(f"[ERROR] Scrape request failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
