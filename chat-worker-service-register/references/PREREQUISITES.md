# Prerequisites (`chat-worker-service-register`)

## 1. ローカル環境要件
- **Node.js / npm**: `chat-worker` の `typecheck` / `test` / `wrangler` 実行に必須。
- **Python 3.10+**: `scripts/*.py` の実行に必須。
- **Wrangler CLI 認証済み**: `wrangler whoami` が通り、`chat.btczoa.app` Worker へのデプロイ権限があること（サンドボックス外で `~/.config/.wrangler` を参照）。

## 2. 対象リポジトリ・ファイル要件
- `/mnt/d/cf-workers/chat-worker` に `src/client/domains.ts` および `src/server/secrets.ts` が存在すること。
- 登録対象の Notebook ディレクトリ（例: `/mnt/d/notebook/<project>/kaggle/.env` または `colab/.env`）に以下が定義されていること：
  - `TUNNEL_HOSTNAME`
  - `TUNNEL_PORT`
  - `LLM_API_KEY`
  - モデル名（`MAYA_MODEL`, `MODEL_NAME`, `DEFAULT_MODEL` 等）
