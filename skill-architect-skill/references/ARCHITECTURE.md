# Architecture & Specifications (`skill-architect`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  Spec[Skill Requirements] --> Scaffold[scaffold_skill.py]
  Scaffold --> SkillDir[Skill Bundle]
  SkillDir --> Validate[validate_skill.py]
  Validate --> Ext["/mnt/d/skills/<name>-skill"]
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant Agent
  participant Scaffold as scaffold_skill.py
  participant Validate as validate_skill.py
  participant External as /mnt/d/skills

  Agent->>Scaffold: Generate 9-part skill skeleton
  Agent->>Agent: Add domain scripts & templates
  Agent->>Validate: Validate structure, AST, Mermaid
  Agent->>External: Sync skill bundle for other agents
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Local Path** | `~/.gemini/antigravity-cli/skills/` | Active Antigravity skills directory |
| **External Path** | `/mnt/d/skills/<name>-skill/` | Shared external skill repository |

## 4. Deliverables
- Standardized skill directory (`SKILL.md`, `scripts/`, `prototype/`, `templates/`, `references/`)
- Synced external package in `/mnt/d/skills/<name>-skill/`
