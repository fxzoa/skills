# cloudrun-deploy: Architecture & Technical Specification

## 1. System Architecture Diagram

```mermaid
flowchart TD
    User["User / Developer"] -->|Specifies --configuration| Inspect["inspect_gcloud_config.py"]
    Inspect -->|Resolves Project ID & Region| Provision["provision_apis_and_repo.py"]
    
    subgraph GCP["Google Cloud Platform (User Project)"]
        APIs["Cloud Run / Cloud Build / Artifact Registry APIs"]
        Repo["Artifact Registry (Docker Repo)"]
        CB["Cloud Build Service Account (roles/run.admin)"]
        CR["Cloud Run (All-in-One Service)"]
        
        Provision -->|Enables APIs & Creates Repo| APIs
        Provision -->|Creates Repo| Repo
        Provision -->|Grants IAM Roles| CB
        
        Deploy["deploy_cloudrun.py"] -->|Submits Build| CB
        CB -->|Builds & Pushes| Repo
        CB -->|Deploys Image| CR
    end

    Deploy --> Verify["verify_cloudrun.py"]
    Verify -->|HTTP GET /api/health| CR
```

## 2. Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as User / Agent
    participant Tool as cloudrun-deploy scripts
    participant GCP as Google Cloud Platform
    participant CR as Cloud Run Service

    Dev->>Tool: inspect_gcloud_config.py --configuration=nanzhiyan
    Tool-->>Dev: Project ID: ai-test-001-515719, Region: asia-northeast1

    Dev->>Tool: provision_apis_and_repo.py -c nanzhiyan
    Tool->>GCP: Enable APIs & Ensure Artifact Registry
    Tool->>GCP: Bind roles/run.admin to Cloud Build SA
    GCP-->>Tool: Provisioning Complete

    Dev->>Tool: deploy_cloudrun.py -c nanzhiyan --service=coin-trade-all-in-one
    Tool->>GCP: gcloud builds submit
    GCP->>CR: Deploy Container Revision (gen2, cpu-throttling: false)
    CR-->>GCP: Ready: True, URL: https://coin-trade-all-in-one-*.run.app
    GCP-->>Tool: Deployment Succeeded

    Dev->>Tool: verify_cloudrun.py -c nanzhiyan -s coin-trade-all-in-one
    Tool->>CR: HTTP GET /api/health
    CR-->>Tool: 200 OK (status: healthy)
    Tool-->>Dev: [SUCCESS] Verified
```

## 3. Required Environment & Deliverables

| Key | Description | Default |
|:---|:---|:---|
| `GCP_PROJECT_ID` | Google Cloud Project ID | Auto-resolved from `gcloud config` |
| `GCP_REGION` | Cloud Run / Artifact Registry region | `asia-northeast1` |
| `SERVICE_NAME` | Cloud Run service name | `coin-trade-all-in-one` |
| `ARTIFACT_REPO` | Artifact Registry repo name | `coin-trade-repo` |
