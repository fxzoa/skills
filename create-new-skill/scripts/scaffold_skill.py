#!/usr/bin/env python3
"""Scaffold a standardized Antigravity skill directory conforming to the 11-part skill architecture.

Includes PROTOTYPE.md for distinguishing reusable components vs. project-specific replacements,
TRIGGERS.md for positive/negative trigger prompt examples, and enforces that SKILL.md acts as
a clean navigation index (<500 lines) rather than a verbose implementation dump.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_inputs(name: str, desc: str) -> list[str]:
    """Validate CLI inputs against Agent Skills frontmatter constraints."""
    errors: list[str] = []
    if not (1 <= len(name) <= 64) or not NAME_PATTERN.match(name):
        errors.append(
            f"Invalid --name '{name}': must be 1-64 chars of lowercase alphanumeric and single hyphens (kebab-case)."
        )
    if not desc.strip() or len(desc) > 1024:
        errors.append("Invalid --desc: must be non-empty and at most 1024 characters.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold standardized 11-part skill bundle.")
    parser.add_argument("--dir", required=True, help="Target skill directory (basename should match --name)")
    parser.add_argument("--name", required=True, help="Skill name (kebab-case, <= 64 chars)")
    parser.add_argument(
        "--desc",
        required=True,
        help="Third-person description covering What, When, and Negative triggers (<= 1024 chars)",
    )
    args = parser.parse_args()

    errors = validate_inputs(args.name, args.desc)
    if errors:
        for err in errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        return 1

    base = Path(args.dir).resolve()
    if base.name != args.name:
        print(
            f"[WARN] Target directory basename '{base.name}' differs from --name '{args.name}'. "
            "Agent Skills standard requires them to match.",
            file=sys.stderr,
        )

    for sub in ["scripts", "prototype", "templates", "references"]:
        (base / sub).mkdir(parents=True, exist_ok=True)

    # 1. SKILL.md: 高凝集インデックスハブ（利用規約・各MD機能・利用条件・参照先まとめ）
    (base / "SKILL.md").write_text(
        f"""---
name: {args.name}
description: {args.desc}
---

# {args.name}

Execute standard operations via pre-built scripts in `scripts/`.
All operational procedures, parameters, and tool interfaces are strictly delegated to dedicated reference documents.

## Core Philosophy: Deterministic Code-driven Control over Probabilistic Control

> [!IMPORTANT]
> **Probabilistic Prompt-driven Orchestration is strictly prohibited for procedural workflows.**
> When an agent relies on prompt instructions to manually synthesize multi-step shell commands, parse unstructured text, or guess operational parameters, it introduces probabilistic failure modes.
> All procedural workflows must be materialized and codified into single-command, deterministic Python scripts (`scripts/*.py`).
> `SKILL.md` serves as a high-level navigation index and conventions hub (<500 lines); concrete implementations are delegated to specialized Markdown files.

---

## 規約・利用前提 (Conventions & Prerequisites)

本スキルを利用するエージェントおよび開発者が遵守すべき全体規約と前提条件の概要：

- **ユーザー指定パラメータ・環境の尊重**: ユーザー指定の環境設定・プロファイル（例: configuration, project, namespace等）を確実に全操作へ伝播すること（詳細: [references/PREREQUISITES.md](references/PREREQUISITES.md)）。
- **プロトタイプの流用と差し替え境界の遵守**: 既存資産を流用する部分と、対象プロジェクトに応じて差し替えるべき部分の境界を厳守すること（詳細: [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)）。
- **発動条件と非発動条件の明確化**: Positive / Negative トリガープロンプト例を定義し、誤発動を防止すること（詳細: [references/TRIGGERS.md](references/TRIGGERS.md)）。
- **決定論的検証の完遂**: 手動推測に頼らず、検証スクリプトの exit 0 をもって完了とすること（詳細: [references/CHECKLIST.md](references/CHECKLIST.md)）。

---

## ドキュメント体系・利用基準 (Document Index & Criteria)

