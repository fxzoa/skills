# Architecture & Specifications (`kaggle-app-hosting`)

## 1. Architecture Diagram
```mermaid
flowchart LR
  User[Web User] -->|HTTPS| CF[Cloudflare Tunnel]
  CF -->|HTTP 127.0.0.1:PORT| App[WebUI / App Process]
  App -->|Read/Write| DB[(SQLite /data/app.db)]
  Sync[sync_dataset.py] -->|sqlite3.backup + zip| DS[Kaggle Private Dataset -dataset]
  DS -.->|Restore on Boot| DB
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  participant NB as Kaggle CPU Notebook
  participant DS as Private Dataset
  participant App as App & Worker
  participant Sync as sync_dataset.py
  participant CF as cloudflared

  NB->>DS: Load .env & restore SQLite DB
  NB->>App: start_services.sh (nohup)
  NB->>App: healthcheck.py (127.0.0.1:PORT/health)
  NB->>CF: Start Named/Quick Tunnel
  loop Every 1 hour (+60s initial)
    Sync->>DS: sqlite3.backup() -> kaggle datasets version
  end
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **Env** | `TUNNEL_MODE`, `TUNNEL_HOST`, `TUNNEL_PORT`, `TUNNEL_HOSTNAME`, `TUNNEL_TOKEN` | Tunnel mode and binding |
| **Env** | `APP_REPO_URL`, `DB_PATH`, `DATASET_ID`, `KAGGLE_API_TOKEN` | App source, DB path, Private Dataset sync auth |
| **External Data** | Kaggle Private Dataset (`-dataset`), GitHub Public Repo | Persistent `.env`/DB and app source |
| **External API** | Kaggle Datasets API (`version -r zip`), Cloudflare Tunnel | Hourly backup and HTTPS ingress |

## 4. Deliverables
- `<app>_kaggle.ipynb`, `kernel-metadata.json`, `.env`, `.env.example`, `http.rest`, `README.html`
- `kaggle_private_dataset/{dataset-metadata.json, prepare_dataset.py, publish_kaggle_dataset.sh}`
