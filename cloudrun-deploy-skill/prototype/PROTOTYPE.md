# PROTOTYPE.md: プロトタイプ資産仕様書・流用/入替境界ガイド

本ドキュメントは、`prototype/` に収録されている実稼働リファレンス資産（`coin-trade-kaggle` 実装例）の構成を解説し、**「他のプロジェクトでもそのまま流用できる汎用設計」** と **「スキル適用時にプロジェクト固有要件として差し替えるべき境界」** を明確に定義・分離したものです。

---

## 1. プロトタイプ収録資産の全体構造

```text
prototype/
├── docker/
│   └── Dockerfile.cloudrun             # Deno + OpenSSH 統合コンテナビルド定義
└── deploy/
    └── cloudrun/
        ├── entrypoint.sh               # 複数WebUI・常駐ボット・SSHトンネル統括起動スクリプト
        ├── service.yaml                # Knative 形式 Cloud Run サービス定義
        ├── cloudbuild.yaml             # Google Cloud Build CI/CD パイプライン定義
        ├── deploy.sh                   # Artifact Registry作成〜デプロイ自動化シェル
        ├── .env.cloudrun.example       # サブシステム有効化トグル付き環境変数見本
        └── cloudrun_deployment_spec.html # Rule.11/14準拠 二重視点HTMLアーキテクチャ仕様書
```

---

## 2. 流用できる部分（汎用コア設計） vs 差し替える部分（個別要件）

他プロジェクト（例: Python FastAPI, Node.js/Next.js, Go microservice, 各種監視ツール等）へ展開する際は、以下の境界線に従って作業を行います。

| 構成要素 | 他プロジェクトでもそのまま「流用」できる部分（汎用資産） | プロジェクトごとに「差し替える」部分（固有要件） |
|:---|:---|:---|
| **Knative マニフェスト<br>(`service.yaml`)** | ・`run.googleapis.com/execution-environment: gen2`（第2世代実行環境）<br>・`run.googleapis.com/cpu-throttling: "false"`（常駐処理・WebSocket切断防止のためのCPU常時割り当て）<br>・`autoscaling.knative.dev/minScale: 1`（常時稼働）<br>・リソース制限枠（`cpu: 2000m`, `memory: 2Gi`）の構造<br>・`startupProbe` / `livenessProbe` の監視パターン | ・`metadata.name`（サービス名）<br>・`image` のリポジトリパス<br>・`autoscaling.knative.dev/maxScale`（※Webアプリ単体なら自動スケール `>1` を許容。二重実行がNGなBot・ワーカーは `1` 固定）<br>・ポート番号・環境変数リスト（`env`） |
| **CI/CD パイプライン<br>(`cloudbuild.yaml`)** | ・`gcr.io/cloud-builders/docker` によるビルド＆プッシュの流れ<br>・`gcr.io/google.com/cloudsdktool/cloud-sdk` による `gcloud run deploy` 実行ステップ<br>・Artifact Registry へのタグ付け（`:latest` またはコミットハッシュ） | ・`_SERVICE_NAME`, `_REPO_NAME` 等の置換パラメータ（`substitutions`）<br>・`Dockerfile` の配置パス（`-f` 引数）<br>・公開設定（`--allow-unauthenticated` の有無） |
| **デプロイ自動化シェル<br>(`deploy.sh`)** | ・`gcloud config get-value project` による環境変数の安全な自動解決ロジック<br>・Artifact Registry リポジトリが未存在の場合に自動 `create` する自己修復処理<br>・Docker 認証（`gcloud auth configure-docker`）フロー | ・デフォルトのサービス名、リポジトリ名、リージョン定数 |
| **マルチプロセス起動制御<br>(`entrypoint.sh`)** | ・フォアグラウンドでメインHTTPゲートウェイ（`PORT` リッスン）を実行する構造<br>・バックグラウンドプロセス（`&`）のログを `/tmp/*.log` へ退避するパターン<br>・SSHトンネル（秘密鍵の展開と `ssh -L` バックグラウンド待受）の自動化ロジック | ・実際に起動するサブサービス群（Node/Python/Denoなどの起動コマンド）<br>・公開ポート番号（`8080` 以外の指定）<br>・起動トグル用環境変数名（`ENABLE_*`） |
| **コンテナ定義<br>(`Dockerfile.cloudrun`)** | ・マルチプロセス統合コンテナに必要な軽量パッケージ（`openssh-client`, `netcat-openbsd`）の同梱手法<br>・Cloud Run の仕様に準じた環境変数（`PORT`, `HOST`）の宣言と `ENTRYPOINT` によるラッパー実行設計 | ・ベースイメージ（Python, Node, Go, Rust等への変更）<br>・ランタイム固有の依存インストール（`npm install`, `pip install`, `uv sync` 等） |
| **技術仕様書<br>(`cloudrun_deployment_spec.html`)** | ・Rule.11（完全自己完結・ライトモード・CDN不要）のデザインテンプレート<br>・Rule.14（論理データフロー＆物理インフラトポロジーの対になる二重視点SVG図解）の骨格 | ・図解内のコンポーネント名（DEX, 外部サービス, 内部ポート名等）<br>・プロジェクト固有の説明文・APIエンドポイント表 |

---

## 3. 他プロジェクト適用時の「差し替え」チェックリスト

他のプロジェクトに本スキルを適用する際は、以下の3ステップで固有部分のみを差し替えます。

### Step 1: 単一サービスか、複数統合（All-in-One）かの判定
- **単一Webサービスの場合:**
  - `entrypoint.sh` は不要。コンテナの `CMD` で直接Webサーバー（例: `uvicorn main:app --port $PORT --host 0.0.0.0`）を起動。
  - `service.yaml` の `cpu-throttling` を `"true"`（リクエスト時のみCPU割り当て）に変更してコスト削減。
- **常駐Botや複数WebUIをまとめる場合:**
  - 本プロトタイプの `entrypoint.sh` を流用し、起動コマンド行のみをプロジェクトのスクリプトに置換。
  - `cpu-throttling: "false"` と `maxScale: 1` を維持。

### Step 2: テンプレートからの生成（`templates/` の利用）
1. `templates/deploy/cloudrun/service.yaml.tmpl` を読み込み、`{{SERVICE_NAME}}`, `{{PORT}}`, `{{HEALTH_PATH}}` などをプロジェクト固有値で置換。
2. `templates/deploy/cloudrun/cloudbuild.yaml.tmpl` の置換パラメータを更新。

### Step 3: スキルツールの実行
プロジェクトルートにて `cloudrun-deploy-skill` のツールを実行するだけで、インフラ準備からデプロイまで完結します：
```bash
# 1. 構成確認
python3 /mnt/d/skills/cloudrun-deploy-skill/scripts/inspect_gcloud_config.py -c <YOUR_CONFIG>

# 2. API & Artifact Registry の自動プロビジョニング
python3 /mnt/d/skills/cloudrun-deploy-skill/scripts/provision_apis_and_repo.py -c <YOUR_CONFIG> --repo <YOUR_REPO>

# 3. ビルド＆デプロイ
python3 /mnt/d/skills/cloudrun-deploy-skill/scripts/deploy_cloudrun.py -c <YOUR_CONFIG> -s <YOUR_SERVICE>

# 4. ヘルスチェック自動検証
python3 /mnt/d/skills/cloudrun-deploy-skill/scripts/verify_cloudrun.py -c <YOUR_CONFIG> -s <YOUR_SERVICE>
```
