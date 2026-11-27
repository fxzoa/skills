# Triggers & Smoke Testing

## Positive Triggers
- "gcloud config default をコピーして、新しいアカウントの configurations を作成して"
- "gcloud の configuration を一覧作成して、.env と同期してほしい"
- "GCPのアカウントを切り替える設定を作成して"
- "gcloud configurations を自動設定して"

## Negative Triggers
- "GCPのAlways Free VMを作成して" -> Use `gcp-free-tier-mesh`
- "Cloud Run にコンテナをデプロイして" -> Use `cloudrun-deploy`
- "gcloud CLI をインストールして" -> Use `dev-environment-setup`

## Smoke Test
```bash
python3 scripts/manage_gcloud_configs.py list
```
Expected output: Table of configurations with exit code 0.
