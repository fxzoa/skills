#!/usr/bin/env python3
"""Export and gzip local Docker images for transfer to e2-micro VMs without registry push."""

from __future__ import annotations

import argparse
import gzip
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Package local Docker images into .tar.gz archives.")
    parser.add_argument(
        "--bundle",
        action="append",
        required=True,
        help="Bundle spec '<bundle_name>=<image1>,<image2>,...' (repeatable).",
    )
    parser.add_argument("--out-dir", required=True, help="Output directory for .tar.gz archives.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for spec in args.bundle:
        if "=" not in spec:
            print(f"[ERROR] Invalid --bundle format: {spec}. Expected '<name>=<img1>,<img2>'.", file=sys.stderr)
            return 1
        name, imgs_raw = spec.split("=", 1)
        images = [i.strip() for i in imgs_raw.split(",") if i.strip()]
        dest = out_dir / f"{name}.tar.gz"
        print(f"[*] Exporting {images} -> {dest}...")

        proc = subprocess.Popen(["docker", "save", *images], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc.stdout is not None
        with gzip.open(dest, "wb") as gz:
            shutil.copyfileobj(proc.stdout, gz)
        _, stderr = proc.communicate()
        if proc.returncode != 0:
            print(f"[ERROR] docker save failed: {stderr.decode()}", file=sys.stderr)
            return proc.returncode
        size_mb = dest.stat().st_size / (1024 * 1024)
        print(f"[OK] {dest} ({size_mb:.1f} MB)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
