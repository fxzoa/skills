#!/usr/bin/env python3
"""Verify VPC peering status, VM memory/Swap usage, and Docker Compose container health across all mesh nodes."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify multi-project GCP Free Tier VM mesh.")
    parser.add_argument(
        "--node",
        action="append",
        required=True,
        help="Node spec '<account>|<vm>|<project>|<stack>' (repeatable).",
    )
    parser.add_argument("--hub-account", default="", help="Optional hub gcloud account to check VPC peerings.")
    parser.add_argument("--hub-project", default="", help="Optional hub project ID.")
    parser.add_argument("--vpc", default="coin-vpc", help="VPC network name (default: coin-vpc).")
    parser.add_argument("--zone", default="us-central1-a", help="GCE zone (default: us-central1-a).")
    parser.add_argument("--tail", type=int, default=5, help="Number of container log lines to show (default: 5).")
    args = parser.parse_args()

    if args.hub_account and args.hub_project:
        print(f"=== VPC Peerings ({args.hub_project} / {args.vpc}) ===")
        env = os.environ.copy()
        env["CLOUDSDK_CORE_ACCOUNT"] = args.hub_account
        subprocess.run(
            ["gcloud", "compute", "networks", "peerings", "list", f"--network={args.vpc}", f"--project={args.hub_project}"],
            env=env,
            check=False,
        )

    failed = False
    for spec in args.node:
        parts = spec.split("|")
        if len(parts) != 4:
            print(f"[ERROR] Invalid --node spec: {spec}. Expected '<account>|<vm>|<project>|<stack>'.", file=sys.stderr)
            return 1
        account, vm, project, stack = parts
        print(f"\n================ {vm} ({project}) ================")
        env = os.environ.copy()
        env["CLOUDSDK_CORE_ACCOUNT"] = account
        cmd = (
            f"free -m | grep -E 'Mem|Swap' && "
            f"cd ~/app/{stack} && sudo docker compose ps && "
            f"sudo docker compose logs --tail={args.tail}"
        )
        res = subprocess.run(
            ["gcloud", "compute", "ssh", vm, f"--zone={args.zone}", f"--project={project}", f"--command={cmd}"],
            env=env,
        )
        if res.returncode != 0:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
