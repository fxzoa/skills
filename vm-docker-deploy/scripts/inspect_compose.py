#!/usr/bin/env python3
"""
Inspect a Docker Compose YAML file for volume mounts, ports, and environment dependencies.
Helps agents identify necessary file transfers and avoid mount pitfalls before deployment.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_yaml_simple(content: str) -> dict:
    """Lightweight YAML parser for Docker Compose services without heavy external dependencies."""
    services = {}
    current_service = None
    current_section = None

    lines = content.splitlines()
    in_services = False

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        if indent == 0 and stripped.startswith("services:"):
            in_services = True
            continue

        if not in_services:
            continue

        # Top level outside services
        if indent == 0 and not stripped.startswith("services:"):
            in_services = False
            continue

        if indent == 2 and stripped.endswith(":"):
            current_service = stripped[:-1].strip()
            services[current_service] = {
                "image": None,
                "volumes": [],
                "ports": [],
                "env_file": [],
                "environment": [],
            }
            current_section = None
            continue

        if current_service and indent == 4 and stripped.endswith(":"):
            current_section = stripped[:-1].strip()
            continue

        if current_service and indent >= 4 and stripped.startswith("image:"):
            services[current_service]["image"] = stripped.split(":", 1)[1].strip()
            continue

        if current_service and current_section in ["volumes", "ports", "env_file", "environment"]:
            if stripped.startswith("-"):
                val = stripped[1:].strip().strip("\"'")
                services[current_service][current_section].append(val)

    return services


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect Docker Compose YAML dependencies.")
    parser.add_argument("--compose", required=True, help="Path to Docker Compose YAML")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    compose_path = Path(args.compose).resolve()
    if not compose_path.exists():
        print(f"[ERROR] Compose file not found: {compose_path}", file=sys.stderr)
        return 1

    content = compose_path.read_text(encoding="utf-8")
    services = parse_yaml_simple(content)

    all_volumes = []
    all_env_files = []
    all_ports = []
    ssh_keys_detected = []

    for s_name, data in services.items():
        for vol in data["volumes"]:
            all_volumes.append((s_name, vol))
            if "ssh" in vol.lower() or "id_rsa" in vol or "google_compute_engine" in vol:
                ssh_keys_detected.append(vol)
        for ef in data["env_file"]:
            all_env_files.append((s_name, ef))
        for p in data["ports"]:
            all_ports.append((s_name, p))

    report = {
        "compose_file": str(compose_path),
        "service_count": len(services),
        "services": list(services.keys()),
        "volume_mounts": [f"{s}: {v}" for s, v in all_volumes],
        "env_files": [f"{s}: {ef}" for s, ef in all_env_files],
        "exposed_ports": [f"{s}: {p}" for s, p in all_ports],
        "ssh_key_references": ssh_keys_detected,
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("==================================================")
    print(f"Docker Compose Inspection: {compose_path.name}")
    print("==================================================")
    print(f"Services ({len(services)}): {', '.join(services.keys())}")

    if all_ports:
        print("\n[Exposed Ports]")
        for s, p in all_ports:
            print(f"  - [{s}] {p}")

    if all_volumes:
        print("\n[Volume Mounts]")
        for s, v in all_volumes:
            print(f"  - [{s}] {v}")

    if all_env_files:
        print("\n[Env Files]")
        for s, ef in all_env_files:
            print(f"  - [{s}] {ef}")

    if ssh_keys_detected:
        print("\n[NOTICE] SSH Key Mounts Detected:")
        for k in ssh_keys_detected:
            print(f"  ! {k}")
        print("  -> Ensure SSH key exists on remote VM with chmod 600 prior to container startup.")

    print("\n[OK] Inspection complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
