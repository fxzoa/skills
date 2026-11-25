#!/usr/bin/env python3
"""Scaffold a Kaggle CPU App Hosting bundle with -notebook/-dataset suffixes and sqlite3.backup() sync."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Kaggle CPU App Hosting project.")
    parser.add_argument("--dir", required=True, help="Target kaggle/ directory")
    parser.add_argument("--owner", required=True, help="Kaggle username")
    parser.add_argument("--slug", required=True, help="Base app slug (suffixes added automatically)")
    parser.add_argument("--notebook-file", default="app_kaggle.ipynb", help="Notebook filename")
    parser.add_argument("--db-name", default="app.db", help="SQLite DB filename under data/")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    nb_slug = f"{args.slug}-notebook"
    ds_slug = f"{args.slug}-dataset"

    _write_json(base / "kernel-metadata.json", {
        "id": f"{args.owner}/{nb_slug}",
        "title": nb_slug,
        "code_file": args.notebook_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": False,
        "enable_tpu": False,
        "enable_internet": True,
        "dataset_sources": [f"{args.owner}/{ds_slug}"],
        "competition_sources": [],
        "kernel_sources": [],
        "model_sources": [],
    })

    ds_dir = base / "kaggle_private_dataset"
    _write_json(ds_dir / "dataset-metadata.json", {
        "title": ds_slug,
        "id": f"{args.owner}/{ds_slug}",
        "licenses": [{"name": "CC0-1.0"}],
    })

    prep_py = ds_dir / "prepare_dataset.py"
    prep_py.write_text(
        f'''#!/usr/bin/env python3
import argparse, shutil, sqlite3, sys
from pathlib import Path

def backup_sqlite(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(src)) as s, sqlite3.connect(str(dst)) as d:
        s.backup(d)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--env-file", default="../.env")
    p.add_argument("--db-file", default="../data/{args.db_name}")
    p.add_argument("--metadata", default="dataset-metadata.json")
    p.add_argument("--stage-dir", default="/tmp/{ds_slug}_stage")
    a = p.parse_args()
    sdir = Path(__file__).resolve().parent
    env_src, db_src, meta_src, stage = (sdir / a.env_file).resolve(), (sdir / a.db_file).resolve(), (sdir / a.metadata).resolve(), Path(a.stage_dir).resolve()
    if not env_src.is_file() or not meta_src.is_file():
        print("[ERROR] Missing .env or dataset-metadata.json", file=sys.stderr)
        return 1
    env_keys = {{k.split("=", 1)[0].strip(): k.split("=", 1)[1].strip() for k in env_src.read_text(encoding="utf-8").splitlines() if k.strip() and not k.strip().startswith("#") and "=" in k}}
    missing = [k for k in ("TUNNEL_HOST", "TUNNEL_PORT", "TUNNEL_HOSTNAME") if not env_keys.get(k)]
    if missing:
        print(f"[ERROR] Missing required keys in .env: {{', '.join(missing)}}", file=sys.stderr)
        return 1
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    shutil.copy2(meta_src, stage / "dataset-metadata.json")
    shutil.copy2(env_src, stage / ".env")
    if db_src.is_file():
        backup_sqlite(db_src, stage / "{args.db_name}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
''',
        encoding="utf-8",
    )

    pub_sh = ds_dir / "publish_kaggle_dataset.sh"
    pub_sh.write_text(
        f'''#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
STAGE_DIR="/tmp/{ds_slug}_stage"
MODE="${{1:-version}}"
MESSAGE="${{2:-Update Kaggle app state}}"
python3 "${{SCRIPT_DIR}}/prepare_dataset.py" --stage-dir "${{STAGE_DIR}}"
case "${{MODE}}" in
  create) kaggle datasets create -p "${{STAGE_DIR}}" -r zip ;;
  version) kaggle datasets version -p "${{STAGE_DIR}}" -m "${{MESSAGE}}" -r zip ;;
  *) echo "Usage: $0 [create|version] [message]" >&2; exit 1 ;;
esac
''',
        encoding="utf-8",
    )

    (base / "http.rest").write_text(
        """@localUrl = http://{{$dotenv TUNNEL_HOST}}:{{$dotenv TUNNEL_PORT}}
@tunnelUrl = https://{{$dotenv TUNNEL_HOSTNAME}}

### Health Check (Local)
GET {{localUrl}}/health

### Health Check (Tunnel)
GET {{tunnelUrl}}/health
""",
        encoding="utf-8",
    )

    for script in [prep_py, pub_sh]:
        script.chmod(0o755)
    print(f"[OK] Scaffolded Kaggle App Hosting bundle in {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
