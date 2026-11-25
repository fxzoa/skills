#!/usr/bin/env python3
"""
Tear down, stop, or clean up Docker Compose workloads on a remote VM.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def gcloud_ssh(vm: str, zone: str, project: str, command: str) -> subprocess.CompletedProcess:
    """Execute a bash command on the remote VM via gcloud compute ssh."""
    cmd = [
        "gcloud", "compute", "ssh", vm,
        f"--zone={zone}",
        f"--project={project}",
        f"--command={command}",
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Command failed ({res.returncode}): {command}", file=sys.stderr)
        print(f"STDERR:\n{res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
    return res


def main() -> int:
    parser = argparse.ArgumentParser(description="Tear down Docker Compose stack on remote VM.")
    parser.add_argument("--vm", required=True, help="Remote VM name")
    parser.add_argument("--remote-dir", required=True, help="Remote directory containing docker-compose.yml")
    parser.add_argument("--project", default="", help="GCP project ID")
    parser.add_argument("--zone", default="", help="GCP zone")
    parser.add_argument("--volumes", action="store_true", help="Remove named volumes declared in Compose")
    parser.add_argument("--remove-dir", action="store_true", help="Delete remote directory after stopping")

    args = parser.parse_args()

    project = args.project
    if not project:
        res = subprocess.run(["gcloud", "config", "get-value", "project"], stdout=subprocess.PIPE, text=True)
        project = res.stdout.strip()
    zone = args.zone
    if not zone:
        res = subprocess.run(["gcloud", "config", "get-value", "compute/zone"], stdout=subprocess.PIPE, text=True)
        zone = res.stdout.strip() or "us-central1-a"

    vol_flag = "-v" if args.volumes else ""
    down_cmd = f"cd {args.remote_dir} && sudo docker compose down {vol_flag}"

    print(f"[*] Stopping containers in {args.remote_dir} on {args.vm}...")
    res = gcloud_ssh(args.vm, zone, project, down_cmd)
    print(res.stdout)

    if args.remove_dir:
        print(f"[*] Removing remote directory {args.remote_dir}...")
        del_cmd = f"rm -rf {args.remote_dir}"
        gcloud_ssh(args.vm, zone, project, del_cmd)
        print("[OK] Remote directory removed.")

    print("[SUCCESS] Teardown complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
