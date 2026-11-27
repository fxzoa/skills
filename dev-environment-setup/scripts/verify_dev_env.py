#!/usr/bin/env python3
"""
dev-environment-setup: verify_dev_env.py
Deterministic verification of installed CLI tools and environment variables.
"""
import shutil
import subprocess
import sys
import os

TOOLS = [
    {
        "name": "uv",
        "cmd": ["uv", "--version"],
        "path_override": os.path.expanduser("~/.local/bin/uv"),
    },
    {
        "name": "node",
        "cmd": ["bash", "-c", "export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \\. \"$NVM_DIR/nvm.sh\" && node -v"],
    },
    {
        "name": "npm",
        "cmd": ["bash", "-c", "export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \\. \"$NVM_DIR/nvm.sh\" && npm -v"],
    },
    {
        "name": "wrangler",
        "cmd": ["bash", "-c", "export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \\. \"$NVM_DIR/nvm.sh\" && wrangler --version"],
    },
    {
        "name": "gcloud",
        "cmd": [os.path.expanduser("~/google-cloud-sdk/bin/gcloud"), "--version"],
    },
    {
        "name": "colab",
        "cmd": [os.path.expanduser("~/.local/bin/colab"), "--help"],
    },
    {
        "name": "kaggle",
        "cmd": [os.path.expanduser("~/.local/bin/kaggle"), "--version"],
    },
]

def main() -> int:
    print("=== [Dev Environment CLI Verification] ===")
    failed = []
    
    for tool in TOOLS:
        name = tool["name"]
        cmd = tool["cmd"]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            if res.returncode == 0:
                out = (res.stdout or res.stderr).strip().splitlines()[0] if (res.stdout or res.stderr) else "OK"
                print(f"[PASS] {name:<10}: {out}")
            else:
                err = res.stderr.strip().splitlines()[0] if res.stderr else f"Exit {res.returncode}"
                print(f"[FAIL] {name:<10}: {err}")
                failed.append(name)
        except Exception as e:
            print(f"[FAIL] {name:<10}: {e}")
            failed.append(name)

    print("=" * 42)
    if failed:
        print(f"FAILED tools: {', '.join(failed)}")
        return 1
    print("All CLI tools are healthy and operational!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
