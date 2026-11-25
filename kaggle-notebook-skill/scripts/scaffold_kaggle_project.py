#!/usr/bin/env python3
"""Scaffold a standard Kaggle LLM notebook bundle with -notebook/-model/-dataset suffixes."""

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
    parser.add_argument("--hf-repo", required=True, help="Source Hugging Face repo ID")
    parser.add_argument("--model-file", required=True, help="Source model filename in HF repo")
    parser.add_argument("--instance-slug", default="default", help="Kaggle model instance slug")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    nb_slug = f"{args.slug}-notebook"
    model_slug = f"{args.slug}-model"
    ds_slug = f"{args.slug}-env-dataset"

    # 1. kernel-metadata.json
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
        "model_sources": [f"{args.owner}/{model_slug}/other/{args.instance_slug}/1"],
    })

    # 2. kaggle_public_model/
    pm_dir = base / "kaggle_public_model"
    _write_json(pm_dir / "model-metadata.json", {
        "ownerSlug": args.owner,
        "title": model_slug,
        "slug": model_slug,
        "subtitle": f"Public Kaggle mirror of {args.hf_repo}",
        "isPrivate": False,
        "description": f"# Model Summary\n\nPublic mirror of `{args.hf_repo}` (`{args.model_file}`).\n",
        "publishTime": "",
        "provenanceSources": f"https://huggingface.co/{args.hf_repo}",
    })
    _write_json(pm_dir / "model-instance-metadata.json", {
        "ownerSlug": args.owner,
        "modelSlug": model_slug,
        "instanceSlug": args.instance_slug,
        "framework": "other",
        "overview": f"Weights for {args.model_file}",
        "usage": f"Mount `{args.owner}/{model_slug}/other/{args.instance_slug}/1` in Kaggle notebook.",
        "licenseName": "Apache 2.0",
        "fineTunable": False,
        "trainingData": [],
        "modelInstanceType": "Unspecified",
        "baseModelInstanceId": 0,
        "externalBaseModelUrl": f"https://huggingface.co/{args.hf_repo}",
    })

    dl_py = pm_dir / "download_model.py"
    dl_py.write_text(
        f'''#!/usr/bin/env python3
import argparse, os, subprocess
from pathlib import Path

HF_REPO = "{args.hf_repo}"
DEFAULT_FILENAME = "{args.model_file}"

def download_file(repo_id: str, filename: str, out_dir: Path, token: str | None) -> Path:
    dest = out_dir / filename
    try:
        from huggingface_hub import hf_hub_download
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir=str(out_dir), token=token)
        return dest
    except ImportError:
        url = f"https://huggingface.co/{{repo_id}}/resolve/main/{{filename}}"
        cmd = ["curl", "-fSL", "-C", "-", url, "-o", str(dest)]
        if token:
            cmd.extend(["-H", f"Authorization: Bearer {{token}}"])
        subprocess.run(cmd, check=True)
        return dest

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--filename", default=DEFAULT_FILENAME)
    p.add_argument("--output-dir", default="/mnt/d/tmp/kaggle_models/{model_slug}")
    p.add_argument("--token", default=os.getenv("HF_TOKEN"))
    a = p.parse_args()
    out_dir = Path(a.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Done: {{download_file(HF_REPO, a.filename, out_dir, a.token)}}")

if __name__ == "__main__":
    main()
''',
        encoding="utf-8",
    )
    pub_m = pm_dir / "publish_kaggle_model.sh"
    pub_m.write_text(
        f'''#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
WORK_DIR="${{1:-/mnt/d/tmp/kaggle_models/{model_slug}}}"
python3 "${{SCRIPT_DIR}}/download_model.py" --output-dir "${{WORK_DIR}}"
cp "${{SCRIPT_DIR}}/model-instance-metadata.json" "${{WORK_DIR}}/model-instance-metadata.json"
kaggle models create -p "${{SCRIPT_DIR}}" 2>&1 || true
if ! kaggle models instances create -p "${{WORK_DIR}}" -r tar 2>&1; then
  kaggle models instances versions create "{args.owner}/{model_slug}/other/{args.instance_slug}" -p "${{WORK_DIR}}" -r tar -n "Update model"
fi
''',
        encoding="utf-8",
    )

    # 3. kaggle_private_dataset/
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

    # 4. http.rest template
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

    for script in [dl_py, pub_m, prep_py, pub_d]:
        script.chmod(0o755)
    print(f"[OK] Scaffolded Kaggle bundle in {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
