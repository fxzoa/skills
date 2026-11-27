#!/usr/bin/env python3
"""
install_kiri.py - Deterministic installer for Kiri container engine and Docker tools.
Downloads Kiri release deb, extracts binaries to ~/.local/bin and ~/.local/libexec,
configures Docker CLI plugins (compose, buildx), and sets up Docker context.
"""

import os
import sys
import argparse
import shutil
import urllib.request
import subprocess
from pathlib import Path

KIRI_VERSION = "v0.2.2"
DEB_URL = f"https://github.com/libracoder/kiri/releases/download/{KIRI_VERSION}/kiri_0.2.2_amd64.deb"

def parse_args():
    parser = argparse.ArgumentParser(description="Install Kiri container engine and configure Docker CLI.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without modifying system.")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.dry_run:
        print("[*] Dry run mode enabled.")
        return

    home = Path.home()
    local_bin = home / ".local" / "bin"
    local_libexec = home / ".local" / "libexec" / "kiri"
    docker_plugins = home / ".docker" / "cli-plugins"
    kiri_run = home / ".kiri" / "run"
    tmp_dir = Path("/mnt/d/tmp/src/kiri_install")

    print(f"[*] Setting up directories under {home}...")
    local_bin.mkdir(parents=True, exist_ok=True)
    local_libexec.mkdir(parents=True, exist_ok=True)
    docker_plugins.mkdir(parents=True, exist_ok=True)
    kiri_run.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    deb_path = tmp_dir / "kiri.deb"
    extracted_dir = tmp_dir / "pkg"

    try:
        print(f"[*] Downloading Kiri {KIRI_VERSION} deb package from GitHub...")
        urllib.request.urlretrieve(DEB_URL, deb_path)

        print("[*] Extracting package with dpkg -x...")
        extracted_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["dpkg", "-x", str(deb_path), str(extracted_dir)], check=True)

        print("[*] Installing binaries to ~/.local/bin and ~/.local/libexec/kiri...")
        for b in (extracted_dir / "usr" / "bin").glob("*"):
            target = local_bin / b.name
            shutil.copy2(b, target)
            target.chmod(0o755)

        for item in (extracted_dir / "usr" / "libexec" / "kiri").glob("*"):
            target = local_libexec / item.name
            if item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item, target)
            else:
                shutil.copy2(item, target)
                target.chmod(0o755)

        print("[*] Linking Docker CLI and plugins...")
        docker_cli = local_libexec / "bin" / "docker"
        if docker_cli.exists():
            link = local_bin / "docker"
            if link.exists() or link.is_symlink():
                link.unlink()
            link.symlink_to(docker_cli)

        for plugin in ["docker-compose", "docker-buildx"]:
            src = local_libexec / "cli-plugins" / plugin
            if src.exists():
                dst = docker_plugins / plugin
                if dst.exists() or dst.is_symlink():
                    dst.unlink()
                dst.symlink_to(src)

        print("[*] Setting up Docker context for Kiri...")
        res = subprocess.run(["docker", "context", "ls", "-q"], capture_output=True, text=True)
        contexts = res.stdout.split()
        if "kiri" not in contexts:
            subprocess.run([
                "docker", "context", "create", "kiri",
                "--description", "Kiri Container Runtime",
                "--docker", "host=unix:///run/kiri/docker.sock"
            ], check=True)
        else:
            subprocess.run([
                "docker", "context", "update", "kiri",
                "--docker", "host=unix:///run/kiri/docker.sock"
            ], check=True)

        subprocess.run(["docker", "context", "use", "kiri"], check=True)

        print("[OK] Kiri installation and Docker CLI integration completed successfully.")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
