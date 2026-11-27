#!/usr/bin/env python3
"""
verify_and_deploy_chat_worker.py
chat-worker の型チェック・ユニットテスト・Cloudflare Workers デプロイ・疎通確認を実行する。
"""

import argparse
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


def run_cmd(cmd: list[str], cwd: Path) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd), check=True)


def check_http(url: str, headers: dict[str, str] | None = None, timeout: float = 10.0) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "chat-worker-verify/1.0", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        print(f"[ERROR] {url} -> HTTP {e.code}", file=sys.stderr)
        return e.code
    except Exception as e:
        print(f"[ERROR] {url} -> {e}", file=sys.stderr)
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Typecheck, test, deploy, and verify chat-worker")
    parser.add_argument("--chat-worker-dir", default="/mnt/d/cf-workers/chat-worker", help="Path to chat-worker repo")
    parser.add_argument("--deploy", action="store_true", help="Run npm run deploy (wrangler deploy)")
    parser.add_argument("--worker-url", default="https://chat.btczoa.app", help="Deployed chat-worker base URL")
    parser.add_argument("--upstream-url", default=None, help="Upstream AI service base URL (e.g. https://code-ai.btczoa.app)")
    parser.add_argument("--api-key", default=None, help="Upstream Bearer API key for /v1/models check")

    args = parser.parse_args()
    cw_dir = Path(args.chat_worker_dir)

    run_cmd(["npm", "run", "typecheck"], cw_dir)
    run_cmd(["npm", "test"], cw_dir)

    if args.deploy:
        run_cmd(["npm", "run", "deploy"], cw_dir)
        worker_health = f"{args.worker_url.rstrip('/')}/health"
        code = check_http(worker_health)
        if code != 200:
            return 1
        print(f"[OK] {worker_health} -> HTTP {code}")

    if args.upstream_url:
        up = args.upstream_url.rstrip("/")
        h_code = check_http(f"{up}/health")
        if h_code != 200:
            return 1
        print(f"[OK] {up}/health -> HTTP {h_code}")
        if args.api_key:
            m_code = check_http(f"{up}/v1/models", headers={"Authorization": f"Bearer {args.api_key}"})
            if m_code != 200:
                return 1
            print(f"[OK] {up}/v1/models -> HTTP {m_code}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
