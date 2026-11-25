#!/usr/bin/env python3
"""inspect_gcloud_config.py: Resolve and validate user-specified gcloud configuration and project."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from typing import Any, Dict


def find_gcloud() -> str:
    path = shutil.which("gcloud")
    if path:
        return path
    for p in ["/snap/bin/gcloud", "/usr/bin/gcloud", "/usr/local/bin/gcloud"]:
        if shutil.which(p):
            return p
    raise FileNotFoundError("Google Cloud SDK ('gcloud') binary not found in PATH.")


def run_cmd(cmd: list[str]) -> str:
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return res.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect gcloud configuration and active project.")
    parser.add_argument("--configuration", "-c", help="gcloud configuration name (e.g. nanzhiyan)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    try:
        gcloud = find_gcloud()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    config_flag = [f"--configuration={args.configuration}"] if args.configuration else []

    try:
        project = run_cmd([gcloud, "config", "get-value", "project"] + config_flag)
        account = run_cmd([gcloud, "config", "get-value", "account"] + config_flag)
        region = run_cmd([gcloud, "config", "get-value", "run/region"] + config_flag) or "asia-northeast1"

        # Determine actual config name
        config_name = args.configuration
        if not config_name:
            config_name = run_cmd([gcloud, "config", "configurations", "list", "--filter=IS_ACTIVE=true", "--format=value(name)"])

        info = {
            "configuration": config_name,
            "project_id": project,
            "account": account,
            "default_region": region,
            "gcloud_path": gcloud,
        }

        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(f"GCloud Configuration: {info['configuration']}")
            print(f"Project ID:           {info['project_id']}")
            print(f"Account:              {info['account']}")
            print(f"Default Region:       {info['default_region']}")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
