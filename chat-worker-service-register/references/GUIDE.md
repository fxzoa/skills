# Step-by-Step Guide (`chat-worker-service-register`)

## Step 1: 登録内容のドライラン確認
Notebook の `.env` を指定し、`--dry-run` で更新内容を確認します：

```bash
python3 scripts/register_chat_service.py \
  --env /mnt/d/notebook/02_maya_gpu_cpu/kaggle/.env \
  --id code-ai \
  --dry-run
```

## Step 2: `chat-worker` へのサービス登録＋自動デプロイ・疎通確認
問題なければ `--dry-run` を外して実行します。`domains.ts` と `secrets.ts` の更新後、自動的に `verify_and_deploy_chat_worker.py --deploy` が呼び出され、`npm run typecheck` / `npm test` / `wrangler deploy` / 疎通確認まで一括完了します（`BypassSandbox: true` で実行）：

```bash
python3 scripts/register_chat_service.py \
  --env /mnt/d/notebook/02_maya_gpu_cpu/kaggle/.env \
  --id code-ai
```

> [!NOTE]
> 登録のみ行いデプロイを保留したい場合は `--no-deploy` を付与し、後から Step 3 を単独実行してください。

## Step 3: （任意）検証・デプロイのみ再実行する場合
`verify_and_deploy_chat_worker.py` を `--deploy` 付きで実行します（`wrangler deploy` と外部 HTTP 疎通を行うため、`BypassSandbox: true` で実行）：

```bash
python3 scripts/verify_and_deploy_chat_worker.py \
  --deploy \
  --upstream-url https://code-ai.btczoa.app \
  --api-key code-ai-api-key
```
