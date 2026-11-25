#!/usr/bin/env python3
"""deploy_cloudrun.py: Build container image with Cloud Build and deploy to Cloud Run."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_gcloud() -> str:
    path = shutil.which("gcloud")
    if path:
        return path
    for p in ["/snap/bin/gcloud", "/usr/bin/gcloud", "/usr/local/bin/gcloud"]:
        if shutil.which(p):
            return p
    raise FileNotFoundError("Google Cloud SDK ('gcloud') binary not found in PATH.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and deploy container to Cloud Run.")
    parser.add_argument("--configuration", "-c", help="gcloud configuration name")
    parser.add_argument("--project", "-p", help="GCP Project ID")
    parser.add_argument("--region", "-r", default="asia-northeast1", help="GCP Region")
    parser.add_argument("--service", "-s", default="coin-trade-all-in-one", help="Cloud Run service name")
    parser.add_argument("--repo", default="coin-trade-repo", help="Artifact Registry repo name")
    parser.add_argument("--config-file", default="deploy/cloudrun/cloudbuild.yaml", help="Path to cloudbuild.yaml")
    parser.add_argument("--source-dir", default=".", help="Root context path to upload")
    parser.add_argument("--allow-unauthenticated", action="store_true", default=True, help="Allow public access")
    args = parser.parse_args()

    gcloud = find_gcloud()
    cfg_flags = [f"--configuration={args.configuration}"] if args.configuration else []

    project = args.project
    if not project:
        p_res = subprocess.run([gcloud, "config", "get-value", "project"] + cfg_flags, stdout=subprocess.PIPE, text=True)
        project = p_res.stdout.strip()
        if not project:
            print("ERROR: GCP Project could not be determined.", file=sys.stderr)
            return 1

    config_path = Path(args.config_file).resolve()
    if not config_path.is_file():
        print(f"ERROR: Cloud Build config file not found: {config_path}", file=sys.stderr)
        return 1

    source_path = Path(args.source_dir).resolve()
    print(f"[*] Submitting Cloud Build from: {source_path}")
    print(f"[*] Target Project: {project}, Region: {args.region}, Service: {args.service}")

    substitutions = f"_REGION={args.region},_REPO_NAME={args.repo},_SERVICE_NAME={args.service}"

    cmd = [
        gcloud, "builds", "submit",
        f"--project={project}",
        f"--region={args.region}",
        f"--config={str(config_path)}",
        f"--substitutions={substitutions}",
        str(source_path),
    ] + cfg_flags

    build_res = subprocess.run(cmd)
    if build_res.returncode != 0:
        print("[!] Cloud Build and deployment failed.", file=sys.stderr)
        return build_res.returncode

    if args.allow_unauthenticated:
        print("[*] Granting unauthenticated invoke permissions...")
        subprocess.run([
            gcloud, "run", "services", "add-iam-policy-binding", args.service,
            f"--project={project}",
            f"--region={args.region}",
            "--member=allUsers",
            "--role=roles/run.invoker",
            "--quiet",
        ] + cfg_flags, stdout=subprocess.DEVNULL)

    # Fetch deployed URL
    url_res = subprocess.run([
        gcloud, "run", "services", "describe", args.service,
        f"--project={project}",
        f"--region={args.region}",
        "--format=value(status.url)",
    ] + cfg_flags, stdout=subprocess.PIPE, text=True)

    if url_res.returncode == 0:
        print(f"\n[SUCCESS] Deployed Cloud Run Service URL: {url_res.stdout.strip()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
