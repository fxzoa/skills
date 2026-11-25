# PROTOTYPE.md: プロトタイプ資産仕様書・流用/入替境界ガイド (create-new-skill)

本ドキュメントは、`create-new-skill` スキルにおけるプロトタイプ資産の取り扱いと、スキル生成時の汎用流用部分と案件固有の差し替え部分の境界を定義したものです。

---

## 1. 流用できる部分（スキル共通標準）
- 全スキル共通の11標準構成（`SKILL.md`, `prototype/PROTOTYPE.md`, `templates/.gitignore.tmpl`, `scripts/`, `references/` 7ファイル）
- `SKILL.md` のインデックス構成（規約・ドキュメント体系・Pre-Built Operations・Anti-Patterns）
- `references/TRIGGERS.md` による発動・非発動プロンプト例の定義フォーマット
- `validate_skill.py` および `sync_skill.py` による決定論的検証・同期メカニズム

## 2. 差し替える部分（スキル固有要件）
- `scripts/*.py` の具体的自動化コード
- `references/` の各ドキュメントに記述する対象技術（GCP, Docker, Kaggle等）固有の仕様・発動プロンプト例・手順・トラブルシューティング
