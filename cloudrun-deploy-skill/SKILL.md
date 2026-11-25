---
name: cloudrun-deploy
description: Deploy and manage containerized services on GCP Cloud Run using user-specified gcloud configurations with deterministic validation and deployment automation.
---

# cloudrun-deploy

Deploy, configure, verify, and manage containerized workloads on Google Cloud Platform (GCP) Cloud Run using user-specified `gcloud` configurations, Cloud Build, and Artifact Registry.

## Core Principle: Code over Prompt

> [!IMPORTANT]
> **実行結果を見て逐次判断する高次思考以外、手順はすべて `scripts/*.py` として 1 コマンド化・決定論的コード化すること。**
> プロンプト推論によるアドホックなシェル操作（`gcloud` 手動連打、未定義タグの当て推量、手動curlポーリング）は禁止。
> `SKILL.md` は詳細を書かず、各MDの役割と利用基準をまとめる「統括インデックス」に徹する。

---

## 規約・利用前提 (Conventions & Prerequisites)

本スキルを呼び出すエージェントおよび開発者が遵守すべき前提条件と規約概要：

- **ユーザー指定 Configuration の尊重**: ユーザー指定の `gcloud` configuration（例: `nanzhiyan`）を常に全ツールへ伝播すること（詳細: [PREREQUISITES.md](references/PREREQUISITES.md)）。
- **CPU スロットリング無効化**: 常駐Bot・ワーカー・WebSocket待受を含むサービスでは、CPU常時割り当て（`cpu-throttling: false`）および `minScale: 1` を必須とすること（詳細: [ARCHITECTURE.md](references/ARCHITECTURE.md)）。
- **単一インスタンス制限**: 自動取引ボット等の二重発注事故防止のため、`maxScale: 1` を厳守すること（詳細: [CHECKLIST.md](references/CHECKLIST.md)）。
- **二重視点アーキテクチャ規約 (Rule.14)**: 論理データフロー図および物理インフラ構成図の双方を含むスタンドアロンHTML仕様書を同梱すること（詳細: [PROTOTYPE.md](prototype/PROTOTYPE.md)）。

---

## Operations (`scripts/`)

> [!NOTE]
> 各スクリプトの詳細なCLI引数、スキーマ、終了コード仕様は [references/TOOLS.md](references/TOOLS.md) を参照。

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `run_full_deployment` | `python3 scripts/run_full_deployment.py -c <cfg> [-s <svc>]` | **【推奨】** 構成検査・API/Repo作成・ビルド・デプロイ・検証の全工程を1コマンドで完全自動実行 | [TOOLS.md#21](references/TOOLS.md) |
| `inspect_gcloud_config` | `python3 scripts/inspect_gcloud_config.py [-c <cfg>] [--json]` | 指定された `gcloud` configuration のプロジェクトID・アカウント・リージョンを解決 | [TOOLS.md#22](references/TOOLS.md) |
| `provision_apis_and_repo` | `python3 scripts/provision_apis_and_repo.py [-c <cfg>] [-p <proj>] [-r <region>]` | 必要なGCP API有効化、Artifact Registry作成、Cloud BuildへのIAM権限付与を自動保証 | [TOOLS.md#23](references/TOOLS.md) |
| `deploy_cloudrun` | `python3 scripts/deploy_cloudrun.py [-c <cfg>] [-s <service>] [--config-file <yaml>]` | Cloud Buildによるコンテナビルド、Artifact Registryプッシュ、Cloud Runへのデプロイを実行 | [TOOLS.md#24](references/TOOLS.md) |
| `verify_cloudrun` | `python3 scripts/verify_cloudrun.py [-c <cfg>] [-s <service>] [--path <path>]` | Cloud RunのReady状態判定および指定エンドポイント（`/api/health`等）の疎通を自動検証 | [TOOLS.md#25](references/TOOLS.md) |

---

## Document Index & Criteria

| Document | Role | When to read |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 流用可能資産と案件固有の差し替え境界定義 | 他PJへスキル展開・資産流用する時 |
| **[references/TOOLS.md](references/TOOLS.md)** | 4分類（Command/Shell/MCP/外部 API）仕様・引数 | CLI引数・終了コードの詳細確認時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | Mermaid論理/物理図・シーケンス図・環境変数 | 通信経路・設計全体像の確認時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | 受け入れ合格基準チェックリスト | デプロイ・作成完了の合否判定時 |
| **[references/GUIDE.md](references/GUIDE.md)** | ステップバイステップ操作手順 | 個別ステップの詳細や手動実行時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | 必須環境・CLIバージョン・IAMロール | 実行環境のセットアップ・権限確認時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | 既知エラーと解決策 | エラー・障害発生時の原因究明時 |

---

## Workflow Calls
1. **通常実行（1コマンド推奨）**:
   `run_full_deployment(--configuration, --service)` → 全工程（検査〜デプロイ〜検証）を決定論的パイプラインで一括完結。
2. **個別ステップ実行（トラブル対応時）**:
   `inspect_gcloud_config` → `provision_apis_and_repo` → `deploy_cloudrun` → `verify_cloudrun` の順で個別検証。

---

## Trigger & Exit Criteria
- **Trigger**: GCP Cloud Run へのコンテナデプロイ、構成確認、または特定 `gcloud` configuration を利用した運用の開始時。
- **Exit Criteria**: `verify_cloudrun.py`（または `run_full_deployment.py`）が終了コード `0` で完了し、Ready状態が `True`、ヘルスチェックが HTTP `200` を返すこと。

---

## Anti-Patterns
- **Never rely on Probabilistic Prompt-driven Orchestration**: アドホックな手動シェル操作を行わず、必ず `scripts/*.py` ツールを介して実行すること。
- **Never hardcode GCP Project IDs in shell commands**: プロジェクトIDは必ず `inspect_gcloud_config.py` 経由で取得すること。
- **Never deploy background bot workloads with CPU throttling enabled**: 常駐Botはスロットリングを無効化（`cpu-throttling: false`）すること。
- **Never allow multi-instance scale-out for automated trading bots**: 二重発注防止のため、`maxScale: 1` を厳守すること。
- **Never ignore PROTOTYPE.md boundaries**: 新規プロジェクト適用時は、流用部分と差し替え部分の境界を [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) で必ず確認すること。
