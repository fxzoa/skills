# cloudrun-deploy: Tool Interface Specifications

Tools and execution boundaries are classified into four formal operational domains:
`Command`, `Shell`, `MCP`, and `外部 API`.

---

## 1. Tool Categories

### 1.1 Command
Deterministic local Python tools implemented in `scripts/`:
- `scripts/run_full_deployment.py`
- `scripts/inspect_gcloud_config.py`
- `scripts/provision_apis_and_repo.py`
- `scripts/deploy_cloudrun.py`
- `scripts/verify_cloudrun.py`

### 1.2 Shell
Standard command-line utilities executed through subprocess or interactive terminal:
- `/snap/bin/gcloud` or `gcloud`
- `curl`
- `docker` (optional when Cloud Build is used)

### 1.3 MCP
Model Context Protocol integrations (if configured):
- `gcp-mcp-server` (resource browsing, log queries)

### 1.4 外部 API
Cloud and DEX REST/RPC interfaces:
- `https://run.googleapis.com` (Cloud Run Admin API)
- `https://cloudbuild.googleapis.com` (Cloud Build API)
- `https://artifactregistry.googleapis.com` (Artifact Registry API)
- `https://api.hyperliquid.xyz` (Target application DEX upstream)

---

## 2. Pre-Built Operations Specification

### 2.1 `run_full_deployment.py`
- **CLI Options:**
  - `--configuration, -c`: Name of gcloud configuration profile.
  - `--project, -p`: Project ID override.
  - `--region, -r`: GCP region (default: `asia-northeast1`).
  - `--service, -s`: Service name (default: `coin-trade-all-in-one`).
  - `--repo`: Target Artifact Registry repository name (default: `coin-trade-repo`).
  - `--config-file`: Path to `cloudbuild.yaml`.
  - `--path`: HTTP health probe path (default: `/api/health`).
- **Exit Codes:**
  - `0`: All 4 pipeline steps succeeded and service is healthy.
  - `1`: Any step failed.

### 2.2 `inspect_gcloud_config.py`
- **CLI Options:**
  - `--configuration, -c`: Name of gcloud configuration profile.
  - `--json`: Output as raw JSON dictionary.
- **Exit Codes:**
  - `0`: Valid profile and active project resolved.
  - `1`: Configuration error or missing gcloud executable.

### 2.3 `provision_apis_and_repo.py`
- **CLI Options:**
  - `--configuration, -c`: Profile name.
  - `--project, -p`: Project ID override.
  - `--region, -r`: GCP region (default: `asia-northeast1`).
  - `--repo`: Target Artifact Registry repository name (default: `coin-trade-repo`).
- **Exit Codes:**
  - `0`: APIs enabled, repo confirmed/created, IAM verified.
  - `1`: Permission denied or service error.

### 2.4 `deploy_cloudrun.py`
- **CLI Options:**
  - `--configuration, -c`: Profile name.
  - `--service, -s`: Service name (default: `coin-trade-all-in-one`).
  - `--config-file`: Cloud Build config YAML path.
  - `--source-dir`: Directory containing context files to upload.
  - `--allow-unauthenticated`: Bind `roles/run.invoker` to `allUsers`.
- **Exit Codes:**
  - `0`: Build finished and Cloud Run revision deployed.
  - `>0`: Build step failure or deployment error.

### 2.5 `verify_cloudrun.py`
- **CLI Options:**
  - `--service, -s`: Cloud Run service name.
  - `--configuration, -c`: Profile name.
  - `--path`: HTTP probe path (default: `/api/health`).
- **Exit Codes:**
  - `0`: Ready state True and HTTP status 200.
  - `1`: Not ready or probe failed.
