#!/usr/bin/env python3
"""
Register or update Cloudflare DNS record for a GCE VM via dns-worker API.
Automatically retrieves the VM's external IP if not specified.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def get_vm_ip(vm: str, zone: str, project: str) -> str:
    """Fetch external IP of the GCE VM."""
    cmd = [
        "gcloud", "compute", "instances", "describe", vm,
        f"--zone={zone}",
        f"--project={project}",
        "--format=get(networkInterfaces[0].accessConfigs[0].natIP)",
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Failed to fetch VM IP: {res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
    ip = res.stdout.strip()
    if not ip:
        print(f"[ERROR] VM {vm} does not appear to have an external IP assigned.", file=sys.stderr)
        sys.exit(1)
    return ip


def get_api_key() -> str:
    """Retrieve DNS_WORKER_API_KEY from env or standard credential files."""
    import os
    if os.environ.get("DNS_WORKER_API_KEY"):
        return os.environ["DNS_WORKER_API_KEY"]

    search_paths = [
        Path("/mnt/d/conf/.env"),
        Path("/mnt/d/.env.nan"),
        Path("/mnt/d/cf-workers/dns-worker/.env"),
    ]
    for p in search_paths:
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:].strip()
                if line.startswith("DNS_WORKER_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip("\"'")
                    if val and val != "<YOUR_DNS_WORKER_API_KEY>":
                        return val

    print("[ERROR] DNS_WORKER_API_KEY not found in environment or /mnt/d/conf/.env", file=sys.stderr)
    sys.exit(1)


def register_dns(
    api_url: str,
    api_key: str,
    zone: str,
    name: str,
    content: str,
    record_type: str = "A",
    ttl: int = 300,
    proxied: bool = False,
    comment: str = "",
    dry_run: bool = False,
) -> dict:
    """Call dns-worker API to register or update DNS record."""
    payload = {
        "zone": zone,
        "name": name,
        "type": record_type,
        "content": content,
        "ttl": ttl,
        "proxied": proxied,
        "comment": comment or f"Automated mapping for {name}.{zone}",
    }
    if dry_run:
        payload["dry_run"] = True

    url = f"{api_url.rstrip('/')}/dns"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        if e.code == 409:
            print(f"[INFO] DNS record for {name}.{zone} already exists (HTTP 409). Checking existing record...")
            return {"ok": True, "already_exists": True, "details": err_body}
        print(f"[ERROR] DNS API returned HTTP {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Register GCE VM IP to Cloudflare DNS via dns-worker API.")
    parser.add_argument("--vm", required=True, help="Target GCE VM instance name")
    parser.add_argument("--subdomain", required=True, help="Subdomain name (e.g., 'kline')")
    parser.add_argument("--zone", default="btczoa.app", help="Cloudflare zone name (default: btczoa.app)")
    parser.add_argument("--api-url", default="https://dns.btczoa.app", help="dns-worker API URL")
    parser.add_argument("--project", default="", help="GCP project ID (default: gcloud config project)")
    parser.add_argument("--zone-gcp", default="", help="GCP zone (default: us-central1-a)")
    parser.add_argument("--ip", default="", help="Override external IP (optional)")
    parser.add_argument("--proxied", action="store_true", help="Enable Cloudflare CDN proxy (default: false for direct SSH/Redis)")
    parser.add_argument("--ttl", type=int, default=300, help="DNS TTL in seconds (default: 300)")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run validation without creating record")

    args = parser.parse_args()

    project = args.project
    if not project:
        res = subprocess.run(["gcloud", "config", "get-value", "project"], stdout=subprocess.PIPE, text=True)
        project = res.stdout.strip()
    zone_gcp = args.zone_gcp
    if not zone_gcp:
        res = subprocess.run(["gcloud", "config", "get-value", "compute/zone"], stdout=subprocess.PIPE, text=True)
        zone_gcp = res.stdout.strip() or "us-central1-a"

    # Get IP
    ip = args.ip or get_vm_ip(args.vm, zone_gcp, project)
    api_key = get_api_key()

    fqdn = f"{args.subdomain}.{args.zone}" if not args.subdomain.endswith(args.zone) else args.subdomain
    short_name = args.subdomain.replace(f".{args.zone}", "")

    print(f"==================================================")
    print(f"Registering DNS Record via dns-worker API")
    print(f"  FQDN:       {fqdn}")
    print(f"  IP:         {ip}")
    print(f"  Zone:       {args.zone}")
    print(f"  Proxied:    {args.proxied}")
    print(f"  TTL:        {args.ttl}s")
    print(f"  Dry Run:    {args.dry_run}")
    print(f"==================================================")

    res = register_dns(
        api_url=args.api_url,
        api_key=api_key,
        zone=args.zone,
        name=short_name,
        content=ip,
        ttl=args.ttl,
        proxied=args.proxied,
        comment=f"GCE VM {args.vm} ({project})",
        dry_run=args.dry_run,
    )

    print("[SUCCESS] API response:")
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
