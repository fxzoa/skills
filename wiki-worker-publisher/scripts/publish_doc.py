#!/usr/bin/env python3
"""
publish_doc.py: Standalone HTML ドキュメントを wiki-worker へ安全に追加・登録・デプロイ・検証するスクリプト

責務:
1. 対象HTMLファイルの存在確認と検証
2. pages/<category>/ への配置
3. scripts/build-wiki.mjs への DOC_OVERRIDES メタデータ自動登録（重複防止）
4. wiki-worker のカタログビルド (npm run build)
5. Cloudflare Workers への本番デプロイ (npm run deploy)
6. 公開URLへの HTTP GET / HEAD ヘルスチェック
※ 注意: 中間ファイルや一時スクリプトは一切削除せず、すべて保持する。
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

DEFAULT_WIKI_ROOT = "/mnt/d/cf-workers/wiki-worker"
VALID_CATEGORIES = ["ai-agents", "llm-infra", "trading-bots", "macro-finance"]

def log(msg):
    print(f"[{os.path.basename(__file__)}] {msg}", flush=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Publish HTML doc to wiki-worker")
    parser.add_argument("--html", required=True, help="絶対パスまたは相対パスの対象HTMLファイル")
    parser.add_argument("--category", choices=VALID_CATEGORIES, default="llm-infra", help=f"配置カテゴリ ({', '.join(VALID_CATEGORIES)})")
    parser.add_argument("--title", help="カタログ表示用タイトル（省略時はHTML内タイトルまたはファイル名）")
    parser.add_argument("--tags", help="カンマ区切りのタグリスト (例: 'GCP,Cloud Billing,IAM')")
    parser.add_argument("--featured", action="store_true", help="注目記事フラグ (true/false)")
    parser.add_argument("--skip-deploy", action="store_true", help="デプロイをスキップしてローカル配置とビルドのみ行う")
    parser.add_argument("--wiki-root", default=DEFAULT_WIKI_ROOT, help="wiki-worker プロジェクトルート")
    return parser.parse_args()

def main():
    args = parse_args()
    html_src = os.path.abspath(args.html)
    wiki_root = os.path.abspath(args.wiki_root)

    if not os.path.isfile(html_src):
        log(f"エラー: 指定されたHTMLファイルが見つかりません: {html_src}")
        sys.exit(1)

    if not os.path.isdir(wiki_root):
        log(f"エラー: wiki-worker のルートが見つかりません: {wiki_root}")
        sys.exit(1)

    filename = os.path.basename(html_src)
    dest_dir = os.path.join(wiki_root, "pages", args.category)
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, filename)

    log(f"1. HTMLファイルをコピー中: {html_src} -> {dest_file}")
    with open(html_src, "r", encoding="utf-8") as f:
        content = f.read()
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. メタデータの抽出と build-wiki.mjs への反映
    build_script = os.path.join(wiki_root, "scripts", "build-wiki.mjs")
    if os.path.isfile(build_script):
        log(f"2. DOC_OVERRIDES メタデータの更新チェック: {build_script}")
        with open(build_script, "r", encoding="utf-8") as f:
            script_text = f.read()

        if filename in script_text:
            log(f"   既に {filename} のエントリーが存在するため、上書きをスキップします。")
        else:
            title = args.title
            if not title:
                m = re.search(r"<title[^>]*>([\s\S]*?)</title>", content, re.IGNORECASE)
                title = m.group(1).strip() if m else filename.replace(".html", "")

            tag_list = [t.strip() for t in args.tags.split(",")] if args.tags else [args.category]
            entry_snippet = f"""  '{filename}': {{
    title: {json.dumps(title, ensure_ascii=False)},
    tags: {json.dumps(tag_list, ensure_ascii=False)},
    originalPath: {json.dumps(html_src, ensure_ascii=False)},
    featured: {"true" if args.featured else "false"},
  }},
"""
            target = "const DOC_OVERRIDES = {"
            if target in script_text:
                script_text = script_text.replace(target, target + "\n" + entry_snippet)
                with open(build_script, "w", encoding="utf-8") as f:
                    f.write(script_text)
                log(f"   DOC_OVERRIDES に {filename} を正常に追加しました。")

    # 3. カタログビルド
    log(f"3. カタログビルドを実行中 (npm run build)...")
    res_build = subprocess.run(["npm", "run", "build"], cwd=wiki_root, capture_output=True, text=True)
    if res_build.returncode != 0:
        log(f"ビルド失敗:\n{res_build.stderr}\n{res_build.stdout}")
        sys.exit(res_build.returncode)
    log("   カタログビルド完了。")

    # 4. デプロイ
    if not args.skip_deploy:
        log(f"4. Cloudflare Workers 本番デプロイを実行中 (npm run deploy)...")
        res_deploy = subprocess.run(["npm", "run", "deploy"], cwd=wiki_root, capture_output=True, text=True)
        if res_deploy.returncode != 0:
            log(f"デプロイ失敗:\n{res_deploy.stderr}\n{res_deploy.stdout}")
            sys.exit(res_deploy.returncode)
        log("   本番デプロイ完了。")

        # 5. 公開検証
        live_url = f"https://wiki.btczoa.app/raw/{args.category}/{filename}"
        log(f"5. 公開URLの死活監視を実行中: {live_url}")
        try:
            req = urllib.request.Request(live_url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.getcode()
                log(f"   検証成功! HTTP ステータス: {status}")
        except Exception as e:
            log(f"   警告: 死活監視でレスポンス確認中に例外が発生しました: {e}")

        print("\n" + "="*60)
        print(f"🎉 公開完了: {live_url}")
        print(f"ポータル: https://wiki.btczoa.app/")
        print("="*60 + "\n")
    else:
        log("デプロイスキップオプションが指定されたため、デプロイを行わずに終了します。")

if __name__ == "__main__":
    main()
