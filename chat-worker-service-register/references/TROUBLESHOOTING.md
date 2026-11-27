# Troubleshooting (`chat-worker-service-register`)

| 症状 | 根本原因 | 解決策 |
|:---|:---|:---|
| `401 Unauthorized` (バックエンド呼び出し時) | `domains.ts` の `apiKey` または `secrets.ts` の `getEffectiveApiKeyForDomain` に `LLM_API_KEY` が未設定／不一致 | Notebook の `.env` の `LLM_API_KEY` を確認し、`register_chat_service.py` を再実行して `wrangler deploy` する |
| `HTTP 530 (error code: 1033)` | Colab / Kaggle 側の Cloudflare Named Tunnel が未起動または停止済み | バックエンド Notebook が稼働中か確認し、トンネル起動後に `verify_and_deploy_chat_worker.py` を再実行する |
| `wrangler deploy` が OAuth URL を開こうとする | サンドボックス内で `~/.config/.wrangler` にアクセスできない | `BypassSandbox: true` で `verify_and_deploy_chat_worker.py --deploy` を実行する |
| `ENDPOINT_PRESETS` に対象モデルが出ない | `domains.ts` の `models` / `defaultModel` 未設定 | `--model <MODEL_ID>` を指定して `register_chat_service.py` を再実行する |
