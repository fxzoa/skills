#!/usr/bin/env python3
"""provision_apis_and_repo.py: Enable required GCP services and ensure Artifact Registry repository exists."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys


def find_gcloud() -> str:
    path = shutil.which("gcloud")
    if path:
        return path
    for p in ["/snap/bin/gcloud", "/usr/bin/gcloud", "/usr/local/bin/gcloud"]:
        if shutil.which(p):
            return p
    raise FileNotFoundError("Google Cloud SDK ('gcloud') binary not found in PATH.")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Enable APIs and provision Artifact Registry.")
    parser.add_argument("--configuration", "-c", help="gcloud configuration name")
    parser.add_argument("--project", "-p", help="GCP Project ID (overrides configuration)")
    parser.add_argument("--region", "-r", default="asia-northeast1", help="GCP Region")
    parser.add_argument("--repo", default="coin-trade-repo", help="Artifact Registry repo name")
    args = parser.parse_args()

    gcloud = find_gcloud()
    cfg_flags = [f"--configuration={args.configuration}"] if args.configuration else []

    # Resolve project ID
    project = args.project
    if not project:
        p_res = run([gcloud, "config", "get-value", "project"] + cfg_flags)
        if p_res.returncode != 0 or not p_res.stdout.strip():
            print("ERROR: Could not resolve GCP Project ID.", file=sys.stderr)
            return 1
        project = p_res.stdout.strip()

    print(f"[*] Provisioning for Project: {project} (Region: {args.region})")

    # 1. Enable APIs
    apis = ["run.googleapis.com", "cloudbuild.googleapis.com", "artifactregistry.googleapis.com"]
    print(f"[*] Enabling APIs: {', '.join(apis)}...")
    res = run([gcloud, "services", "enable"] + apis + [f"--project={project}"] + cfg_flags)
    if res.returncode != 0:
        print(f"ERROR enabling services: {res.stderr}", file=sys.stderr)
        return 1

    # 2. Check and Create Artifact Registry
    print(f"[*] Ensuring Artifact Registry repository '{args.repo}' exists...")
    check_repo = run([
        gcloud, "artifacts", "repositories", "describe", args.repo,
        f"--location={args.region}", f"--project={project}"
    ] + cfg_flags)

    if check_repo.returncode != 0:
        print(f"[*] Creating repository '{args.repo}'...")
        create_repo = run([
            gcloud, "artifacts", "repositories", "create", args.repo,
            "--repository-format=docker",
            f"--location={args.region}",
            f"--project={project}",
            "--description=Container repository managed by cloudrun-deploy-skill"
        ] + cfg_flags)
        if create_repo.returncode != 0:
            print(f"ERROR creating repository: {create_repo.stderr}", file=sys.stderr)
            return 1
        print("[+] Artifact Registry repository created successfully.")
    else:
        print("[+] Artifact Registry repository already exists.")

    # 3. Grant IAM permissions to Cloud Build Service Account
    print("[*] Configuring IAM permissions for Cloud Build...")
    pnum_res = run([gcloud, "projects", "describe", project, "--format=value(projectNumber)"] + cfg_flags)
    if pnum_res.returncode == 0 and pnum_res.stdout.strip():
        pnum = pnum_res.stdout.strip()
        sa = f"serviceAccount:{pnum}@cloudbuild.gserviceaccount.com"
        for role in ["roles/run.admin", "roles/iam.serviceAccountUser"]:
            run([
                gcloud, "projects", "add-iam-policy-binding", project,
                f"--member={sa}", f"--role={role}"
            ] + cfg_flags)
        print("[+] Cloud Build IAM bindings configured.")

    print("[OK] Infrastructure provisioning complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
