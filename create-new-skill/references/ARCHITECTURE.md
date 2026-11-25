# Architecture & Specifications (`create-new-skill`)

> [!NOTE]
> プロジェクトの Rule.11（HTML-First ポリシー）はユーザー向け技術文書・報告書を対象としており、スキル内部の `references/` における軽量な構造把握では Mermaid 図解を標準採用しています。

## 1. Architecture Diagram
```mermaid
flowchart LR
  Spec[Skill Requirements] --> Scaffold[scaffold_skill.py]
  Scaffold --> SkillDir[11-Part Skill Bundle]
  SkillDir --> Validate[validate_skill.py]
  Validate --> Sync[sync_skill.py]
  Sync --> Ext["/mnt/d/skills/<name>-skill"]
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant Agent
  participant Scaffold as scaffold_skill.py
  participant Validate as validate_skill.py
  participant Sync as sync_skill.py
  participant External as /mnt/d/skills

  Agent->>Scaffold: Generate 11-part skill skeleton
  Agent->>Agent: Add scripts, TRIGGERS.md & references
  Agent->>Validate: Validate frontmatter, links, AST, Mermaid
  Agent->>Sync: Validate & mirror skill bundle
  Sync->>External: Deterministic sync for other agents
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Local Path** | `~/.gemini/antigravity-cli/skills/` | Active Antigravity skills directory |
| **External Path** | `/mnt/d/skills/<name>-skill/` | Shared external skill repository |

## 4. Deliverables
- Standardized 11-part skill directory (`SKILL.md`, `scripts/`, `prototype/PROTOTYPE.md`, `templates/.gitignore.tmpl`, `references/` 7 files)
- Synced external package in `/mnt/d/skills/<name>-skill/`
