# setup-run-crawl4ai: Tool Interface Specifications

Tools and execution boundaries are classified into four formal operational domains:
`Command`, `Shell`, `MCP`, and `外部 API`.

---

## 1. Tool Categories

### 1.1 Command
Deterministic local Python tools implemented in `scripts/`:
- `scripts/setup_crawl4ai.py`
- `scripts/verify_crawl4ai.py`
- `scripts/crawl_url.py`

### 1.2 Shell
Standard command-line utilities executed through subprocess:
- `docker`
- `curl`

### 1.3 MCP
Model Context Protocol integrations (if configured):
- `mcp-server-docker` (container lifecycle)

### 1.4 外部 API
Web endpoints and local container REST APIs:
- `http://127.0.0.1:11235/health` (Container Health Check)
- `http://127.0.0.1:11235/crawl` (POST Scrape API)

---

## 2. Pre-Built Operations Specification

### 2.1 `setup_crawl4ai.py`
- **CLI Options:**
  - `--port`: Host port to bind (default: `11235`).
  - `--token`: API token override (generated via secrets if omitted).
  - `--env-file`: Target `.env` file path for persistent credentials.
  - `--force-recreate`: Force delete and re-create container.
- **Exit Codes:**
  - `0`: Container successfully running, healthy, and `.env` updated.
  - `1`: Docker daemon missing, port conflict, or timeout.

### 2.2 `verify_crawl4ai.py`
- **CLI Options:**
  - `--base-url`: Crawl4AI URL (default: `http://127.0.0.1:11235`).
  - `--token`: API Token override.
  - `--env-file`: Source `.env` file to read credentials from.
  - `--test-url`: Target URL for test scrape (default: `https://example.com`).
- **Exit Codes:**
  - `0`: Health OK and test scrape returned valid HTML.
  - `1`: Connection refused, 401 unauthorized, or scrape failed.

### 2.3 `crawl_url.py`
- **CLI Options:**
  - `url`: Target URL to scrape (positional).
  - `--format`: `markdown`, `html`, or `json` (default: `markdown`).
  - `--output, -o`: Save result to file.
- **Exit Codes:**
  - `0`: Scraping succeeded and content outputted.
  - `1`: API error.
