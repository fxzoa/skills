---
name: setup-run-crawl4ai
description: Provisions, configures, and operates a self-hosted Crawl4AI headless browser crawler in Docker with deterministic token management, health checking, and Markdown extraction. Use when setting up Crawl4AI on a new machine, verifying container health, or scraping URLs via the local Crawl4AI API. Do NOT use for deploying arbitrary Docker Compose stacks to cloud VMs or simple static HTTP fetches without headless browser rendering.
---

# setup-run-crawl4ai

Provision, configure, and operate self-hosted Crawl4AI Docker containers across developer machines (home PC, office PC, cloud VMs) with deterministic 1-click batch setup.

## Core Principle: Code over Prompt

> [!IMPORTANT]
> **実行結果を見て逐次判断する高次思考以外、手順はすべて `scripts/*.py` として 1 コマンド化・決定論的コード化すること。**
> プロンプト推論による手動 Docker コマンド連打やアドホックなトークン設定は禁止。
> `SKILL.md` は詳細を書かず、各MDの役割と利用基準をまとめる「統括インデックス」に徹する。

---

## 規約・利用前提 (Conventions & Prerequisites)

本スキルを呼び出すエージェントおよび開発者が遵守すべき前提条件と規約概要：

- **Docker デーモン必須**: 実行環境に Docker Engine または Docker Desktop が起動していること（詳細: [PREREQUISITES.md](references/PREREQUISITES.md)）。
- **shm-size 1g 規約**: ヘッドレスブラウザ（Chromium）のクラッシュを防ぐため、コンテナ起動時は必ず `--shm-size=1g` を適用すること。
- **環境変数の永続化**: 生成されたトークンおよびベースURLは指定された `.env` ファイルへ確実に追記・同期すること（詳細: [CHECKLIST.md](references/CHECKLIST.md)）。
- **プロトタイプ境界の遵守 (PROTOTYPE.md)**: 別端末展開時の流用部分と環境固有の差し替え部分を [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) で確認すること。

---

## Operations (`scripts/`)

> [!NOTE]
> 各スクリプトの詳細なCLI引数、スキーマ、終了コード仕様は [references/TOOLS.md](references/TOOLS.md) を参照。

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `setup_crawl4ai` | `python3 scripts/setup_crawl4ai.py [--port <p>] [--env-file <path>]` | **【推奨】** トークン自動生成・Docker起動・健全性確認・`.env` 保存を1コマンドで一括実行 | [TOOLS.md#21](references/TOOLS.md) |
| `verify_crawl4ai` | `python3 scripts/verify_crawl4ai.py [--env-file <path>]` | ヘルスチェック確認およびテストURLスクレイピングによる動作合否判定 | [TOOLS.md#22](references/TOOLS.md) |
| `crawl_url` | `python3 scripts/crawl_url.py <url> [-o <out>] [--format markdown]` | 稼働中のコンテナを利用して対象URLを即座にスクレイピング・Markdown化 | [TOOLS.md#23](references/TOOLS.md) |

---

## Document Index & Criteria

| Document | Role | When to read |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 流用可能資産と環境固有の差し替え境界定義 | 会社PCや別端末へバッチ導入・流用する時 |
| **[references/TOOLS.md](references/TOOLS.md)** | 4分類（Command/Shell/MCP/外部 API）仕様・引数 | CLI引数・終了コードの詳細確認時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | Mermaid論理/物理図・シーケンス図・環境変数 | コンテナアーキテクチャ・通信仕様の確認時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | 受け入れ合格基準チェックリスト | コンテナ導入・セットアップ完了の合否判定時 |
| **[references/GUIDE.md](references/GUIDE.md)** | ステップバイステップ操作手順 | 会社PC等での初回導入・手動バッチ実行時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | 必須環境（Docker, Python, ポート要件） | 実行環境のセットアップ・権限確認時 |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | 発火条件（Positive/Negative）とスモークテスト | スキル適用可否の判定・検証時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | ポート競合、shm不足、タイムアウト等の解決策 | コンテナ起動失敗やスクレイピングエラー発生時 |

---

## Workflow Calls
1. **セットアップ**: `setup_crawl4ai(--env-file)` → トークン生成、コンテナ起動、健全性確認、設定ファイル保存を一括実行。
2. **検証**: `verify_crawl4ai(--env-file)` → 健全性ステータスおよび実スクレイピング疎通を検査。
3. **スクレイピング実行**: `crawl_url(<url>, --format)` → 必要なWebページをクリーンなMarkdown/JSONとして取得。

---

## Trigger & Exit Criteria
- **Trigger**: 新端末（会社PC等）での Crawl4AI 導入、コンテナ起動、またはWebスクレイピング基盤の構築要求時。
- **Exit Criteria**: `verify_crawl4ai.py` が終了コード `0` を返し、テストスクレイピングが成功すること。

---

## Anti-Patterns
- **Never run raw ad-hoc docker commands**: 必ず `scripts/setup_crawl4ai.py` 経由で実行すること。
- **Never omit shm-size parameter**: `--shm-size=1g` なしで起動すると Chromium がメモリ不足で異常終了する。
- **Never leave tokens unsaved**: 発行した認証情報は必ず `.env` へ同期し、別セッションでも再利用可能にすること。
