# Prototype & Reusability Boundaries (`chat-worker-service-register`)

## 1. 流用可能資産 (Reusable Core)
以下はすべての `/mnt/d/notebook/*` AI サービス（Colab / Kaggle）で共通利用できます：
- `scripts/register_chat_service.py`: `.env`（`TUNNEL_HOSTNAME`, `TUNNEL_PORT`, `LLM_API_KEY`, モデル変数）を読み取り、`ENDPOINT_PRESETS` と `getEffectiveApiKeyForDomain` を冪等に更新するロジック。
- `scripts/verify_and_deploy_chat_worker.py`: `npm run typecheck`, `npm test`, `npm run deploy`, および `/health`・`/v1/models` 疎通検証のパイプライン。
- `chat-worker` 側のプロキシ基盤（`src/index.ts`, `src/server/secrets.ts` の Secrets Store / フォールバック機構）。

## 2. 案件固有の差し替え境界 (Project-Specific Parameters)
新規 AI サービスごとに差し替えるパラメータは以下の通りです：

| 項目 | 参照元 (Notebook `.env`) | 反映先 (`chat-worker`) |
|:---|:---|:---|
| プリセット ID (`--id`) | サービス識別子（例: `code-ai`, `qwen3-6-40b-kaggle`） | `domains.ts` (`id`) |
| 公開 URL (`--hostname`) | `TUNNEL_HOSTNAME`（例: `code-ai.btczoa.app`） | `domains.ts` (`url`) & `secrets.ts` (`domain.includes(...)`) |
| ポート (`--port`) | `TUNNEL_PORT`（例: `8007`） | `domains.ts` (`port`) |
| API キー (`--api-key`) | `LLM_API_KEY`（例: `code-ai-api-key`） | `domains.ts` (`apiKey`) & `secrets.ts` (フォールバック値) |
| モデル ID (`--model`) | `MAYA_MODEL` / `MODEL_NAME` 等 | `domains.ts` (`models`, `defaultModel`) |
