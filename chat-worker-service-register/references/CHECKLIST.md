# Acceptance Checklist (`chat-worker-service-register`)

- [ ] Notebook 側（Colab / Kaggle）が稼働しており、`https://<TUNNEL_HOSTNAME>/health` が `200 OK` を返す。
- [ ] `https://<TUNNEL_HOSTNAME>/v1/models` が `.env` の `LLM_API_KEY` で `200 OK` を返す（`401` にならない）。
- [ ] `scripts/register_chat_service.py` により `src/client/domains.ts` にプリセット（`id`, `url`, `port`, `apiKey`, `models`, `defaultModel`）が登録・更新されている。
- [ ] `src/server/secrets.ts` の `getEffectiveApiKeyForDomain` に該当ドメインのキー解決ルールが登録されている。
- [ ] `npm run typecheck` および `npm test` がすべてパスする（exit `0`）。
- [ ] `npm run deploy`（`wrangler deploy`）で `chat.btczoa.app` へデプロイが完了し、`GET https://chat.btczoa.app/health` が `200 OK` を返す。