| ドキュメント | 主な機能・収録内容 | 参照・利用基準（いつ読むべきか） |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | 実稼働リファレンス資産の全容と、流用可能部分 / 案件ごとに差し替える部分の境界分離定義 | 他プロジェクトへ本スキルを適用する際、どの定義をそのまま流用し、どのコードを差し替えるべきか判断する時 |
| **[references/TOOLS.md](references/TOOLS.md)** | 4大分類（Command / Shell / MCP / 外部 API）のツール仕様、CLI引数、終了コード、入出力詳細 | 各 `scripts/*.py` の詳細なCLIオプションや終了コード仕様を確認する時 |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | Mermaid論理・物理構成図、シーケンス図、環境変数・API一覧 | システム全体の通信経路、データフロー、および環境変数の仕様を確認する時 |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | 事前環境、プロビジョニング、デプロイ、稼働検証の合格基準一覧 | 操作前後の安全確認および受け入れ検証を漏れなく実施する時 |
| **[references/GUIDE.md](references/GUIDE.md)** | 初回設定から実行、検証に至るステップバイステップ操作ガイド | 実際のコマンド実行手順やワークフローの詳細を確認・実行する時 |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | 必要な実行ランタイム、CLIバージョン、必須アカウント権限/IAM一覧 | 実行環境のセットアップやアカウント権限不足の確認を行う時 |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | スキル発動プロンプト例（Positive / Negative）とスモークテスト手順 | 発動精度の検証や `description` のチューニングを行う時 |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | 既知のエラー、根本原因、および解決策一覧 | 実行エラーや予期せぬ不具合が発生した時 |

---

## Pre-Built Operations (`scripts/`)

