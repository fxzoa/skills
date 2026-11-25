#!/usr/bin/env python3
import argparse, shutil, sqlite3, sys
from pathlib import Path

def backup_sqlite(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(src)) as s, sqlite3.connect(str(dst)) as d:
        s.backup(d)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--env-file", default="../.env")
    p.add_argument("--db-file", default="../data/app.db")
    p.add_argument("--metadata", default="dataset-metadata.json")
    p.add_argument("--stage-dir", default="/tmp/sample-app-dataset_stage")
    a = p.parse_args()
    sdir = Path(__file__).resolve().parent
    env_src, db_src, meta_src, stage = (sdir / a.env_file).resolve(), (sdir / a.db_file).resolve(), (sdir / a.metadata).resolve(), Path(a.stage_dir).resolve()
    if not env_src.is_file() or not meta_src.is_file():
        print("[ERROR] Missing .env or dataset-metadata.json", file=sys.stderr)
        return 1
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    shutil.copy2(meta_src, stage / "dataset-metadata.json")
    shutil.copy2(env_src, stage / ".env")
    if db_src.is_file():
        backup_sqlite(db_src, stage / "app.db")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
