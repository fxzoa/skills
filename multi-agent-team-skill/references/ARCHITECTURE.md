# Architecture & Specifications (`multi-agent-team-skill`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  Input[Requirements / Context] --> Skill[multi-agent-team-skill]
  Skill --> Output[Deliverables]
  Output --> Validate[scripts/]
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant User
  participant Agent
  participant Script as scripts/
  User->>Agent: Request deliverable
  Agent->>Script: Validate output
  Script-->>User: Verified artifact
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Input** | Workspace files / specs | Source context for generation |

## 4. Deliverables
- Multi-model AI team orchestration
