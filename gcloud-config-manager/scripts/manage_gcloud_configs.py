#!/usr/bin/env python3
"""
manage_gcloud_configs.py

Deterministic management of multi-account gcloud configurations.
Reads .env or CLI args and manages ~/.config/gcloud/configurations/ safely without
triggering interactive confirmation prompts or authorization blocks.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


GCLOUD_CONFIG_DIR = Path.home() / ".config" / "gcloud" / "configurations"


def ensure_config_dir():
    GCLOUD_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def parse_env_file(env_path: Path):
    """Parse GCP_CONFIG_<NODE>_* keys from .env file."""
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {env_path}")

    configs = {}
    default_zone = "us-central1-a"
    default_region = "us-central1"

    pattern = re.compile(r"^GCP_CONFIG_([A-Za-z0-9_]+)_(ACCOUNT|PROJECT|ZONE|REGION|VM_NAME|CIDR)=(.*)$")
    zone_pattern = re.compile(r"^GCP_DEFAULT_ZONE=(.*)$")
    region_pattern = re.compile(r"^GCP_DEFAULT_REGION=(.*)$")

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            zm = zone_pattern.match(line)
            if zm:
                default_zone = zm.group(1).strip()
                continue

            rm = region_pattern.match(line)
            if rm:
                default_region = rm.group(1).strip()
                continue

            m = pattern.match(line)
            if m:
                node = m.group(1).lower()
                key = m.group(2).lower()
                val = m.group(3).strip()

                if node not in configs:
                    configs[node] = {
                        "name": node,
                        "zone": default_zone,
                        "region": default_region,
                    }
                configs[node][key] = val

    # Fill default zones/regions
    for node, data in configs.items():
        if "zone" not in data or not data["zone"]:
            data["zone"] = default_zone
        if "region" not in data or not data["region"]:
            data["region"] = default_region

    return configs


def write_configuration(name: str, account: str, project: str, zone: str, region: str):
    """Write configuration INI file directly to bypass interactive CLI prompt."""
    ensure_config_dir()
    config_file = GCLOUD_CONFIG_DIR / f"config_{name}"

    content = f"""[core]
account = {account}
project = {project}

[compute]
zone = {zone}
region = {region}
"""
    config_file.write_text(content, encoding="utf-8")
    print(f"[OK] Wrote gcloud config: {name} -> {config_file}")


def list_configurations():
    """Run gcloud config configurations list and print output."""
    res = subprocess.run(["gcloud", "config", "configurations", "list"], capture_output=True, text=True)
    if res.returncode == 0:
        print(res.stdout)
    else:
        print(f"[ERROR] Failed to list configurations: {res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)


def activate_configuration(name: str):
    """Activate a specified configuration."""
    res = subprocess.run(["gcloud", "config", "configurations", "activate", name], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[OK] Activated configuration: {name}")
        print(res.stdout)
    else:
        print(f"[ERROR] Failed to activate configuration '{name}': {res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)


def main():
    parser = argparse.ArgumentParser(description="Manage gcloud multi-account configurations deterministically.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: sync-env
    p_sync = subparsers.add_parser("sync-env", help="Sync gcloud configurations from an .env file.")
    p_sync.add_argument("--env-file", default="/mnt/d/conf/.env", help="Path to .env file.")

    # Subcommand: set
    p_set = subparsers.add_parser("set", help="Create or update a single configuration.")
    p_set.add_argument("--name", required=True, help="Configuration name.")
    p_set.add_argument("--account", required=True, help="Google account email.")
    p_set.add_argument("--project", required=True, help="GCP project ID.")
    p_set.add_argument("--zone", default="us-central1-a", help="Default compute zone.")
    p_set.add_argument("--region", default="us-central1", help="Default compute region.")

    # Subcommand: list
    subparsers.add_parser("list", help="List all gcloud configurations.")

    # Subcommand: activate
    p_act = subparsers.add_parser("activate", help="Activate a gcloud configuration.")
    p_act.add_argument("name", help="Configuration name to activate.")

    args = parser.parse_args()

    if args.command == "sync-env":
        env_path = Path(args.env_file)
        configs = parse_env_file(env_path)
        if not configs:
            print(f"[WARN] No GCP_CONFIG_* definitions found in {env_path}")
            return
        for name, data in configs.items():
            if "account" in data and "project" in data:
                write_configuration(name, data["account"], data["project"], data["zone"], data["region"])
        print("\n=== Current Configurations ===")
        list_configurations()

    elif args.command == "set":
        write_configuration(args.name, args.account, args.project, args.zone, args.region)
        list_configurations()

    elif args.command == "list":
        list_configurations()

    elif args.command == "activate":
        activate_configuration(args.name)


if __name__ == "__main__":
    main()
