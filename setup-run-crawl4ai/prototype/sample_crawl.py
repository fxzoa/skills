#!/usr/bin/env python3
"""sample_crawl.py: Verify Crawl4AI local container by scraping a target URL."""

import argparse
import json
import os
import sys
import urllib.request


def main():
    parser = argparse.ArgumentParser(description="Sample Crawl4AI API verification.")
    parser.add_argument("--url", default="https://example.com", help="Target URL to crawl")
    parser.add_argument("--base-url", default=os.getenv("CRAWL4AI_BASE_URL", "http://127.0.0.1:11235"))
    parser.add_argument("--token", default=os.getenv("CRAWL4AI_API_TOKEN", ""))
    args = parser.parse_args()

    endpoint = f"{args.base_url.rstrip('/')}/crawl"
    headers = {"Content-Type": "application/json"}
    if args.token:
        headers["Authorization"] = f"Bearer {args.token}"

    payload = json.dumps({"urls": [args.url]}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")

    print(f"[*] Sending crawl request to {endpoint} for: {args.url}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                print("[SUCCESS] Crawl4AI scraped target URL successfully!")
                return 0
            else:
                print(f"[ERROR] Crawling failed: {data}", file=sys.stderr)
                return 1
    except Exception as e:
        print(f"[ERROR] Request failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
