# setup-run-crawl4ai: Architecture & Specifications

## 1. Architecture Diagram

```mermaid
flowchart TD
    User["Agent / Developer / Batch Script"] -->|Invokes 1-Click Setup| Setup["setup_crawl4ai.py"]
    Setup -->|Generates 32-byte Token| Token["secrets.token_hex(32)"]
    Setup -->|Writes/Updates| EnvFile[".env (e.g. /mnt/d/conf/.env)"]
    Setup -->|Spawns with shm-size=1g| Docker["Docker Container (crawl4ai)"]
    
    subgraph Container["Local Docker Engine (Port 11235)"]
        API["FastAPI Server (Port 11235)"]
        Playwright["Playwright Chromium Browser (Headless)"]
        API --> Playwright
    end

    Docker --> API
    Setup -->|Polls GET /health| API
    
    Verify["verify_crawl4ai.py / crawl_url.py"] -->|POST /crawl with Bearer Token| API
    Playwright -->|Scrapes & Cleans DOM| Web["Target Web Sites"]
```

## 2. Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / Agent
    participant Script as setup_crawl4ai.py
    participant Docker as Docker Daemon
    participant Container as crawl4ai Container
    participant Env as .env File

    Dev->>Script: python3 setup_crawl4ai.py --env-file /conf/.env
    Script->>Script: Check port 11235 & generate token
    Script->>Docker: docker run -d --name crawl4ai -p 11235:11235 --shm-size=1g
    Docker->>Container: Start container process
    loop Health Check (timeout 60s)
        Script->>Container: GET /health
        Container-->>Script: 200 OK {"status": "ok"}
    end
    Script->>Env: Append CRAWL4AI_BASE_URL & CRAWL4AI_API_TOKEN
    Script-->>Dev: [SUCCESS] Ready to use
```

## 3. Environment Variables & Deliverables

| Key | Purpose | Example |
|:---|:---|:---|
| `CRAWL4AI_BASE_URL` | Local container HTTP URL | `http://127.0.0.1:11235` |
| `CRAWL4AI_API_TOKEN` | Bearer authentication token | `027cbf51f3fe...` |
| `CRAWL4AI_PORT` | Host binding port | `11235` |
