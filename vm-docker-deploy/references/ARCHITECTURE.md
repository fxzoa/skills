# Architecture & Specifications (`vm-docker-deploy`)

## 1. Architecture Diagram
```mermaid
flowchart TD
  LocalYaml["Docker Compose YAML<br>(Input)"] --> Inspect["scripts/inspect_compose.py"]
  Inspect --> Deploy["scripts/deploy_compose.py"]
  
  subgraph GCE_VM["Google Cloud VM (e2-micro / Ubuntu)"]
    DockerEngine["Docker Engine & Compose Plugin"]
    SSHConfig["~/.ssh/google_compute_engine<br>(600 perms)"]
    AppDir["~/app/<service>/<br>├── docker-compose.yml<br>└── .env"]
    Containers["Docker Containers<br>(redis-tunnel, collector, bot)"]
    
    DockerEngine --> Containers
    SSHConfig --> Containers
    AppDir --> Containers
  end

  Deploy -- "1. Auto-install Docker" --> DockerEngine
  Deploy -- "2. Sync SSH Key & perms" --> SSHConfig
  Deploy -- "3. Upload Compose & .env" --> AppDir
  Deploy -- "4. docker compose up -d" --> DockerEngine
  Deploy -- "5. Healthcheck loop" --> Containers

  Deploy -. "External IP" .-> DNS["scripts/register_dns.py"]
  DNS -- "POST /dns" --> Cloudflare["Cloudflare (dns.btczoa.app)<br>kline.btczoa.app -> IP"]
  
  Verify["scripts/verify_vm.py"] -. "Status" .-> Containers
  Teardown["scripts/teardown_vm.py"] -. "down -v" .-> DockerEngine
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
  autonumber
  actor Operator as User / Agent
  participant Inspect as inspect_compose.py
  participant Deploy as deploy_compose.py
  participant GCE as Remote VM (gcloud SSH/SCP)
  participant DNS as register_dns.py
  participant CF as Cloudflare DNS Worker

  Operator->>Inspect: Check YAML dependencies
  Inspect-->>Operator: Volume mounts & ports verified
  Operator->>Deploy: Execute deployment
  Deploy->>GCE: Check & install Docker Engine
  Deploy->>GCE: Prepare ~/.ssh (700) and sync SSH private key (600)
  Deploy->>GCE: Transfer docker-compose.yml & .env
  Deploy->>GCE: sudo docker compose down && docker compose up -d
  loop Health Polling
    Deploy->>GCE: docker compose ps --format json
  end
  Deploy-->>Operator: Stack Healthy & Operational
  opt DNS Mapping
    Operator->>DNS: Register subdomain (e.g. kline)
    DNS->>GCE: Retrieve external NAT IP
    DNS->>CF: POST /dns (Authorization: Bearer KEY)
    CF-->>DNS: HTTP 200/201 (A Record Registered)
    DNS-->>Operator: DNS Mapped (FQDN -> IP)
  end
```

## 3. Environment Variables, External Data & APIs
| Category | Name | Purpose |
|:---|:---|:---|
| **CLI** | `gcloud` | Google Cloud CLI for transport (`ssh`, `scp`) and metadata query |
| **Auth** | `DNS_WORKER_API_KEY` | Read from `/mnt/d/.env.nan` for Cloudflare DNS registration |
| **API** | `https://dns.btczoa.app/dns` | REST endpoint for DNS A record management |
| **Auth** | `~/.ssh/google_compute_engine` | SSH private key used by containers for tunneling or host access |
| **Env** | `REDIS_SSH_KEY_PATH` | Host path mapped into containers (default: `~/.ssh/google_compute_engine`) |

## 4. Deliverables
- Fully running Docker container stack on target VM.
- Persistent configuration under `~/app/<service>/docker-compose.yml`.
- Standardized verification logs, health checks, and optional DNS A record.
