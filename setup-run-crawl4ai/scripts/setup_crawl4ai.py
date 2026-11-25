#!/usr/bin/env python3
"""setup_crawl4ai.py: Deterministic 1-click batch setup for Crawl4AI Docker container."""

from __future__ import annotations

import argparse
import os
import secrets
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


def find_docker() -> str:
    path = shutil.which("docker")
    if path:
        return path
    for p in ["/snap/bin/docker", "/usr/bin/docker", "/usr/local/bin/docker"]:
        if shutil.which(p):
            return p
    raise FileNotFoundError("Docker CLI not found in PATH.")


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def wait_for_health(base_url: str, timeout: int = 60) -> bool:
    endpoint = f"{base_url.rstrip('/')}/health"
    print(f"[*] Waiting for Crawl4AI health check at {endpoint}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(endpoint)
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    print("[+] Crawl4AI container is healthy and responding.")
                    return True
        except Exception:
            pass
        time.sleep(2)
    return False


def update_env_file(env_path: Path, port: int, token: str) -> None:
    base_url = f"http://127.0.0.1:{port}"
    env_content = ""
    if env_path.is_file():
        env_content = env_path.read_text(encoding="utf-8")

    lines = env_content.splitlines()
    filtered = [l for l in lines if not l.startswith("CRAWL4AI_BASE_URL=") and not l.startswith("CRAWL4AI_API_TOKEN=")]

    filtered.append(f"CRAWL4AI_BASE_URL={base_url}")
    filtered.append(f"CRAWL4AI_API_TOKEN={token}")

    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text("\n".join(filtered) + "\n", encoding="utf-8")
    print(f"[+] Synced credentials to: {env_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Crawl4AI Docker setup operator.")
    parser.add_argument("--port", type=int, default=11235, help="Host port to bind (default: 11235)")
    parser.add_argument("--token", help="API token (generated automatically if omitted)")
    parser.add_argument("--env-file", default="/mnt/d/conf/.env", help="Path to .env file for persistence")
    parser.add_argument("--force-recreate", action="store_true", help="Remove existing crawl4ai container")
    args = parser.parse_args()

    try:
        docker = find_docker()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # 1. Generate or use token
    token = args.token or secrets.token_hex(32)

    # 2. Check existing container
    ps = subprocess.run([docker, "ps", "-a", "--filter", "name=^/crawl4ai$", "--format", "{{.Status}}"],
                        stdout=subprocess.PIPE, text=True)
    exists = bool(ps.stdout.strip())

    if exists:
        if args.force_recreate:
            print("[*] Removing existing crawl4ai container...")
            subprocess.run([docker, "rm", "-f", "crawl4ai"], stdout=subprocess.DEVNULL)
            exists = False
        else:
            print("[*] Container 'crawl4ai' already exists. Checking if running...")
            if "Up" not in ps.stdout:
                print("[*] Starting existing crawl4ai container...")
                subprocess.run([docker, "start", "crawl4ai"])
            wait_for_health(f"http://127.0.0.1:{args.port}")
            update_env_file(Path(args.env_file).resolve(), args.port, token)
            return 0

    # 3. Check port availability
    if is_port_in_use(args.port):
        print(f"ERROR: Port {args.port} is already in use by another process.", file=sys.stderr)
        return 1

    # 4. Run Docker container
    print(f"[*] Starting Crawl4AI container on port {args.port}...")
    run_cmd = [
        docker, "run", "-d",
        "--name", "crawl4ai",
        "--restart", "unless-stopped",
        "-p", f"{args.port}:11235",
        "--shm-size=1g",
        "-e", f"CRAWL4AI_API_TOKEN={token}",
        "unclecode/crawl4ai:latest"
    ]
    res = subprocess.run(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"ERROR: Failed to run container: {res.stderr}", file=sys.stderr)
        return res.returncode

    # 5. Wait for health
    if not wait_for_health(f"http://127.0.0.1:{args.port}", timeout=60):
        print("ERROR: Container health check timed out.", file=sys.stderr)
        return 1

    # 6. Update .env
    update_env_file(Path(args.env_file).resolve(), args.port, token)

    print("\n[SUCCESS] Crawl4AI setup completed successfully!")
    print(f"Endpoint:  http://127.0.0.1:{args.port}")
    print(f"API Token: {token}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
