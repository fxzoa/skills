#!/usr/bin/env python3
"""Pre-check model/dataset dependencies on Kaggle Cloud, create if missing, then push notebook."""

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
    parser.add_argument("--model-work-dir", default="", help="Optional WORK_DIR arg for publish_kaggle_model.sh")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    km = json.loads((base / "kernel-metadata.json").read_text(encoding="utf-8"))

    # 1. Check & create Datasets
    for ds in km.get("dataset_sources", []):
        res = _run(["kaggle", "datasets", "status", ds], check=False)
        if res.returncode != 0:
            pub_ds = base / "kaggle_private_dataset" / "publish_kaggle_dataset.sh"
            if not pub_ds.is_file():
                print(f"[ERROR] Dataset {ds} missing and {pub_ds} not found.", file=sys.stderr)
                return 1
            _run([str(pub_ds), "create"])

    # 2. Check & create Models
    for ms in km.get("model_sources", []):
        parts = ms.split("/")
        model_ref = f"{parts[0]}/{parts[1]}"
        res = _run(["kaggle", "models", "get", model_ref], check=False)
        if res.returncode != 0:
            pub_m = base / "kaggle_public_model" / "publish_kaggle_model.sh"
            if not pub_m.is_file():
                print(f"[ERROR] Model {model_ref} missing and {pub_m} not found.", file=sys.stderr)
                return 1
            cmd = [str(pub_m)] + ([args.model_work_dir] if args.model_work_dir else [])
            _run(cmd)

    # 3. Push Notebook
    _run(["kaggle", "kernels", "push", "-p", str(base)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
