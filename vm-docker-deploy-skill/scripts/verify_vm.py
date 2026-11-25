#!/usr/bin/env python3
"""
Verify status of Docker containers and host health on a remote VM.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify remote VM Docker containers.")
    parser.add_argument("--vm", required=True, help="Remote VM name")
    parser.add_argument("--project", default="", help="GCP Project ID")
    parser.add_argument("--zone", default="", help="GCP Zone")
    parser.add_argument("--remote-dir", default="", help="Remote app directory")

    args = parser.parse_args()

    project_arg = [f"--project={args.project}"] if args.project else []
    zone_arg = [f"--zone={args.zone}"] if args.zone else []

    check_cmd = "docker info --format 'Docker: {{.ServerVersion}}' 2>/dev/null || echo 'Docker not running'"
    if args.remote_dir:
        check_cmd += f" && cd {args.remote_dir} && sudo docker compose ps"
    else:
        check_cmd += " && sudo docker ps"

    cmd = ["gcloud", "compute", "ssh", args.vm] + zone_arg + project_arg + [f"--command={check_cmd}"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
