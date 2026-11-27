# TRIGGERS.md

## Positive Triggers (発動条件)
* 「Kiri をインストールしてコンテナ環境をセットアップして」
* 「Docker CLI と Docker Compose、Buildx を Kiri に関連づけて」
* 「新しいマシンを立ち上げたので、Dockerエンジン（Kiri）とスキル群を初期設定して」
* 「Kiri デーモンを systemd で自動起動（常駐化）したい」
* 「/mnt/d/skills のスキルを Antigravity に一括登録して」

## Negative Triggers (非発動条件)
* 「Docker Desktop を Windows にインストールして」（本スキルは軽量 Rust 製 Kiri 対象）
* 「Cloud Run や GCE VM に Docker コンテナをデプロイして」（`cloudrun-deploy-skill` または `vm-docker-deploy` を使用）
* 「新しいスキルを作成したい」（`create-new-skill` を使用）
