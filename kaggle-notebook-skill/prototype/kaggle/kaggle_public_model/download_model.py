#!/usr/bin/env python3
import argparse, os, subprocess
from pathlib import Path

HF_REPO = "org/sample-llm"
DEFAULT_FILENAME = "model.gguf"

def download_file(repo_id: str, filename: str, out_dir: Path, token: str | None) -> Path:
    dest = out_dir / filename
    try:
        from huggingface_hub import hf_hub_download
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir=str(out_dir), token=token)
        return dest
    except ImportError:
        url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
        cmd = ["curl", "-fSL", "-C", "-", url, "-o", str(dest)]
        if token:
            cmd.extend(["-H", f"Authorization: Bearer {token}"])
        subprocess.run(cmd, check=True)
        return dest

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--filename", default=DEFAULT_FILENAME)
    p.add_argument("--output-dir", default="/mnt/d/tmp/kaggle_models/sample-llm-model")
    p.add_argument("--token", default=os.getenv("HF_TOKEN"))
    a = p.parse_args()
    out_dir = Path(a.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Done: {download_file(HF_REPO, a.filename, out_dir, a.token)}")

if __name__ == "__main__":
    main()
