#!/usr/bin/env python3
"""Safely copy non-empty secret keys from a master .env file to one or more target .env files without printing values."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely sync secret keys between .env files.")
    parser.add_argument("--src", required=True, help="Source .env file containing non-empty secret values.")
    parser.add_argument("--dst", action="append", required=True, help="Destination .env file (repeatable).")
    parser.add_argument("--key", action="append", required=True, help="Environment variable key to sync (repeatable).")
    args = parser.parse_args()

    src_lines = Path(args.src).read_text().splitlines()
    updates: dict[str, str] = {}
    for key in args.key:
        match = next((l for l in src_lines if l.startswith(f"{key}=")), "")
        val = match.split("=", 1)[1].strip() if "=" in match else ""
        if not val:
            print(f"[ERROR] Key '{key}' is missing or empty in {args.src}", file=sys.stderr)
            return 1
        updates[key] = match

    for dst_str in args.dst:
        dst_path = Path(dst_str)
        lines = dst_path.read_text().splitlines() if dst_path.exists() else []
        for key, new_line in updates.items():
            replaced = False
            for idx, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[idx] = new_line
                    replaced = True
            if not replaced:
                lines.append(new_line)
        dst_path.write_text("\n".join(lines) + "\n")
        print(f"[OK] Synced {len(updates)} key(s) -> {dst_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
