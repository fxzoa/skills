#!/usr/bin/env python3
"""run_full_deployment.py: One-click deterministic pipeline for Cloud Run deployment and verification.

Executes:
1. inspect_gcloud_config (resolves Project, Account, Region)
2. provision_apis_and_repo (ensures APIs, Artifact Registry, IAM roles)
3. deploy_cloudrun (submits Cloud Build & deploys revision)
4. verify_cloudrun (validates Ready condition and HTTP health probe)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_step(script_name: str, args_list: list[str]) -> int:
    script_path = Path(__file__).parent / script_name
    if not script_path.is_file():
        print(f"ERROR: Script not found: {script_path}", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(script_path)] + args_list
    print(f"\n=======================================================")
    print(f"[PIPELINE STEP] Running {script_name}...")
    print(f"=======================================================")
    res = subprocess.run(cmd)
    return res.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="One-click deterministic Cloud Run deployment pipeline.")
    parser.add_argument("--configuration", "-c", help="gcloud configuration name (e.g. nanzhiyan)")
    parser.add_argument("--project", "-p", help="GCP Project ID override")
    parser.add_argument("--region", "-r", default="asia-northeast1", help="GCP Region")
    parser.add_argument("--service", "-s", default="coin-trade-all-in-one", help="Cloud Run service name")
    parser.add_argument("--repo", default="coin-trade-repo", help="Artifact Registry repo name")
    parser.add_argument("--config-file", default="deploy/cloudrun/cloudbuild.yaml", help="Path to cloudbuild.yaml")
    parser.add_argument("--source-dir", default=".", help="Root context path to upload")
    parser.add_argument("--path", default="/api/health", help="HTTP health probe path")
    args = parser.parse_args()

    common_cfg = [f"--configuration={args.configuration}"] if args.configuration else []

    # Step 1: Inspect
    inspect_args = list(common_cfg)
    code = run_step("inspect_gcloud_config.py", inspect_args)
    if code != 0:
        print("[!] Step 1 (Inspect Configuration) failed. Aborting pipeline.", file=sys.stderr)
        return code

    # Step 2: Provision
    prov_args = list(common_cfg) + [f"--region={args.region}", f"--repo={args.repo}"]
    if args.project:
        prov_args.append(f"--project={args.project}")
    code = run_step("provision_apis_and_repo.py", prov_args)
    if code != 0:
        print("[!] Step 2 (Provision APIs & Repo) failed. Aborting pipeline.", file=sys.stderr)
        return code

    # Step 3: Deploy
    deploy_args = list(common_cfg) + [
        f"--region={args.region}",
        f"--service={args.service}",
        f"--repo={args.repo}",
        f"--config-file={args.config_file}",
        f"--source-dir={args.source_dir}",
    ]
    if args.project:
        deploy_args.append(f"--project={args.project}")
    code = run_step("deploy_cloudrun.py", deploy_args)
    if code != 0:
        print("[!] Step 3 (Cloud Run Deploy) failed. Aborting pipeline.", file=sys.stderr)
        return code

    # Step 4: Verify
    verify_args = list(common_cfg) + [
        f"--region={args.region}",
        f"--service={args.service}",
        f"--path={args.path}",
    ]
    if args.project:
        verify_args.append(f"--project={args.project}")
    code = run_step("verify_cloudrun.py", verify_args)
    if code != 0:
        print("[!] Step 4 (Verification) failed.", file=sys.stderr)
        return code

    print("\n=======================================================")
    print("[SUCCESS] All pipeline steps completed successfully!")
    print("=======================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
