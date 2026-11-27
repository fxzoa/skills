# Architecture & Specifications (`tech-blog-html-skill`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  Input[Requirements / Context] --> Skill[tech-blog-html-skill]
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
- 9-block technical blog standalone HTML generator
