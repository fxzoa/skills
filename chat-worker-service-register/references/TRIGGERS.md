# Triggers & Smoke Tests (`chat-worker-service-register`)

## Positive Triggers (発動すべき要求)
1. `/mnt/d/notebook` に新しい AI サービスを Colab/Kaggle へデプロイしたので、`chat-worker` に登録したい。
2. `chat-worker` 側の AI サービス登録情報（API キーやモデル名）を最新の `.env` に合わせて更新してデプロイして。
3. `chat.btczoa.app` からバックエンド AI サービスを呼ぶと `401 Unauthorized` が出るので、`domains.ts` と `secrets.ts` を修正して。

## Negative Triggers (発動しない要求)
1. `/mnt/d/notebook/.../kaggle/t4x2_maya_kaggle.ipynb` を Kaggle に PUSH して（→ `kaggle-operator` を使用）。
2. Google Colab のセッションを起動してノートブックを実行して（→ `colab-operator` を使用）。
3. `chat-worker` とは無関係な新規 Cloudflare Worker をゼロから構築して（→ `fullstack-dev` 等を使用）。

## Smoke Test
```bash
python3 /home/ppbb/.gemini/antigravity-cli/skills/create-new-skill/scripts/validate_skill.py \
  /home/ppbb/.gemini/antigravity-cli/skills/chat-worker-service-register
```
