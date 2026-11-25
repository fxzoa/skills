# Trigger Prompts & Smoke Tests (`create-new-skill`)

本ドキュメントは、`create-new-skill` の **発動精度（Routing Accuracy）** を維持・検証するためのプロンプト例（Positive / Negative）とスモークテスト手順を定義します。

---

## 1. Positive Trigger Examples（発動すべきプロンプト例）

以下の意図を含むユーザー要求では、`create-new-skill` が選択・参照されるべきです。

1. **新規スキルの雛形作成**
   * 「新しいスキル `my-deploy-skill` の雛形を標準構成で作成して」
   * 「Docker デプロイ手順を再利用可能な Antigravity スキルとしてパッケージ化したい」
2. **既存スキルの標準化・監査・バリデーション**
   * 「作成したスキルディレクトリが標準構成と規約を満たしているか検証して」
   * 「既存スキルの `SKILL.md` と `references/` をレビューして不足ファイルを補完して」
3. **外部スキルリポジトリへの安全同期**
   * 「ローカルで修正したスキルを検証したうえで `/mnt/d/skills/` へ差分確認・同期して」

---

## 2. Negative Trigger Examples（発動してはいけないプロンプト例）

以下の要求はスキル作成・監査ではないため、`create-new-skill` を誤発動させないでください。

1. **既存スキルの単なる利用・実行**
   * 「`run-crawl4ai-docker` を使ってこの URL をスクレイピングして」（対象スキル自体を使うタスク）
   * 「`colab-notebook` スキルに従ってノートブックを作って」（個別スキルの利用タスク）
2. **通常のアプリケーション開発や単発スクリプト作成**
   * 「FastAPI でユーザー登録 API を実装して」
   * 「Python で CSV を集計するワンオフスクリプトを書いて」

---

## 3. Smoke Test 手順（`description` チューニング時）

`SKILL.md` の `description` または構成を変更した際は、以下を確認します。

1. **静的検証**: `python3 scripts/validate_skill.py <skill_dir>` が exit `0` を返すこと。
2. **トリガー整合確認**:
   * `description` に **What（何をするか）**・**When（いつ使うか）**・**Negative Trigger（何に使わないか）** が三人称で含まれているか。
   * Positive 例のプロンプトを読んだエージェントが迷わず本スキルを候補に挙げられるか。
   * Negative 例のプロンプトで誤って候補に入らないか。
