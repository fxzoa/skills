# References: TRIGGERS.md

## Positive Triggers (Activate this skill)
- "開発環境を初期セットアップして"
- "新しいLinux/WSLマシンにCLIツール（gcloud, wrangler, colab, kaggle等）を入れて"
- "開発者用CLI環境を一括再構築したい"
- "dev environment setup run"
- "Setup my workstation tools: uv, nvm, gcloud, wrangler"

## Negative Triggers (Do NOT activate this skill)
- "Docker のみインストールしたい" -> `kiri-docker-setup` を使用
- "単一のColabノートブックを実行したい" -> `colab-operator` を使用
- "Kaggleノートブックをプッシュしたい" -> `kaggle-operator` を使用
- "Cloudflare Workerのソースコードをデプロイしたい" -> `chat-worker-service-register` 等を使用
