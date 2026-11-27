# Tools & Interfaces Reference (`chat-worker-service-register`)

本スキルで使用するツールは以下の4分類に整理されています。

---

## 1. Command ツール (Python CLI / `scripts/`)

| Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `register_chat_service.py` | Notebook `.env` または引数から `domains.ts` / `secrets.ts` を冪等更新し、続けてテスト・デプロイ・疎通確認まで同時実行 | `python3 scripts/register_chat_service.py --env <path> --id <id> [--no-deploy] [--dry-run]` | `0`: 成功, `1`: 引数/ファイル/デプロイエラー |
| `verify_and_deploy_chat_worker.py` | `typecheck` / `test` / `wrangler deploy` / 疎通検証を実行 | `python3 scripts/verify_and_deploy_chat_worker.py [--deploy] [--upstream-url <url>] [--api-key <key>]` | `0`: 成功, `1`: 検証または疎通失敗 |

---

## 2. Shell コマンド (OS & Infrastructure)

| Command | Purpose | Example |
|:---|:---|:---|
| `npm run typecheck` | TypeScript 型検査 | `cd /mnt/d/cf-workers/chat-worker && npm run typecheck` |
| `npm test` | Node 組み込みテストランナー実行 | `cd /mnt/d/cf-workers/chat-worker && npm test` |
| `npm run deploy` | Cloudflare Workers へ本番デプロイ | `cd /mnt/d/cf-workers/chat-worker && npm run deploy` |

---

## 3. MCP ツール (Agent Primitives)

| Primitive | Role | Usage |
|:---|:---|:---|
| `run_command` | `scripts/*.py` の実行（`wrangler deploy` や外部疎通は `BypassSandbox: true`） | 登録・テスト・デプロイ・疎通確認 |
| `read_file` | Notebook `.env` や `domains.ts` / `secrets.ts` の事前確認 | 差分や既存プリセットの確認 |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Endpoint | Purpose |
|:---|:---|:---|
| `Cloudflare Workers API` | `wrangler deploy` 経由 | `chat.btczoa.app` Worker のデプロイ |
| `chat-worker Health API` | `GET https://chat.btczoa.app/health` | デプロイ後の Worker 稼働確認 |
| `Upstream AI Service API` | `GET https://<TUNNEL_HOSTNAME>/health`, `/v1/models` | Cloudflare Tunnel 経由の推論サーバー疎通・Bearer 認証確認 |
