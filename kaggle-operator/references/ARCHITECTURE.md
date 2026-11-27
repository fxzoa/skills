# Architecture & Specifications (`kaggle-operator`)

## 1. Architecture Diagram
```mermaid
flowchart TD
  Op[deploy_kaggle.py] -->|1. Check/Create| DS[Kaggle Private Dataset -dataset]
  Op -->|2. Push| Kernel[Kaggle Kernel -notebook]
  Kernel -->|Runs on| Cloud[Kaggle Cloud GPU Batch]
  Cloud -->|Downloads model to /tmp/models| HF[Hugging Face / Direct URL]
  Check[check_kaggle_run.sh] -->|Status & Output| Cloud
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant Script as deploy_kaggle.py
  participant KaggleAPI as Kaggle Cloud API
  participant Monitor as check_kaggle_run.sh

  Script->>KaggleAPI: kaggle datasets status <dataset>
  alt Missing
    Script->>KaggleAPI: publish_kaggle_dataset.sh create
  end
  Script->>KaggleAPI: kaggle kernels push -p <dir>
  loop Until COMPLETE or ERROR
    Monitor->>KaggleAPI: kaggle kernels status <notebook>
  end
  Monitor->>KaggleAPI: kaggle kernels output (logs)
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Env** | `KAGGLE_API_TOKEN`, `HF_TOKEN` | Kaggle CLI auth and optional HF download auth |
| **External Data** | `kernel-metadata.json`, `dataset-metadata.json` | Resource IDs (`-notebook`, `-dataset`) |
| **External API** | Kaggle REST API (`datasets`, `kernels`) | Resource verification, creation, push, log retrieval |

## 4. Deliverables
- Deployed Kaggle Private Dataset (`-dataset`) and Notebook (`-notebook`)
- Downloaded execution logs (`<out_dir>/<slug>.log`, `logs/*.log`) and verified `http.rest` responses
