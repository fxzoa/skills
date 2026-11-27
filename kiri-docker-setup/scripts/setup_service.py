#!/usr/bin/env python3
"""
setup_service.py - Deterministic systemd service configurator for Kiri.
Registers /etc/systemd/system/kiri.service, enables auto-start, and ensures
socket permissions allow non-root users.
Reads SUDO_PASSWORD from /mnt/d/conf/.env if present, otherwise prompts interactively.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

SERVICE_CONTENT = """[Unit]
Description=Kiri Container Daemon
After=network.target

[Service]
Type=simple
Environment=HOME=/root
Environment=KIRI_SOCKET=/run/kiri/docker.sock
ExecStart={kiri_bin} daemon
ExecStartPost=/bin/sh -c "sleep 0.5 && chmod 666 /run/kiri/docker.sock || true"
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Configure systemd service for Kiri.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without modifying system.")
    return parser.parse_args()

def get_sudo_password():
    env_file = Path("/mnt/d/conf/.env")
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "SUDO_PASSWORD=" in line:
                    return line.split("SUDO_PASSWORD=", 1)[1].strip().strip("\"'")
    return None

def run_sudo(cmd, password=None):
    if password:
        p = subprocess.Popen(["sudo", "-S"] + cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = p.communicate(input=password + "\n")
        if p.returncode != 0:
            raise RuntimeError(f"Command {' '.join(cmd)} failed: {stderr}")
        return stdout
    else:
        subprocess.run(["sudo"] + cmd, check=True)
        return ""

def main():
    args = parse_args()
    if args.dry_run:
        print("[*] Dry run mode enabled.")
        return

    home = Path.home()
    kiri_bin = home / ".local" / "bin" / "kiri"
    if not kiri_bin.exists():
        print(f"[!] Error: {kiri_bin} not found. Run install_kiri.py first.", file=sys.stderr)
        sys.exit(1)

    password = get_sudo_password()

    print("[*] Creating /etc/systemd/system/kiri.service...")
    content = SERVICE_CONTENT.format(kiri_bin=str(kiri_bin))
    
    if password:
        p = subprocess.Popen(["sudo", "-S", "tee", "/etc/systemd/system/kiri.service"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        p.communicate(input=f"{password}\n{content}")
    else:
        p = subprocess.Popen(["sudo", "tee", "/etc/systemd/system/kiri.service"], stdin=subprocess.PIPE, text=True)
        p.communicate(input=content)

    print("[*] Reloading systemd daemon...")
    run_sudo(["systemctl", "daemon-reload"], password)

    print("[*] Enabling and starting kiri.service...")
    run_sudo(["systemctl", "enable", "--now", "kiri.service"], password)

    print("[*] Checking kiri.service status...")
    out = run_sudo(["systemctl", "status", "kiri.service", "--no-pager"], password)
    print(out)
    print("[OK] Kiri systemd service configured and running successfully.")

if __name__ == "__main__":
    main()
