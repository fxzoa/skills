---
name: dev-environment-setup
description: Installs, configures, and verifies developer CLI environments (uv, nvm, Node.js LTS, Wrangler, gcloud, Colab CLI, Kaggle CLI) on Linux/WSL2 with idempotent automation. Use when provisioning or repairing a development workstation environment. Do NOT use for Docker-only setups (use kiri-docker-setup) or single-service deployments.
---

# dev-environment-setup

Deterministic setup and health verification for standard developer CLI tooling suite on Linux/WSL2.

## Core Principle: Code over Prompt

> [!IMPORTANT]
> すべてのツールインストールおよび健全性検証は `scripts/*.sh` および `scripts/*.py` により 1 コマンド・決定論的に実行すること。
> 手動での個別シェル実行や推論によるパス設定変更は禁止。

## Operations (`scripts/`)

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `setup_dev_env` | `bash scripts/setup_dev_env.sh` | 全 CLI（uv, nvm, Node.js, Wrangler, gcloud, colab, kaggle）を冪等に一括導入 |
| `verify_dev_env` | `python3 scripts/verify_dev_env.py` | 各ツールのバージョン・実行可能性を機械的にスモークテスト |

## Document Index & Criteria

| Document | Role | When to read |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 流用可能資産と案件固有の差し替え境界定義 | 他OS（macOS等）への移植や特定CLIの追加・除外時 |
| **[references/TOOLS.md](references/TOOLS.md)** | 導入する各 CLI の仕様・引数・認証方法 | CLIごとのログインや初期設定を行う時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | ディレクトリ構造・PATH 境界・依存関係図 | 実行環境の分離構造を確認する時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | セットアップ完了受け入れ合格基準 | 環境初期化後の合否判定時 |
| **[references/GUIDE.md](references/GUIDE.md)** | ステップバイステップ操作手順 | 個別ツールの再セットアップや手動反映時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | 必須環境（Ubuntu/WSL2, curl, tar, bash, git） | 導入前のシステム要件確認時 |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | スキル発動プロンプト例（Positive / Negative） | スキル呼び出しの精度確認時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | 既知エラーと解決策（Python 3.14 six 欠落等） | インストール失敗やコマンド不達時 |

## Workflow Calls
1. `bash scripts/setup_dev_env.sh` → 冪等インストール実行
2. `python3 scripts/verify_dev_env.py` → 正常性検証（exit 0 を確認）
3. `source ~/.bashrc` → 現行シェルに PATH 反映

## Trigger & Exit Criteria
- **Trigger**: 開発環境の新規プロビジョニング、Linux/WSL2 ワークステーションの初期セットアップ、または CLI ツール群の破損・修復時。
- **Exit Criteria**: `python3 scripts/verify_dev_env.py` が exit `0`（全ツール [PASS]）で完了すること。

## Anti-Patterns
- **No Manual apt Installations**: システムを汚す不要なグローバル apt パッケージを乱立させない（nvm, uv, ユーザーアーカイブを活用）。
- **No Unversioned Dependencies**: Kaggle の Python 3.14 互換性問題（`six` 欠落）を手動パッチせず、自動インストーラー（`--with six`）に集約する。
- **No Missing Smoke Tests**: インストール完了後に `verify_dev_env.py` をスキップしない。
