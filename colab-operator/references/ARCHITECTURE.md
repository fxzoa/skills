# Architecture & Specifications (`colab-operator`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  CLI[colab CLI Scripts] -->|ADC Auth| API[Google Colab API]
  API -->|Provision / Exec| VM[Colab GPU/TPU VM /content]
  VM -->|Logs & Status| CLI
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant Deploy as deploy_colab.sh
  participant Colab as Colab VM (-s session)
  participant Check as check_colab_run.sh
  participant Stop as stop_colab.sh

  Deploy->>Colab: colab new -s <session> --gpu <type>
  Deploy->>Colab: colab exec -s <session> -f <nb.ipynb>
  Check->>Colab: colab status & colab log
  Note over Deploy,Check: Patch locally & re-exec on error
  Stop->>Colab: colab stop -s <session>
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Env / Auth** | Google ADC (`gcloud auth application-default login`) | Headless Colab API authentication |
| **External Data** | Local `.ipynb` / `.py`, `/content/.env` | Remote execution target and VM secrets |
| **External API** | Google Colab API (`new`, `exec`, `status`, `log`, `stop`) | VM lifecycle and kernel execution |

## 4. Deliverables
- Active/verified Colab session output and logs (`colab log -s <session>`)
- Verified `http.rest` inference results and clean session teardown
