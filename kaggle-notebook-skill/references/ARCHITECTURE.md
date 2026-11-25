# Architecture & Specifications (`kaggle-notebook`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  Client[External Client / IDE] -->|HTTPS :443 Bearer| CF[Cloudflare Named Tunnel]
  CF -->|HTTP 127.0.0.1:8000| Uvicorn[FastAPI Proxy server.py]
  Uvicorn -->|HTTP 127.0.0.1:8001| Engine[LLM Engine / Strata / llama.cpp]
  Engine -->|CUDA| GPUs[Kaggle Tesla T4 x2 32GB VRAM]
  DS[Kaggle Private Dataset .env] -.->|/kaggle/input| Uvicorn
  PM[Kaggle Public Model Weights] -.->|/kaggle/input or /tmp/models| Engine
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant User as Operator / Script
  participant Kaggle as Kaggle Batch (T4 x2)
  participant Proxy as FastAPI (:8000)
  participant Engine as LLM Backend (:8001)
  participant CF as cloudflared

  User->>Kaggle: deploy_kaggle() -> kernels push
  Kaggle->>Kaggle: Dump env & load external .env
  Kaggle->>Proxy: Start Uvicorn (/tmp/.venv)
  Proxy->>Engine: Spawn backend process
  loop Poll /api/v1/status
    Kaggle->>Proxy: GET /api/v1/status
    Proxy-->>Kaggle: model_status == ready
  end
  Kaggle->>CF: Start Named Tunnel (TUNNEL_TOKEN)
  Kaggle->>Proxy: Smoke test POST /v1/chat/completions
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Env** | `TUNNEL_HOST`, `TUNNEL_PORT`, `TUNNEL_HOSTNAME`, `TUNNEL_TOKEN`, `LLM_API_KEY` | Network binding, Named Tunnel auth, Bearer auth |
| **Env** | `MODEL_NAME`, `HF_REPO_ID`, `VENV_DIR`, `MODELS_DIR` | Model ID and `/tmp/` isolation paths |
| **External Data** | `nanbingjun/<slug>-env-dataset`, `nanbingjun/<slug>-model` | Mounted `.env` and pre-published model weights |
| **External API** | Hugging Face Hub API (`/api/models/<repo>/tree/main`), Cloudflare Tunnel | Filename verification and HTTPS ingress |
| **Public API** | `GET /healthz`, `GET /api/v1/status`, `GET /v1/models`, `POST /v1/chat/completions` | Health, GPU/VRAM status, OpenAI-compatible inference |

## 4. Deliverables
- `<name>_kaggle.ipynb`, `kernel-metadata.json`, `.env`, `.env.example`, `http.rest`, `README.html`
- `kaggle_public_model/{download_model.py, model-metadata.json, model-instance-metadata.json, publish_kaggle_model.sh}`
- `kaggle_private_dataset/{dataset-metadata.json, prepare_dataset.py, publish_kaggle_dataset.sh}`
