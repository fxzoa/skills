# Architecture & Specifications (`colab-notebook`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  Client[External Client] -->|HTTPS| CF[Cloudflare Tunnel]
  CF -->|HTTP 127.0.0.1:8000| Uvicorn[FastAPI server.py]
  Uvicorn -->|In-Process / Subprocess| Engine[Inference Engine / llama.cpp]
  Env[External .env /content/.env] -.-> Uvicorn
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant NB as Colab Notebook
  participant Env as External .env
  participant FastAPI as Uvicorn (:8000)
  participant CF as cloudflared

  NB->>Env: Validate required keys (Rule.13)
  NB->>NB: Setup uv venv (/tmp/.venv) & %%writefile modules
  NB->>FastAPI: Launch Uvicorn background process
  loop Poll /api/v1/status
    NB->>FastAPI: GET /api/v1/status
    FastAPI-->>NB: ready
  end
  NB->>CF: Start Tunnel -> print public URL
  NB->>FastAPI: Test /v1/chat/completions & tail logs
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Env** | `TUNNEL_HOST`, `TUNNEL_PORT`, `TUNNEL_HOSTNAME`, `LLM_API_KEY`, `MODEL_NAME` | Server binding, Tunnel host, auth, model ID |
| **External Data** | `/content/.env`, Hugging Face model weights | External secrets and downloaded weights |
| **Public API** | `GET /healthz`, `GET /api/v1/status`, `GET /v1/models`, `POST /v1/chat/completions` | Health, status, OpenAI-compatible inference |

## 4. Deliverables
- `<name>_colab.ipynb`, `.env`, `.env.example`, `http.rest`, `README.html`
- Generated runtime modules (`core/{config,logger,state,engine}.py`, `routers/{health,status,chat,models}.py`, `server.py`)
