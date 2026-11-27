#!/usr/bin/env python3
"""Inject per-account short-lived OAuth2 access tokens into TF_VAR_access_tokens and run Terraform."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


def get_token(account: str) -> str:
    res = subprocess.run(
        ["gcloud", "auth", "print-access-token", f"--account={account}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if res.returncode != 0:
        print(f"[ERROR] Failed to get token for {account}: {res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
    return res.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Terraform across multi-account GCP projects using OAuth2 tokens.")
    parser.add_argument("--tf-dir", required=True, help="Path to Terraform root directory.")
    parser.add_argument(
        "--node",
        action="append",
        required=True,
        help="Node key and gcloud account in format '<node_key>:<email>' (repeatable).",
    )
    parser.add_argument("--action", choices=["plan", "apply", "output"], default="plan", help="Terraform action.")
    parser.add_argument("--target", action="append", default=[], help="Optional Terraform -target resource.")
    parser.add_argument("--auto-approve", action="store_true", help="Pass -auto-approve on apply.")
    args = parser.parse_args()

    tokens: dict[str, str] = {}
    for item in args.node:
        if ":" not in item:
            print(f"[ERROR] Invalid --node format: {item}. Expected '<node_key>:<email>'.", file=sys.stderr)
            return 1
        key, account = item.split(":", 1)
        tokens[key] = get_token(account)

    env = os.environ.copy()
    env["TF_VAR_access_tokens"] = json.dumps(tokens)

    cmd = ["terraform", args.action]
    if args.action in ("plan", "apply"):
        cmd.append("-input=false")
        for tgt in args.target:
            cmd.append(f"-target={tgt}")
    if args.action == "apply" and args.auto_approve:
        cmd.append("-auto-approve")

    print(f"[*] Running {' '.join(cmd)} in {args.tf_dir} for {len(tokens)} project(s)...")
    res = subprocess.run(cmd, cwd=args.tf_dir, env=env)
    return res.returncode


if __name__ == "__main__":
    raise SystemExit(main())
