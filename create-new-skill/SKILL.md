---
name: create-new-skill
description: Scaffolds, validates, and syncs standardized Antigravity skills with scripts/, prototype/, templates/, and references/ (including TRIGGERS.md). Use when creating a new skill, auditing or refactoring an existing skill directory, or syncing skills to /mnt/d/skills. Do not use when simply executing or following an existing domain skill.
---

# create-new-skill

Standardized agent skill creator, validator, and synchronizer.

## Core Principle: Code over Prompt

> [!IMPORTANT]
> **実行結果を見て逐次判断する高次思考以外、手順はすべて `scripts/*.py` として 1 コマンド化・決定論的コード化すること。**
> プロンプト推論によるアドホックなシェル操作（`mkdir`, `cp`, `diff` 等）は禁止。
> `SKILL.md` は詳細を書かず、各MDの役割と利用基準をまとめる「統括インデックス」に徹する。

## Operations (`scripts/`)

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `scaffold_skill` | `python3 scripts/scaffold_skill.py --dir <dir> --name <name> --desc "<desc>"` | スキル雛形（11標準構成）を一括生成 |
| `validate_skill` | `python3 scripts/validate_skill.py <skill_dir>` | フロントマター、行数、リンク整合性、必須構成、Mermaid図、4分類ツール、構文を機械的検証 |
| `sync_skill` | `python3 scripts/sync_skill.py --src <dir> --dst <dir> [--apply] [--delete]` | バリデーション、差分比較、安全同期を 1 コマンド実行 |

## Document Index & Criteria

| Document | Role | When to read |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 流用可能資産と案件固有の差し替え境界定義 | 他PJへスキル展開・資産流用する時 |
| **[references/TOOLS.md](references/TOOLS.md)** | 4分類（Command/Shell/MCP/外部 API）仕様・引数 | CLI引数・終了コードの詳細確認時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | Mermaid論理/物理図・シーケンス図・環境変数 | 通信経路・設計全体像の確認時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | 受け入れ合格基準チェックリスト | デプロイ・作成完了の合否判定時 |
| **[references/GUIDE.md](references/GUIDE.md)** | ステップバイステップ操作手順 | 具体的な操作手順の確認・実行時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | 必須環境・CLIバージョン・IAMロール | 実行環境のセットアップ・権限確認時 |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | スキル発動プロンプト例（Positive / Negative）とスモークテスト | トリガー精度の確認・`description` 調整時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | 既知エラーと解決策 | エラー・障害発生時 |

## Workflow Calls
1. `scaffold_skill(--dir, --name, --desc)` → 雛形生成
2. 決定論的処理を `scripts/*.py` へコード化
3. `prototype/PROTOTYPE.md` に流用・差し替え境界を明記
4. `references/TRIGGERS.md` に発動・非発動プロンプト例を定義し、他 `references/*.md` へ詳細を記述（`SKILL.md` は 500 行未満で簡潔に維持）
5. `sync_skill(--src, --dst, --apply)` → 検証＆同期

## Trigger & Exit Criteria
- **Trigger**: スキルの新規作成、標準化監査、または外部スキルディレクトリへの同期時。
- **Exit Criteria**: `python3 scripts/validate_skill.py <skill_dir>` および `python3 scripts/sync_skill.py --src <dir> --dst <dir>` が exit `0`（100% 一致）で完了すること。

## Anti-Patterns
- **No Prompt-driven Procedures**: 1 コマンド化できる手順をプロンプト推論で手動実行しない。
- **No Verbose SKILL.md**: `SKILL.md` に実装コードや詳細長文をダンプしない（500行未満に抑え、専用MDへ委譲）。
- **No Vague Description**: `description` に「What / When / Negative Trigger」を欠いた曖昧な一文を書かない。
- **No Missing PROTOTYPE.md / TRIGGERS.md**: 流用境界と発動プロンプト例のドキュメントを省略しない。
- **No Missing TOOLS.md**: 4分類（`Command`, `Shell`, `MCP`, `外部 API`）を省略しない。
