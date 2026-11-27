# Triggers & Smoke Tests (`gcp-free-tier-mesh`)

## Positive Triggers (Should Activate)
- "5つの GCP プロジェクトの Free Tier VM を VPC ピアリングで接続して分散デプロイしたい"
- "別アカウントの GCP プロジェクト間で通信の Egress 課金をゼロにする Terraform 構成を作って"
- "e2-micro 複数台にコンテナを 3 個ずつ分散配置して一斉検証して"
- "請求先アカウントがないプロジェクトに別アカウントの Billing Account をリンクして構築して"

## Negative Triggers (Should NOT Activate)
- "この 1 台の VM に docker-compose.yml をデプロイして" -> Use `vm-docker-deploy`
- "Cloud Run に WebUI をデプロイして" -> Use `cloudrun-deploy-skill`
- "Kaggle ノートブックを推論サーバーとして起動して" -> Use `kaggle-notebook`

## Smoke Test Command
```bash
python3 scripts/link_billing.py --help
python3 scripts/apply_tf_tokens.py --help
python3 scripts/package_images.py --help
python3 scripts/deploy_mesh.py --help
python3 scripts/verify_mesh.py --help
python3 scripts/sync_env_secret.py --help
```
