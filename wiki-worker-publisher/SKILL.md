---
name: wiki-worker-publisher
description: Publishes standalone HTML documents to Cloudflare Workers Wiki (wiki.btczoa.app) with automated metadata catalog registration, build, deployment, and live URL verification. Use when adding or updating documents on wiki-worker. Do NOT use for general static web hosting or Kaggle/Colab notebook deployments.
---

# wiki-worker-publisher

Cloudflare Workers 上で運用されている社内技術ポータル `wiki.btczoa.app`（`wiki-worker`）へ、スタンドアロンHTMLドキュメント（構成図、Tree、仕様書等）を決定論的かつ安全に追加・登録・デプロイ・検証するスキル。

## コア原則 (Core Principles)

1. **決定論的1コマンド実行**: 手動の `cp` や `wrangler` コマンドではなく、`scripts/publish_doc.py` によりカタログ登録・ビルド・デプロイ・URL確認を一括自動実行する。
2. **中間ファイル・スクリプトの完全保持ポリシー**: 生成スクリプト、作業用スクリプト、ログファイル等の作成物は自動削除せず、すべてディスク上に永続保持する。
3. **ワークスペース整合性**: `cf-workers` ルートの依存関係（`hono` や `common-worker-utils`）のシンボリックリンクが維持されていることを前提とし、必要に応じてルートから復元する。

## 操作インターフェース (`scripts/`)

| 操作 | 実行コマンド | 用途 |
|:---|:---|:---|
| **ドキュメント発行・デプロイ** | `python3 scripts/publish_doc.py --html <path> --category <cat> [--title <title>] [--tags <tags>] [--featured]` | HTML配置、カタログ登録、ビルド、デプロイ、URL検証の一括実行 |
| **ローカルビルドのみ検証** | `python3 scripts/publish_doc.py --html <path> --category <cat> --skip-deploy` | デプロイを伴わない事前ビルド検証 |

### 対象カテゴリ (`--category`)
- `llm-infra`: LLM推論基盤、GPUサーバー、クラウドインフラ、GCP/AWS/Cloudflare（既定）
- `ai-agents`: 自律エージェント、プロンプト工学、AIアーキテクチャ
- `trading-bots`: Hyperliquid自動売買、BOT構成
- `macro-finance`: 金融・マクロ経済分析レポート

## ドキュメントインデックス

| ファイル | 役割 | 参照タイミング |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 流用可能資産と差し替え境界 | 他プロジェクト・環境への展開時 |
| **[references/TOOLS.md](references/TOOLS.md)** | CLIツール・スクリプト仕様詳細 | コマンド引数・仕様確認時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | wiki-worker アーキテクチャと全体フロー | システム構成・通信経路確認時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | 発行・デプロイ合格判定チェックリスト | デプロイ完了確認時 |
| **[references/GUIDE.md](references/GUIDE.md)** | ステップバイステップ発行ガイド | 手順確認時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | 必要前提条件（Wrangler, OAuth認証） | 環境確認・トラブル時 |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | スキル発動プロンプト例とスモークテスト | トリガー調整時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | 既知エラーと復旧手順 | デプロイ失敗・依存エラー発生時 |

## Trigger & Exit Criteria
- **Trigger**: Requests like "WIKI-WORKERへ追加して", "wiki.btczoa.appにデプロイして", or adding/updating HTML documents on wiki-worker.
- **Exit Criteria**: `python3 scripts/publish_doc.py` completes with exit code 0 and the live URL returns HTTP 200.

## Anti-Patterns
- Never delete temporary scripts or artifacts during publication without user consent.
- Never manually edit `dist/catalog.json` directly (always generate via `npm run build` or `scripts/publish_doc.py`).
- Never run ad-hoc shell copy/wrangler commands without updating metadata in `scripts/build-wiki.mjs`.

