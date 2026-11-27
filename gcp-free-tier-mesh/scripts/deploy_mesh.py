#!/usr/bin/env python3
"""Prepare Swap, data permissions, Docker images, and .env files on a target VM, then invoke deploy_compose.py."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_DEPLOY_COMPOSE = "/home/ppbb/.gemini/antigravity-cli/skills/vm-docker-deploy/scripts/deploy_compose.py"


def run_cmd(cmd: list[str], env: dict[str, str]) -> None:
    res = subprocess.run(cmd, env=env)
    if res.returncode != 0:
        sys.exit(res.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy a mesh node stack to an e2-micro VM.")
    parser.add_argument("--compose", required=True, help="Local Docker Compose YAML path.")
    parser.add_argument("--vm", required=True, help="Target GCE VM instance name.")
    parser.add_argument("--project", required=True, help="GCP Project ID.")
    parser.add_argument("--account", required=True, help="gcloud account email for this project.")
    parser.add_argument("--zone", default="us-central1-a", help="GCE zone (default: us-central1-a).")
    parser.add_argument("--tar", default="", help="Optional .tar.gz Docker image archive to load on VM.")
    parser.add_argument("--env-map", action="append", default=[], help="Env sync '<local_env>:<remote_filename>' (repeatable).")
    parser.add_argument("--data-dir", action="append", default=[], help="Subdirectory under ~/app/<stack>/data/ to chmod 777.")
    parser.add_argument("--swap-gb", type=int, default=1, help="Swap size in GB if /swapfile is absent (default: 1).")
    parser.add_argument("--deploy-script", default=DEFAULT_DEPLOY_COMPOSE, help="Path to vm-docker-deploy deploy_compose.py.")
    args = parser.parse_args()

    compose_path = Path(args.compose).resolve()
    stack = compose_path.stem
    remote_dir = f"~/app/{stack}"
    env = os.environ.copy()
    env["CLOUDSDK_CORE_ACCOUNT"] = args.account

    # 1. Create Swap, remote directories, and writable data dirs (for non-root USER deno UID 1000)
    data_cmds = " ".join([f"{remote_dir}/data/{d}" for d in args.data_dir])
    chmod_cmd = " && ".join([f"chmod 777 {remote_dir}/data/{d}" for d in args.data_dir])
    prep_parts = [
        f"mkdir -p {remote_dir}/env {data_cmds}".strip(),
        f"if [ ! -f /swapfile ]; then sudo fallocate -l {args.swap_gb}G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile; fi",
    ]
    if chmod_cmd:
        prep_parts.append(chmod_cmd)

    print(f"[*] Preparing {args.vm} ({args.project})...")
    run_cmd(
        ["gcloud", "compute", "ssh", args.vm, f"--zone={args.zone}", f"--project={args.project}", f"--command={' && '.join(prep_parts)}"],
        env,
    )

    # 2. Transfer .env files
    for mapping in args.env_map:
        if ":" not in mapping:
            print(f"[ERROR] Invalid --env-map: {mapping}. Expected '<local>:<remote_name>'.", file=sys.stderr)
            return 1
        local_env, remote_name = mapping.split(":", 1)
        run_cmd(
            ["gcloud", "compute", "scp", local_env, f"{args.vm}:{remote_dir}/env/{remote_name}", f"--zone={args.zone}", f"--project={args.project}"],
            env,
        )

    # 3. Transfer and load Docker images if provided
    if args.tar:
        tar_path = Path(args.tar).resolve()
        remote_tar = f"{remote_dir}/{tar_path.name}"
        run_cmd(
            ["gcloud", "compute", "scp", str(tar_path), f"{args.vm}:{remote_tar}", f"--zone={args.zone}", f"--project={args.project}"],
            env,
        )
        load_cmd = (
            "if command -v docker >/dev/null 2>&1; then "
            f"sudo docker load -i {remote_tar} && rm -f {remote_tar}; "
            "else echo '[INFO] Docker not yet installed; run deploy_compose.py first or install Docker.'; fi"
        )
        run_cmd(
            ["gcloud", "compute", "ssh", args.vm, f"--zone={args.zone}", f"--project={args.project}", f"--command={load_cmd}"],
            env,
        )

    # 4. Delegate to vm-docker-deploy/scripts/deploy_compose.py
    run_cmd(
        [
            sys.executable,
            args.deploy_script,
            "--compose",
            str(compose_path),
            "--vm",
            args.vm,
            "--project",
            args.project,
            "--zone",
            args.zone,
        ],
        env,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
