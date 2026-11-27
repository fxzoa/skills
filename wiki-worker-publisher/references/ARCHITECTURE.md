# Architecture & Specifications (`wiki-worker-publisher`)

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
