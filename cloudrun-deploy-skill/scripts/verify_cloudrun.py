#!/usr/bin/env python3
"""verify_cloudrun.py: Verify health endpoint, readiness, and conditions of a deployed Cloud Run service."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request


def find_gcloud() -> str:
    path = shutil.which("gcloud")
    if path:
        return path
    for p in ["/snap/bin/gcloud", "/usr/bin/gcloud", "/usr/local/bin/gcloud"]:
        if shutil.which(p):
            return p
    raise FileNotFoundError("Google Cloud SDK ('gcloud') binary not found in PATH.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Cloud Run service health and deployment state.")
    parser.add_argument("--service", "-s", default="coin-trade-all-in-one", help="Service name")
    parser.add_argument("--configuration", "-c", help="gcloud configuration name")
    parser.add_argument("--project", "-p", help="GCP Project ID")
    parser.add_argument("--region", "-r", default="asia-northeast1", help="GCP Region")
    parser.add_argument("--path", default="/api/health", help="HTTP path to verify")
    args = parser.parse_args()

    gcloud = find_gcloud()
    cfg_flags = [f"--configuration={args.configuration}"] if args.configuration else []

    project = args.project
    if not project:
        p_res = subprocess.run([gcloud, "config", "get-value", "project"] + cfg_flags, stdout=subprocess.PIPE, text=True)
        project = p_res.stdout.strip()

    print(f"[*] Checking Cloud Run service '{args.service}' in project '{project}'...")

    # Get URL
    desc = subprocess.run([
        gcloud, "run", "services", "describe", args.service,
        f"--project={project}",
        f"--region={args.region}",
        "--format=json",
    ] + cfg_flags, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if desc.returncode != 0:
        print(f"ERROR describing service: {desc.stderr}", file=sys.stderr)
        return 1

    svc_data = json.loads(desc.stdout)
    url = svc_data.get("status", {}).get("url")
    if not url:
        print("ERROR: Service URL could not be found.", file=sys.stderr)
        return 1

    print(f"[+] Service URL: {url}")

    # Inspect conditions
    conditions = svc_data.get("status", {}).get("conditions", [])
    ready_cond = next((c for c in conditions if c.get("type") == "Ready"), None)
    if ready_cond and ready_cond.get("status") == "True":
        print("[+] Cloud Run Ready condition: True")
    else:
        print(f"[!] Warning: Ready condition is {ready_cond.get('status') if ready_cond else 'Unknown'}")

    # Test HTTP endpoint
    target_url = f"{url.rstrip('/')}/{args.path.lstrip('/')}"
    print(f"[*] Probing endpoint: {target_url}...")
    try:
        req = urllib.request.Request(target_url, headers={"User-Agent": "cloudrun-deploy-verifier/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            status = resp.status
            print(f"[+] HTTP Status: {status}")
            print(f"[+] Response Body Preview: {body[:200]}")
            if status == 200:
                print("[SUCCESS] Cloud Run deployment verified successfully!")
                return 0
            else:
                print(f"[!] Warning: Non-200 status code: {status}")
                return 1
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[!] Connection failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
