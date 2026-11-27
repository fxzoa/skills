#!/usr/bin/env python3
import argparse, shutil, sys
from pathlib import Path

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--env-file", default="../.env")
    p.add_argument("--metadata", default="dataset-metadata.json")
    p.add_argument("--stage-dir", default="/tmp/sample-llm-env-dataset")
    a = p.parse_args()
    sdir = Path(__file__).resolve().parent
    env_src, meta_src, stage = (sdir / a.env_file).resolve(), (sdir / a.metadata).resolve(), Path(a.stage_dir).resolve()
    if not env_src.is_file() or not meta_src.is_file():
        print("[ERROR] Missing .env or dataset-metadata.json", file=sys.stderr)
        return 1
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    shutil.copy2(meta_src, stage / "dataset-metadata.json")
    shutil.copy2(env_src, stage / ".env")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
