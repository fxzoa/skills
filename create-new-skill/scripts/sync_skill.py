#!/usr/bin/env python3
"""sync_skill.py: Deterministically sync, diff, and audit skill between source and target directories."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_validate(skill_dir: Path) -> int:
    """Run validate_skill.py against the source skill directory."""
    validate_script = Path(__file__).parent / "validate_skill.py"
    if not validate_script.is_file():
        print(f"ERROR: validate_skill.py not found at {validate_script}", file=sys.stderr)
        return 1

    res = subprocess.run([sys.executable, str(validate_script), str(skill_dir)])
    return res.returncode


def get_all_relative_files(base_dir: Path) -> list[str]:
    """Collect sorted relative file paths excluding cache and VCS directories."""
    rel_files = []
    for root, _, files in os.walk(base_dir):
        if "__pycache__" in root or ".git" in root:
            continue
        for f in files:
            p = Path(root) / f
            rel_files.append(str(p.relative_to(base_dir)))
    return sorted(rel_files)


def compare_dirs(src: Path, dst: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (only_src, only_dst, differing) relative paths."""
    src_files = set(get_all_relative_files(src))
    dst_files = set(get_all_relative_files(dst)) if dst.exists() else set()

    only_src = sorted(list(src_files - dst_files))
    only_dst = sorted(list(dst_files - src_files))
    common = sorted(list(src_files & dst_files))

    differing = [rel for rel in common if not filecmp.cmp(src / rel, dst / rel, shallow=False)]
    return only_src, only_dst, differing


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic skill sync, diff, and audit tool.")
    parser.add_argument("--src", required=True, help="Source skill directory")
    parser.add_argument("--dst", required=True, help="Target destination skill directory (e.g. /mnt/d/skills/<name>-skill)")
    parser.add_argument("--apply", action="store_true", help="Apply synchronization (copy files)")
    parser.add_argument("--delete", action="store_true", help="Delete files present only in --dst (requires --apply)")
    parser.add_argument("--skip-validation", action="store_true", help="Skip pre-sync validate_skill check")
    args = parser.parse_args()

    if args.delete and not args.apply:
        print("ERROR: --delete requires --apply.", file=sys.stderr)
        return 1

    src = Path(args.src).resolve()
    dst = Path(args.dst).resolve()

    if not src.is_dir():
        print(f"ERROR: Source directory not found: {src}", file=sys.stderr)
        return 1

    # 1. 決定論的検証 (validate_skill)
    if not args.skip_validation:
        print(f"[*] Running deterministic validation on {src}...")
        code = run_validate(src)
        if code != 0:
            print("[!] Validation failed. Aborting sync.", file=sys.stderr)
            return code
        print("[+] Validation passed.")

    # 2. 差分検査 (diff)
    print(f"[*] Comparing {src} -> {dst}...")
    only_src, only_dst, differing = compare_dirs(src, dst)

    if not only_src and not only_dst and not differing:
        print("[OK] Source and destination are 100% in sync.")
        return 0

    print("\n--- Diff Summary ---")
    if only_src:
        print(f"  Only in source ({len(only_src)} files):")
        for f in only_src[:10]:
            print(f"    + {f}")
        if len(only_src) > 10:
            print(f"    ... and {len(only_src) - 10} more")
    if only_dst:
        print(f"  Only in destination ({len(only_dst)} files):")
        for f in only_dst[:10]:
            print(f"    - {f}")
        if len(only_dst) > 10:
            print(f"    ... and {len(only_dst) - 10} more")
    if differing:
        print(f"  Modified content ({len(differing)} files):")
        for f in differing:
            print(f"    M {f}")

    # 3. 同期反映 (apply)
    if args.apply:
        print(f"\n[*] Applying synchronization to {dst}...")
        dst.mkdir(parents=True, exist_ok=True)
        for rel in only_src + differing:
            src_file = src / rel
            dst_file = dst / rel
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
        if args.delete and only_dst:
            for rel in only_dst:
                (dst / rel).unlink(missing_ok=True)
            print(f"[*] Deleted {len(only_dst)} extraneous file(s) from {dst}.")
        elif only_dst:
            print("[NOTE] Extraneous files in destination were preserved (pass --delete to mirror-delete).")
        print("[SUCCESS] Synchronization completed deterministically.")
        return 0

    print("\n[NOTE] Dry-run complete. Run with --apply to synchronize.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
