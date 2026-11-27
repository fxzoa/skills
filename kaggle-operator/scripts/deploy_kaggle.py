#!/usr/bin/env python3
"""Pre-check dataset dependencies on Kaggle Cloud, create if missing, then push notebook."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"$ {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, check=check)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify dependencies and push Kaggle notebook.")
    parser.add_argument("dir", help="Path to directory containing kernel-metadata.json")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    km = json.loads((base / "kernel-metadata.json").read_text(encoding="utf-8"))

    # 1. Check & create Datasets (e.g. private .env dataset)
    for ds in km.get("dataset_sources", []):
        res = _run(["kaggle", "datasets", "status", ds], check=False)
        if res.returncode != 0:
            pub_ds = base / "kaggle_private_dataset" / "publish_kaggle_dataset.sh"
            if not pub_ds.is_file():
                print(f"[ERROR] Dataset {ds} missing and {pub_ds} not found.", file=sys.stderr)
                return 1
            _run([str(pub_ds), "create"])

    # 2. Push Notebook (models are downloaded to /tmp/models within the notebook)
    _run(["kaggle", "kernels", "push", "-p", str(base)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
