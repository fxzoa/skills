# TOOLS.md — wiki-worker-publisher

## 1. Command 仕様

### `publish_doc.py`
Standalone HTML ドキュメントを wiki-worker へ配置・メタデータ登録・ビルド・デプロイ・URL検証までを自動実行する。

#### 引数仕様
- `--html <path>` (必須): 公開するHTMLファイルのローカルパス
- `--category <category>` (任意、既定: `llm-infra`):
  - `llm-infra`
  - `ai-agents`
  - `trading-bots`
  - `macro-finance`
- `--title <title>` (任意): カタログ表示用のタイトル（未指定時は `<title>` タグから自動抽出）
- `--tags <tags>` (任意): カンマ区切りの検索タグ（例: `GCP,IAM,Billing`）
- `--featured` (フラグ): 注目記事としてトップにピン留め
- `--skip-deploy` (フラグ): 本番デプロイを行わず、ローカル配置とビルドのみ検証
- `--wiki-root <dir>` (任意、既定: `/mnt/d/cf-workers/wiki-worker`)

## 2. Shell コマンド
- `npm run build`: カタログJSON（`dist/catalog.json`）およびポータルHTML（`dist/index.html`）を生成。
- `npm run deploy`: `node scripts/build-wiki.mjs && wrangler deploy --env=""` を実行。

## 3. MCP / 外部 API
- **Cloudflare API (Wrangler OAuth)**: `~/.config/.wrangler/config/default.toml` の OAuth トークンを使用して Workers へのアセット・スクリプトアップロードを実行。
- **公開URL HTTP HEAD Check**: デプロイ完了後、`https://wiki.btczoa.app/raw/<category>/<file>` に対して 200 OK を検証。
