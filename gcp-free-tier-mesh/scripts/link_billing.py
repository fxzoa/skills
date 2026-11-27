#!/usr/bin/env python3
"""Link active GCP Billing Accounts to multiple projects (supports cross-account fallback)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys


def run_gcloud(args: list[str], account: str = "", check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["gcloud", *args]
    if account:
        cmd.append(f"--account={account}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] {' '.join(cmd)}\n{res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
    return res


def get_open_billing_account(account: str) -> str | None:
    res = run_gcloud(["billing", "accounts", "list", "--format=json"], account=account)
    accounts = json.loads(res.stdout or "[]")
    for item in accounts:
        if item.get("open") is True:
            return item["name"].split("/")[-1]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Link Billing Accounts across multiple GCP projects.")
    parser.add_argument(
        "--pair",
        action="append",
        required=True,
        help="Account and project pair in format '<email>:<project_id>' (repeatable).",
    )
    parser.add_argument("--fallback-owner", default="", help="Billing owner email when an account has 0 billing accounts.")
    parser.add_argument("--fallback-billing-id", default="", help="Fallback Billing Account ID owned by --fallback-owner.")
    args = parser.parse_args()

    for raw in args.pair:
        if ":" not in raw:
            print(f"[ERROR] Invalid --pair format: {raw}. Expected '<email>:<project_id>'.", file=sys.stderr)
            return 1
        account, project = raw.split(":", 1)

        info_res = run_gcloud(["billing", "projects", "describe", project, "--format=json"], account=account)
        info = json.loads(info_res.stdout or "{}")
        if info.get("billingEnabled"):
            print(f"[OK] {project} already linked ({info.get('billingAccountName')})")
            continue

        billing_id = get_open_billing_account(account)
        if billing_id:
            print(f"[*] Linking {project} -> {billing_id} using {account}...")
            run_gcloud(["billing", "projects", "link", project, f"--billing-account={billing_id}"], account=account)
            print(f"[OK] Linked {project} -> {billing_id}")
            continue

        if not args.fallback_owner or not args.fallback_billing_id:
            print(
                f"[ERROR] Account {account} has 0 open billing accounts and no --fallback-owner/--fallback-billing-id set.",
                file=sys.stderr,
            )
            return 1

        print(f"[*] {account} has 0 billing accounts. Granting roles/billing.projectManager to {args.fallback_owner} on {project}...")
        run_gcloud(
            [
                "projects",
                "add-iam-policy-binding",
                project,
                f"--member=user:{args.fallback_owner}",
                "--role=roles/billing.projectManager",
            ],
            account=account,
        )
        run_gcloud(
            ["billing", "projects", "link", project, f"--billing-account={args.fallback_billing_id}"],
            account=args.fallback_owner,
        )
        print(f"[OK] Cross-account linked {project} -> {args.fallback_billing_id} via {args.fallback_owner}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