> [!NOTE]
> Detailed CLI flags, schemas, exit codes, and agent execution protocols are documented in [references/TOOLS.md](references/TOOLS.md).

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `example_op` | `python3 scripts/example_op.py <arg>` | Describe operation | [TOOLS.md#11](references/TOOLS.md) |

---

## Workflow Calls
1. `example_op(<arg>)` → execute core workflow (参照: [GUIDE.md](references/GUIDE.md)).

---

## Trigger & Exit Criteria
- **Trigger**: Describe when to activate `{args.name}`.
- **Exit Criteria**: All automated checks pass with exit code `0` and verification in `CHECKLIST.md` is met.

---

## Anti-Patterns
- **Never rely on Probabilistic Prompt-driven Orchestration**: Do not leave procedural steps for the agent to manually synthesize ad-hoc shell commands. Materialize them into deterministic `scripts/*.py`.
- **Never dump verbose implementation details into SKILL.md**: Keep `SKILL.md` clean as an index (<500 lines); delegate detailed steps to `references/GUIDE.md` and interfaces to `references/TOOLS.md`.
- **Never write vague frontmatter descriptions**: Always state What, When, and Negative triggers in third person.
- **Never ignore PROTOTYPE.md or TRIGGERS.md**: Clearly distinguish reusable boundaries and maintain trigger prompt examples.
- **Never omit references/TOOLS.md or skip the 4 tool categories (`Command`, `Shell`, `MCP`, `外部 API`).**
""",
        encoding="utf-8",
    )

    # 2. prototype/PROTOTYPE.md: 流用部分と差し替え部分の境界分離定義
    (base / "prototype" / "PROTOTYPE.md").write_text(
        f"""# PROTOTYPE.md: プロトタイプ資産仕様書・流用/入替境界ガイド (`{args.name}`)

本ドキュメントは、`prototype/` に収録されている実稼働リファレンス資産の構成を解説し、**「他のプロジェクトでもそのまま流用できる汎用設計」** と **「スキル適用時にプロジェクト固有要件として差し替えるべき境界」** を明確に定義・分離したものです。

---

## 1. プロトタイプ収録資産の全体構造

```text
prototype/
└── example/
    └── sample_workload.ext             # 実稼働リファレンス実装
```

---

## 2. 流用できる部分（汎用コア設計） vs 差し替える部分（個別要件）

他プロジェクトへ展開する際は、以下の境界線に従って作業を行います。

| 構成要素 | 他プロジェクトでもそのまま「流用」できる部分（汎用資産） | プロジェクトごとに「差し替える」部分（固有要件） |
|:---|:---|:---|
| **コアロジック / パイプライン** | ・定型的なビルド/デプロイ/検証のフロー<br>・共通エラーハンドリング | ・対象リポジトリ固有のファイルパス<br>・固有の実行コマンド・ポート |
| **環境変数 / 設定** | ・共通の命名規則・構造 | ・プロジェクト固有の認証情報・接続先エンドポイント |

---

## 3. 他プロジェクト適用時の「差し替え」チェックリスト

1. `templates/` 配下のテンプレートをプロジェクトルートへコピー
2. プロジェクト固有の変数・コマンドへ置換
3. `scripts/` の自動化ツールを実行して検証完了を確認
""",
        encoding="utf-8",
    )

    (base / "templates" / ".gitignore.tmpl").write_text(
        ".env\n.env.*\n!.env.example\n*.pem\n*.key\nlogs/\ntmp/\n__pycache__/\n*.pyc\n",
        encoding="utf-8",
    )

    (base / "references" / "TOOLS.md").write_text(
        f"""# Tools & Interfaces Reference (`{args.name}`)

This document defines tool interfaces, CLI signatures, and protocol classifications for `{args.name}`.
Tools are organized by execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `example_op.py` | Core workflow operator | `python3 scripts/example_op.py <arg>` | `0`: Success, `1`: Failure |

### 1.1 `example_op.py`
- **Arguments**:
  - `<arg>`: Description
- **Output**: Description

---

## 2. Shell コマンド (OS & Infrastructure)

| Shell Command / Utility | Purpose | Example |
|:---|:---|:---|
| `python3` | Script execution harness | `python3 scripts/example_op.py --help` |

---

## 3. MCP ツール (Agent Primitives)

| MCP Primitive | Role in Skill | Usage Context |
|:---|:---|:---|
| `run_command` | Execute pre-built scripts in `scripts/` | Main tool execution |
| `read_file` | Read specifications, configs, and inputs | File inspection |
| `write_file` / `edit_file` | Generate or patch artifacts | Code generation |

---

## 4. 外部 API (External REST / RPC Services)

| Service / API | Protocol | Endpoint | Auth | Purpose |
|:---|:---|:---|:---|:---|
| N/A | HTTP/REST | - | - | External integrations (if any) |
""",
        encoding="utf-8",
    )

    (base / "references" / "ARCHITECTURE.md").write_text(
        f"""# Architecture & Specifications (`{args.name}`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  Input[Input / Config] --> Script[scripts/]
  Script --> Output[Deliverables]
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant Agent
  participant Script as scripts/
  Agent->>Script: Invoke pre-built operation
  Script-->>Agent: Verified result
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Env** | `EXAMPLE_VAR` | Example config |

## 4. Deliverables
- Standard output artifacts
""",
        encoding="utf-8",
    )

    (base / "references" / "TRIGGERS.md").write_text(
        f"""# Trigger Prompts & Smoke Tests (`{args.name}`)

本ドキュメントは、`{args.name}` の発動精度（Routing Accuracy）を検証するためのプロンプト例とスモークテスト手順を定義します。

---

## 1. Positive Trigger Examples（発動すべきプロンプト例）

* 「（ここに `{args.name}` を発動させたい具体的なユーザー発話例を2〜3件記載）」

---

## 2. Negative Trigger Examples（発動してはいけないプロンプト例）

* 「（ここに類似しているが別スキル／通常作業として扱うべき発話例を2〜3件記載）」

---

## 3. Smoke Test 手順

1. `SKILL.md` の `description` に **What / When / Negative Trigger** が三人称で含まれているか確認する。
2. Positive 例で本スキルが候補に選ばれ、Negative 例で誤発動しないことを確認する。
""",
        encoding="utf-8",
    )

    (base / "references" / "CHECKLIST.md").write_text(
        f"""# Acceptance Checklist (`{args.name}`)

- [ ] All 11 standard parts exist (`SKILL.md`, `scripts/`, `prototype/PROTOTYPE.md`, `templates/.gitignore.tmpl`, `references/{{ARCHITECTURE,CHECKLIST,GUIDE,PREREQUISITES,TOOLS,TRIGGERS,TROUBLESHOOTING}}.md`).
- [ ] `SKILL.md` frontmatter `name` matches directory name (`kebab-case`, <= 64 chars) and `description` covers What / When / Negative triggers (<= 1024 chars).
- [ ] `SKILL.md` is concise (< 500 lines) with valid internal relative links.
- [ ] Procedural workflows are materialized into deterministic Python scripts in `scripts/`.
- [ ] `references/TRIGGERS.md` defines Positive & Negative trigger prompt examples.
- [ ] `references/TOOLS.md` covers Command, Shell, MCP, and 外部 API.
- [ ] `prototype/PROTOTYPE.md` clarifies reusable vs project-specific parts.
- [ ] Scripts pass `validate_skill.py` (syntax, `--help`, and structure checks).
""",
        encoding="utf-8",
    )
    (base / "references" / "GUIDE.md").write_text(
        f"# Operation Guide (`{args.name}`)\n\n1. Run `scripts/` operations.\n2. Verify against `CHECKLIST.md`, `references/TRIGGERS.md`, and `references/TOOLS.md`.\n",
        encoding="utf-8",
    )
    (base / "references" / "PREREQUISITES.md").write_text(
        f"# Prerequisites (`{args.name}`)\n\n- Python >= 3.10\n",
        encoding="utf-8",
    )
    (base / "references" / "TROUBLESHOOTING.md").write_text(
        f"# Troubleshooting (`{args.name}`)\n\n| Symptom | Root Cause | Fix |\n|:---|:---|:---|\n| Example error | Cause | Fix |\n",
        encoding="utf-8",
    )

    print(f"[OK] Scaffolded standardized 11-part skill '{args.name}' in {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
