---
name: chat-worker-service-register
description: Registers Colab or Kaggle deployed AI services into chat-worker (domains.ts and secrets.ts), runs typecheck/tests, deploys via wrangler, and verifies upstream/worker endpoints. Use when registering a newly deployed notebook AI service into chat-worker or fixing 401/model preset mismatches. Do NOT use for deploying Colab/Kaggle notebooks themselves or building unrelated Cloudflare Workers.
---

# chat-worker-service-register

Register newly deployed Colab/Kaggle AI services from `/mnt/d/notebook/*` into `/mnt/d/cf-workers/chat-worker` (`chat.btczoa.app`) using deterministic Python scripts in `scripts/`.

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control

> [!IMPORTANT]
> **Probabilistic Prompt-driven Orchestration is strictly prohibited for procedural workflows.**
> All registration, testing, deployment, and endpoint checks must be executed via `scripts/*.py` rather than ad-hoc manual edits or shell synthesis.
> `SKILL.md` serves as a concise navigation index (<500 lines); detailed specifications live in `references/`.

---

## Document Index & Criteria

| Document | Role | When to read |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 流用可能資産と案件ごとの差し替え境界定義 | 新規 AI サービス（Colab / Kaggle）を登録・流用する時 |
| **[references/TOOLS.md](references/TOOLS.md)** | 4大分類（Command / Shell / MCP / 外部 API）の仕様・引数・終了コード | `scripts/*.py` の CLI オプションや終了コードを確認する時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | Mermaid 論理/物理図・登録シーケンス・認証フロー | `chat-worker` と Cloudflare Tunnel の通信・認証経路を確認する時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | 事前確認・登録・デプロイ・疎通検証の合格基準 | 作業完了の合否判定を行う時 |
| **[references/GUIDE.md](references/GUIDE.md)** | ステップバイステップの登録・デプロイ手順 | 実際の登録コマンドを実行する時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | Node.js / Wrangler 認証 / Notebook `.env` 前提条件 | 実行環境の前提・権限を確認する時 |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | 発動プロンプト例（Positive / Negative）とスモークテスト | トリガー精度を確認する時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | 401 / 530 / Wrangler OAuth 等のエラー原因と解決策 | エラー発生時に切り分け・修復する時 |

---

## Pre-Built Operations (`scripts/`)

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `register_chat_service` | `python3 scripts/register_chat_service.py --env <notebook_env> --id <preset_id>` | `.env` から `domains.ts` と `secrets.ts` を冪等更新し、続けて `typecheck` / `test` / `wrangler deploy` / 疎通確認まで同時実行（`--no-deploy` で抑止可） | [TOOLS.md](references/TOOLS.md) |
| `verify_and_deploy_chat_worker` | `python3 scripts/verify_and_deploy_chat_worker.py --deploy --upstream-url <url> --api-key <key>` | `typecheck` / `test` / `wrangler deploy` / 疎通確認を単独実行 | [TOOLS.md](references/TOOLS.md) |

---

## Workflow Calls
1. `register_chat_service(--env <notebook_dir>/.env, --id <service_id>)` → `domains.ts` & `secrets.ts` 更新 ＋ 自動テスト・`wrangler deploy`・疎通確認を同時実行 (参照: [GUIDE.md](references/GUIDE.md))

---

## Trigger & Exit Criteria
- **Trigger**: `/mnt/d/notebook` 配下の Colab / Kaggle AI サービスをデプロイした後に `chat-worker` へ登録・更新する時、または `401` / モデル不一致を解消する時。
- **Exit Criteria**: `register_chat_service.py` および `verify_and_deploy_chat_worker.py --deploy` が exit `0` で完了し、`https://chat.btczoa.app/health` および対象サービスの `/health`・`/v1/models` が HTTP 200 を返すこと。

---

## Anti-Patterns
- **Never edit `domains.ts` without `secrets.ts`**: クライアントプリセットだけ更新すると、外部クライアント経由の API 呼び出しで `401 Unauthorized` が発生する。
- **Never deploy without `typecheck` & `test`**: `npm run typecheck && npm test` を通さずに `wrangler deploy` を実行しない。
- **Never hardcode different `LLM_API_KEY` values**: Notebook 側の `.env` (`LLM_API_KEY`) と `chat-worker` 側の設定を必ず一致させる。
