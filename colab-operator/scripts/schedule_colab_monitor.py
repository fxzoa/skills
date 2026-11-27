#!/usr/bin/env python3
"""
schedule_colab_monitor.py
Colab セッションのステータスおよび各種ログ・ヘルスエンドポイントを定期監視し、
問題（OOM、プロセス異常終了、接続エラー等）を検知した際に自律自己改善ループ用の
診断サマリと詳細ログを出力するスクリプトラッパー。
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from typing import Dict, Any, Optional

def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def check_colab_status(session: str) -> dict[str, Any]:
    rc, out, err = run_cmd(["colab", "--auth", "adc", "status", "-s", session])
    status_line = out.strip() if out.strip() else err.strip()
    return {
        "status_code": rc,
        "raw": status_line,
        "is_idle": "Status: IDLE" in status_line,
        "is_running": "Status: BUSY" in status_line or "RUNNING" in status_line
    }

def fetch_recent_logs(session: str, lines: int = 40) -> str:
    script = f"""
import os
def show(f):
    if os.path.exists(f):
        print(f'=== {{f}} (tail) ===')
        try:
            with open(f, errors='ignore') as fp:
                print(''.join(fp.readlines()[-{lines}:]))
        except Exception as e:
            print(f'Error reading {{f}}: {{e}}')
show('logs/server.log')
show('logs/uvicorn.log')
show('logs/llama_server.log')
show('logs/tunnel.log')
"""
    rc, out, err = run_cmd(["colab", "--auth", "adc", "exec", "-s", session, "-c", script])
    if rc != 0:
        # Fallback to stdin execution if -c is not supported
        p = subprocess.Popen(["colab", "--auth", "adc", "exec", "-s", session], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate(input=script)
    return out

def check_healthz(endpoint_url: str, timeout: float = 5.0) -> dict[str, Any]:
    try:
        req = urllib.request.Request(endpoint_url, headers={"User-Agent": "schedule-colab-monitor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            body = res.read().decode("utf-8", errors="ignore")
            try:
                data = json.loads(body)
            except Exception:
                data = body
            return {"healthy": True, "code": res.status, "data": data}
    except Exception as e:
        return {"healthy": False, "error": str(e)}

def parse_diagnostics(log_text: str) -> list[str]:
    issues = []
    lower = log_text.lower()
    if "out of memory" in lower or "oom-kill" in lower or "code -9" in lower:
        issues.append("OOM_KILLED: システムメモリまたはGPU VRAM不足によりプロセスが強制終了されました。")
    if "address already in use" in lower or "errno 98" in lower:
        issues.append("PORT_CONFLICT: 指定ポートが既存プロセスにより占有されています。")
    if "modulenotfounderror" in lower or "no module named" in lower:
        issues.append("MISSING_MODULE: 仮想環境または依存ライブラリの不足が検知されました。")
    if "syntaxerror" in lower:
        issues.append("SYNTAX_ERROR: 生成コードに文法エラーが存在します。")
    if "no such file or directory" in lower:
        issues.append("FILE_NOT_FOUND: 必須ファイルまたはモデルパスが見つかりません。")
    return issues

def main():
    parser = argparse.ArgumentParser(description="Colab Status & Log Check Scheduler")
    parser.add_argument("--session", "-s", required=True, help="Colab session name")
    parser.add_argument("--interval", "-i", type=int, default=15, help="Polling interval in seconds")
    parser.add_argument("--max-checks", "-m", type=int, default=40, help="Maximum number of checks")
    parser.add_argument("--health-url", "-u", default=None, help="Optional healthz endpoint URL to test")
    parser.add_argument("--auto-dump-on-error", action="store_true", default=True, help="Automatically dump logs on error")

    args = parser.parse_args()

    print(f"🚀 [SCHEDULER] Colab セッション '{args.session}' の定期監視を開始します (間隔: {args.interval}s, 最大: {args.max_checks}回)...")

    for cycle in range(1, args.max_checks + 1):
        print(f"\n--- [Check {cycle}/{args.max_checks}] ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---")
        status = check_colab_status(args.session)
        print(f"Session Status: {status['raw']}")

        if status["status_code"] != 0:
            print("⚠️ セッション状態の取得に失敗しました。セッションが存在しないかADC認証切れの可能性があります。")

        # ヘルスチェックエンドポイントの確認
        if args.health_url:
            health = check_healthz(args.health_url)
            if health["healthy"]:
                print(f"✅ Health Endpoint OK: {health['data']}")
                status_val = health.get("data", {}).get("status") or health.get("data", {}).get("data", {}).get("model_status")
                if status_val == "ready":
                    print("🎉 モデルバックエンドが正常に ready となりました。監視ループを完了します。")
                    sys.exit(0)
            else:
                print(f"⏳ Health Endpoint Wait: {health['error']}")

        # ログ取得と自己改善用エラー判定
        logs = fetch_recent_logs(args.session)
        issues = parse_diagnostics(logs)

        if issues:
            print("\n🚨 [DIAGNOSTIC] 問題が検出されました。自己改善ループをトリガーしてください:")
            for issue in issues:
                print(f"  • {issue}")
            print("\n--- Recent Logs Snapshot ---")
            print(logs)
            sys.exit(2)

        time.sleep(args.interval)

    print("\n⏰ 監視上限回数に達しました。")
    sys.exit(1)

if __name__ == "__main__":
    main()
