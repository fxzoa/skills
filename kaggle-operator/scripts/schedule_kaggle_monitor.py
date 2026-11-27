#!/usr/bin/env python3
"""
schedule_kaggle_monitor.py
Kaggle カーネルのバッチ実行ステータスを定期監視し、
ERROR や COMPLETE 時に自動でログを取得・診断して自己改善ループ用の
サマリを出力するスケジューラ兼診断スクリプト。
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional

def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def get_kernel_id(kaggle_dir: str) -> str:
    meta_path = Path(kaggle_dir) / "kernel-metadata.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"kernel-metadata.json が見つかりません: {meta_path}")
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["id"]

def check_status(kernel_id: str) -> str:
    rc, out, err = run_cmd(["kaggle", "kernels", "status", kernel_id])
    return out.strip() if out.strip() else err.strip()

def download_output(kernel_id: str, out_dir: str) -> None:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    run_cmd(["kaggle", "kernels", "output", kernel_id, "-p", out_dir])

def parse_kaggle_logs(out_dir: str) -> tuple[list[str], str]:
    issues = []
    log_content = ""
    log_files = glob.glob(f"{out_dir}/*.log") + glob.glob(f"{out_dir}/**/*.log", recursive=True)

    for lf in log_files:
        try:
            with open(lf, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                log_content += f"\n=== {os.path.basename(lf)} ===\n" + "\n".join(content.split("\n")[-40:])
                lower = content.lower()
                if "error 137" in lower or "oom" in lower or "out of memory" in lower:
                    issues.append(f"OOM_KILLED (137): {os.path.basename(lf)} でメモリ超過が検知されました。")
                if "modulenotfounderror" in lower or "no module named" in lower:
                    issues.append(f"MISSING_MODULE: {os.path.basename(lf)} で依存モジュールの不足が検知されました。")
                if "404 client error" in lower or "not found" in lower:
                    issues.append(f"RESOURCE_NOT_FOUND: {os.path.basename(lf)} で外部リソース取得エラーが検知されました。")
                if "syntaxerror" in lower:
                    issues.append(f"SYNTAX_ERROR: {os.path.basename(lf)} で文法エラーが検知されました。")
        except Exception:
            pass

    return issues, log_content

def check_remote_endpoint(url: str, timeout: float = 5.0) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "schedule-kaggle-monitor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.status == 200
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="Kaggle Batch Execution & Log Check Scheduler")
    parser.add_argument("--kaggle-dir", "-k", required=True, help="Directory containing kernel-metadata.json")
    parser.add_argument("--output-dir", "-o", default="/tmp/kaggle_monitor_out", help="Directory to save downloaded logs")
    parser.add_argument("--interval", "-i", type=int, default=30, help="Polling interval in seconds")
    parser.add_argument("--max-checks", "-m", type=int, default=60, help="Maximum number of polling checks")
    parser.add_argument("--health-url", "-u", default=None, help="Cloudflare Tunnel or remote health endpoint URL")

    args = parser.parse_args()

    kernel_id = get_kernel_id(args.kaggle_dir)
    print(f"🚀 [SCHEDULER] Kaggle カーネル '{kernel_id}' の定期監視を開始します (間隔: {args.interval}s, 最大: {args.max_checks}回)...")

    for cycle in range(1, args.max_checks + 1):
        print(f"\n--- [Check {cycle}/{args.max_checks}] ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---")
        status_line = check_status(kernel_id)
        print(f"Kernel Status: {status_line}")

        # Cloudflare Tunnel / REST エンドポイント疎通確認
        if args.health_url:
            if check_remote_endpoint(args.health_url):
                print(f"✅ Remote Health Endpoint 疎通成功: {args.health_url}")

        if "has status \"error\"" in status_line.lower() or "error" in status_line.lower():
            print("\n🚨 [KAGGLE ERROR] カーネルが異常終了しました。ログをダウンロードして解析します...")
            download_output(kernel_id, args.output_dir)
            issues, logs = parse_kaggle_logs(args.output_dir)
            print("\n--- Diagnostic Summary ---")
            for iss in issues:
                print(f"  • {iss}")
            print("\n--- Downloaded Logs Snippet ---")
            print(logs)
            sys.exit(2)

        if "has status \"complete\"" in status_line.lower() or "complete" in status_line.lower():
            print("\n🎉 [KAGGLE COMPLETE] カーネル実行が正常完了しました。最新ログを保存します。")
            download_output(kernel_id, args.output_dir)
            sys.exit(0)

        time.sleep(args.interval)

    print("\n⏰ 監視上限回数に達しました。")
    sys.exit(1)

if __name__ == "__main__":
    main()
