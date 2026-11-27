#!/usr/bin/env python3
"""Scaffold a standard Kaggle LLM notebook bundle with -notebook/-dataset suffixes (direct /tmp download)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Kaggle LLM notebook project structure.")
    parser.add_argument("--dir", required=True, help="Target kaggle/ directory")
    parser.add_argument("--owner", required=True, help="Kaggle username / ownerSlug")
    parser.add_argument("--slug", required=True, help="Base project slug (suffixes added automatically)")
    parser.add_argument("--notebook-file", default="notebook.ipynb", help="Notebook filename")
    parser.add_argument("--hf-repo", default="", help="Optional source Hugging Face repo ID")
    parser.add_argument("--model-file", default="", help="Optional source model filename in HF repo")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    nb_slug = f"{args.slug}-notebook"
    ds_slug = f"{args.slug}-env-dataset"

    # 1. kernel-metadata.json (no model_sources input, direct download to /tmp/models)
    _write_json(base / "kernel-metadata.json", {
        "id": f"{args.owner}/{nb_slug}",
        "title": nb_slug,
        "code_file": args.notebook_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_tpu": False,
        "enable_internet": True,
        "dataset_sources": [f"{args.owner}/{ds_slug}"],
        "competition_sources": [],
        "kernel_sources": [],
        "model_sources": [],
    })

    # 2. kaggle_private_dataset/
    ds_dir = base / "kaggle_private_dataset"
    _write_json(ds_dir / "dataset-metadata.json", {
        "title": ds_slug,
        "id": f"{args.owner}/{ds_slug}",
        "licenses": [{"name": "CC0-1.0"}],
    })
    prep_py = ds_dir / "prepare_dataset.py"
    prep_py.write_text(
        f'''#!/usr/bin/env python3
import argparse, shutil, sys
from pathlib import Path

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--env-file", default="../.env")
    p.add_argument("--metadata", default="dataset-metadata.json")
    p.add_argument("--stage-dir", default="/tmp/{ds_slug}")
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
''',
        encoding="utf-8",
    )
    pub_d = ds_dir / "publish_kaggle_dataset.sh"
    pub_d.write_text(
        f'''#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
STAGE_DIR="/tmp/{ds_slug}_stage"
MODE="${{1:-version}}"
MESSAGE="${{2:-Update .env}}"
python3 "${{SCRIPT_DIR}}/prepare_dataset.py" --stage-dir "${{STAGE_DIR}}"
case "${{MODE}}" in
  create) kaggle datasets create -p "${{STAGE_DIR}}" -r zip ;;
  version) kaggle datasets version -p "${{STAGE_DIR}}" -m "${{MESSAGE}}" -r zip ;;
  *) echo "Usage: $0 [create|version] [message]" >&2; exit 1 ;;
esac
''',
        encoding="utf-8",
    )

    # 3. http.rest template
    (base / "http.rest").write_text(
        '''@localUrl = http://{{$dotenv TUNNEL_HOST}}:{{$dotenv TUNNEL_PORT}}
@tunnelUrl = https://{{$dotenv TUNNEL_HOSTNAME}}
@apiKey = {{$dotenv LLM_API_KEY}}
@modelName = {{$dotenv MODEL_NAME}}

### Health Check (Local)
GET {{localUrl}}/healthz

### Health Check (Tunnel)
GET {{tunnelUrl}}/healthz

### Server Status (Tunnel)
GET {{tunnelUrl}}/api/v1/status
Authorization: Bearer {{apiKey}}

### List Models (Tunnel)
GET {{tunnelUrl}}/v1/models
Authorization: Bearer {{apiKey}}

### Chat Completions (Tunnel)
POST {{tunnelUrl}}/v1/chat/completions
Content-Type: application/json
Authorization: Bearer {{apiKey}}

{
  "model": "{{modelName}}",
  "messages": [{"role": "user", "content": "Hello!"}],
  "max_tokens": 128,
  "stream": false
}
''',
        encoding="utf-8",
    )

    for script in [prep_py, pub_d]:
        script.chmod(0o755)
    print(f"[OK] Scaffolded Kaggle bundle in {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
