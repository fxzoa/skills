---
name: kiri-docker-setup
description: Installs and configures Kiri lightweight Rust container engine, Docker CLI plugins (Compose/Buildx), systemd daemon service on Linux/WSL2, and workspace agent skills. Use when setting up a fresh machine or container environment with Kiri. Do NOT use for standard Docker Desktop or cloud VM deployments.
---

# kiri-docker-setup

Standardized setup runbook and deterministic automation for Kiri container runtime and Antigravity workspace skills.

## Core Principle: Code over Prompt

> [!IMPORTANT]
> **実行結果を見て逐次判断する高次思考以外、手順はすべて `scripts/*.py` として 1 コマンド化・決定論的コード化すること。**
> プロンプト推論によるアドホックなシェル操作は禁止。
> `SKILL.md` は詳細を書かず、各ドキュメントの役割と利用基準をまとめる「統括インデックス」に徹する。

## Operations (`scripts/`)

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `install_kiri` | `python3 scripts/install_kiri.py` | Kiriバイナリ、Docker CLI、Compose/Buildxプラグイン取得配置とDockerコンテキスト作成 |
| `setup_service` | `python3 scripts/setup_service.py` | systemd `kiri.service` 登録、常駐自動起動化、ソケット権限調整 |
| `link_skills` | `python3 scripts/link_skills.py` | `/mnt/d/skills` の全スキルを `.agents/skills` およびグローバル設定へ一括シンボリックリンク |

## Document Index & Criteria

| Document | Role | When to read |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 流用可能資産と案件固有の差し替え境界定義 | 他OSや別WSLディストロへスキル展開する時 |
| **[references/TOOLS.md](references/TOOLS.md)** | 4分類（Command/Shell/MCP/外部 API）仕様・引数 | CLI引数・終了コードの詳細確認時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | システム構成・通信経路・権限モデル・環境変数 | 通信経路・ソケット設計の確認時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | 受け入れ合格基準チェックリスト | インストール・セットアップ完了の合否判定時 |
| **[references/GUIDE.md](references/GUIDE.md)** | ステップバイステップ操作手順 | 具体的な操作手順の確認・実行時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | 必須環境・CLIバージョン・権限要件 | 実行環境のセットアップ・前提確認時 |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | スキル発動プロンプト例（Positive / Negative） | トリガー精度の確認・`description` 調整時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | 既知エラーと解決策 | エラー・障害発生時 |

## Workflow Calls
1. `python3 scripts/install_kiri.py` → バイナリとCLIプラグインの配置
2. `python3 scripts/setup_service.py` → systemd 自動起動サービス有効化
3. `python3 scripts/link_skills.py` → ワークスペーススキルの同期・リンク
4. `docker run --rm alpine echo hello` によるスモークテスト検証

## Trigger & Exit Criteria
- **Trigger**: 新規マシン、WSL環境構築、Dockerコンテナ環境の初期化、またはスキル一括再設定時。
- **Exit Criteria**: `systemctl is-active kiri.service` が active であり、`docker ps` および `docker run --rm alpine echo hello` が exit `0` で成功すること。

## Anti-Patterns
- **No Prompt-driven Procedures**: スクリプト化されている手順をプロンプト推論でアドホックに手動実行しない。
- **No Direct Non-Root Daemon Execution**: Linux 環境で Kiri を一般ユーザーのまま起動しない（カーネルのコンテナ分離に root / systemd が必須）。
- **No Static Socket Permission Assumption**: ソケット作成後のパーミッション調整（`chmod 666`）を怠り、一般ユーザーからの Docker コマンドを拒否させない。
- **No Manual Skill Copying**: `/mnt/d/skills` から実体コピーを行わず、シンボリックリンクを用いて最新コミットを常に反映させる。
