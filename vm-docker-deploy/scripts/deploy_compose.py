#!/usr/bin/env python3
"""
Deploy Docker Compose workloads to cloud VMs (GCE / Linux).
Handles Docker installation, SSH key syncing, directory preparation,
file transfer via scp, and service health checks.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return completed process."""
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Command failed ({res.returncode}): {' '.join(cmd)}", file=sys.stderr)
        print(f"STDOUT:\n{res.stdout}", file=sys.stderr)
        print(f"STDERR:\n{res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
    return res


def gcloud_ssh(vm: str, zone: str, project: str, command: str) -> subprocess.CompletedProcess:
    """Execute a bash command on the remote VM via gcloud compute ssh."""
    cmd = [
        "gcloud", "compute", "ssh", vm,
        f"--zone={zone}",
        f"--project={project}",
        f"--command={command}",
    ]
    return run_cmd(cmd, check=True)


def gcloud_scp(src: str, dest: str, vm: str, zone: str, project: str) -> None:
    """Transfer a local file to remote VM via gcloud compute scp."""
    cmd = [
        "gcloud", "compute", "scp", src, f"{vm}:{dest}",
        f"--zone={zone}",
        f"--project={project}",
    ]
    run_cmd(cmd, check=True)


def ensure_docker(vm: str, zone: str, project: str) -> None:
    """Ensure Docker and Docker Compose Plugin are installed on remote VM."""
    print(f"[*] Checking Docker installation on {vm}...")
    check = subprocess.run(
        [
            "gcloud", "compute", "ssh", vm,
            f"--zone={zone}",
            f"--project={project}",
            "--command=which docker && which docker-compose || docker compose version",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check.returncode == 0:
        print("[OK] Docker and Docker Compose plugin are already installed.")
        return

    print("[!] Docker not detected. Provisioning Docker Engine and Docker Compose plugin...")
    install_script = (
        "sudo apt-get update && "
        "sudo apt-get install -y ca-certificates curl gnupg && "
        "sudo install -m 0755 -d /etc/apt/keyrings && "
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && "
        "sudo chmod a+r /etc/apt/keyrings/docker.gpg && "
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && '
        "sudo apt-get update && "
        "sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && "
        "sudo usermod -aG docker $USER && "
        "sudo systemctl enable docker && sudo systemctl start docker"
    )
    gcloud_ssh(vm, zone, project, install_script)
    print("[OK] Docker successfully installed.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy Docker Compose YAML to cloud VM.")
    parser.add_argument("--compose", required=True, help="Path to local Docker Compose YAML")
    parser.add_argument("--vm", required=True, help="Remote VM name (GCE instance)")
    parser.add_argument("--project", default="", help="GCP Project ID (default: gcloud config project)")
    parser.add_argument("--zone", default="", help="GCP Zone (default: gcloud config zone or us-central1-a)")
    parser.add_argument("--remote-dir", default="", help="Remote directory path (default: ~/app/<compose_stem>)")
    parser.add_argument("--env-file", default="", help="Path to local .env file (optional)")
    parser.add_argument("--ssh-key", default="", help="Path to local SSH private key for container mounts (optional)")
    parser.add_argument("--health-timeout", type=int, default=120, help="Seconds to wait for health checks (default: 120)")

    args = parser.parse_args()

    compose_path = Path(args.compose).resolve()
    if not compose_path.exists():
        print(f"[ERROR] Compose file not found: {compose_path}", file=sys.stderr)
        return 1

    # Resolve project & zone
    project = args.project
    if not project:
        res = run_cmd(["gcloud", "config", "get-value", "project"])
        project = res.stdout.strip()
    zone = args.zone
    if not zone:
        res = run_cmd(["gcloud", "config", "get-value", "compute/zone"], check=False)
        zone = res.stdout.strip() or "us-central1-a"

    service_name = compose_path.stem
    remote_dir = args.remote_dir or f"~/app/{service_name}"

    print(f"==================================================")
    print(f"Deploying Docker Compose to VM")
    print(f"  VM:        {args.vm}")
    print(f"  Project:   {project}")
    print(f"  Zone:      {zone}")
    print(f"  Compose:   {compose_path}")
    print(f"  Target:    {remote_dir}")
    print(f"==================================================")

    # 1. Ensure Docker is ready
    ensure_docker(args.vm, zone, project)

    # 2. Prepare remote directories
    print(f"[*] Preparing remote directories: {remote_dir} and ~/.ssh...")
    gcloud_ssh(args.vm, zone, project, f"mkdir -p {remote_dir} ~/.ssh && chmod 700 ~/.ssh")

    # 3. Transfer SSH key if specified or referenced
    ssh_key_path = Path(args.ssh_key).expanduser() if args.ssh_key else Path("~/.ssh/google_compute_engine").expanduser()
    if ssh_key_path.exists():
        print(f"[*] Syncing SSH key {ssh_key_path} to remote VM...")
        gcloud_scp(str(ssh_key_path), "~/.ssh/google_compute_engine", args.vm, zone, project)
        gcloud_ssh(args.vm, zone, project, "chmod 600 ~/.ssh/google_compute_engine")

    # 4. Transfer .env if provided
    if args.env_file:
        env_path = Path(args.env_file).resolve()
        if env_path.exists():
            print(f"[*] Syncing environment file {env_path}...")
            gcloud_scp(str(env_path), f"{remote_dir}/.env", args.vm, zone, project)

    # 5. Pre-create mount point files if referenced in Compose to prevent Docker directory-auto-creation trap
    # Also set default REDIS_SSH_KEY_PATH in .env if not already defined
    setup_env_cmd = (
        f"cd {remote_dir} && "
        f"if [ ! -f .env ]; then touch .env; fi && "
        f"if ! grep -q 'REDIS_SSH_KEY_PATH' .env; then "
        f"  echo \"REDIS_SSH_KEY_PATH=$HOME/.ssh/google_compute_engine\" >> .env; "
        f"fi"
    )
    gcloud_ssh(args.vm, zone, project, setup_env_cmd)

    # 6. Transfer Docker Compose YAML
    print(f"[*] Uploading compose file to {remote_dir}/docker-compose.yml...")
    gcloud_scp(str(compose_path), f"{remote_dir}/docker-compose.yml", args.vm, zone, project)

    # 7. Start containers
    print(f"[*] Launching containers via docker compose...")
    launch_cmd = f"cd {remote_dir} && sudo docker compose down && sudo docker compose up -d"
    gcloud_ssh(args.vm, zone, project, launch_cmd)

    # 8. Verification and Health Check Loop
    print(f"[*] Verifying container status (timeout: {args.health_timeout}s)...")
    start_time = time.time()
    healthy = False

    while time.time() - start_time < args.health_timeout:
        ps_res = gcloud_ssh(args.vm, zone, project, f"cd {remote_dir} && sudo docker compose ps --format json")
        output = ps_res.stdout.strip()
        print(f"--- Current Status ({int(time.time() - start_time)}s elapsed) ---")
        display_res = gcloud_ssh(args.vm, zone, project, f"cd {remote_dir} && sudo docker compose ps")
        print(display_res.stdout)

        # Check for unhealthy / exited states (avoid matching JSON key "ExitCode")
        if '"unhealthy"' in output.lower() or '"exited"' in output.lower() or '"dead"' in output.lower():
            time.sleep(5)
            continue

        if "running" in output.lower() or "healthy" in output.lower():
            healthy = True
            break
        time.sleep(5)

    if healthy:
        print("[SUCCESS] All services are deployed and operational!")
        logs_res = gcloud_ssh(args.vm, zone, project, f"cd {remote_dir} && sudo docker compose logs --tail=20")
        print("=== Recent Logs ===")
        print(logs_res.stdout)
        return 0
    else:
        print("[WARNING] Services started but healthcheck did not achieve healthy status within timeout.", file=sys.stderr)
        logs_res = gcloud_ssh(args.vm, zone, project, f"cd {remote_dir} && sudo docker compose logs --tail=50")
        print("=== Error Logs ===", file=sys.stderr)
        print(logs_res.stdout, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
