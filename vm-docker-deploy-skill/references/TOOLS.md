# Tools & Interfaces Reference (`vm-docker-deploy`)

This document provides complete technical specifications, CLI interfaces, JSON schemas, and execution protocols for `vm-docker-deploy`.
Tools are strictly organized into four execution categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

Pre-built Python automation utilities located in `scripts/`. Agents should invoke these scripts instead of synthesizing ad-hoc shell commands.

| Command Script | Primary Role | CLI Invocation | Exit Codes |
|:---|:---|:---|:---|
| `inspect_compose.py` | Static YAML dependency analyzer | `python3 scripts/inspect_compose.py --compose <PATH> [--json]` | `0`: OK, `1`: Error |
| `deploy_compose.py` | Full deployment lifecycle pipeline | `python3 scripts/deploy_compose.py --compose <PATH> --vm <VM>` | `0`: Healthy, `1`: Error |
| `register_dns.py` | Dynamic Cloudflare DNS mapper | `python3 scripts/register_dns.py --vm <VM> --subdomain <NAME>` | `0`: Mapped, `1`: Error |
| `verify_vm.py` | Remote status & runtime inspector | `python3 scripts/verify_vm.py --vm <VM> [--remote-dir <DIR>]` | `0`: Running, `1`: Error |
| `teardown_vm.py` | Safe container stopper & cleaner | `python3 scripts/teardown_vm.py --vm <VM> --remote-dir <DIR>` | `0`: Removed, `1`: Error |

### 1.1 `inspect_compose.py`
- **Purpose**: Pre-flight inspection of Docker Compose YAML before remote execution.
- **CLI Options**:
  - `--compose <FILE>`: (Required) Local path to Docker Compose YAML.
  - `--json`: (Optional) Output structured JSON instead of human-readable text.
- **Output Schema**: Returns list of `services`, `volume_mounts`, `ports`, `env_files`, and highlights sensitive mounts (e.g. SSH keys).

### 1.2 `deploy_compose.py`
- **Purpose**: Provisions Docker Engine if missing, creates remote directory structure, syncs SSH keys (`chmod 600`), transfers compose file, starts stack, and polls health checks.
- **CLI Options**:
  - `--compose <FILE>`: (Required) Local Compose YAML path.
  - `--vm <NAME>`: (Required) Target GCE VM instance name.
  - `--project <PROJ>`: (Optional) GCP Project ID (defaults to active `gcloud` config).
  - `--zone <ZONE>`: (Optional) GCE zone (defaults to `us-central1-a`).
  - `--remote-dir <DIR>`: (Optional) Remote target path (defaults to `~/app/<service>`).
  - `--env-file <FILE>`: (Optional) Path to local `.env` file to upload.
  - `--ssh-key <PATH>`: (Optional) Local SSH private key (defaults to `~/.ssh/google_compute_engine`).
  - `--health-timeout <SEC>`: (Optional) Timeout for healthcheck loop (default: `120`).

### 1.3 `register_dns.py`
- **Purpose**: Retrieves VM external NAT IP and binds it as an A-Record via the `dns-worker` REST API.
- **CLI Options**:
  - `--vm <NAME>`: (Required) Target GCE VM name.
  - `--subdomain <NAME>`: (Required) Subdomain to register (e.g., `kline`).
  - `--zone <ZONE>`: (Optional) Cloudflare zone (default: `btczoa.app`).
  - `--proxied`: (Optional) Enable Cloudflare CDN proxy (default: `false` for direct SSH/Redis).
  - `--ttl <SEC>`: (Optional) DNS TTL (default: `300`).
  - `--dry-run`: (Optional) Validate payload and zone without creating.

### 1.4 `verify_vm.py`
- **Purpose**: Quick non-destructive check of Docker daemon and container status.
- **CLI Options**:
  - `--vm <NAME>`: (Required) Target VM name.
  - `--remote-dir <DIR>`: (Optional) Service directory to run `docker compose ps`.

### 1.5 `teardown_vm.py`
- **Purpose**: Graceful shutdown and cleanup of remote stacks.
- **CLI Options**:
  - `--vm <NAME>`: (Required) Target VM name.
  - `--remote-dir <DIR>`: (Required) Remote service directory.
  - `--volumes`: (Optional) Pass `-v` to remove declared volumes.
  - `--remove-dir`: (Optional) Delete the remote folder (`rm -rf`) after shutdown.

---

## 2. Shell コマンド (OS & Infrastructure)

Low-level infrastructure commands invoked via SSH or local bash environments.

| Shell Command / Pattern | Runtime Layer | Purpose | Key Flags & Parameters |
|:---|:---|:---|:---|
| `gcloud compute ssh` | Local -> Remote VM | Open remote shell & run command | `--zone=<z>`, `--project=<p>`, `--command="..."` |
| `gcloud compute scp` | Local -> Remote VM | Secure file transfer | `--zone=<z>`, `--project=<p>` |
| `gcloud compute instances describe` | Local -> GCP API | Retrieve instance metadata & NAT IP | `--format="get(networkInterfaces[0].accessConfigs[0].natIP)"` |
| `sudo docker compose up -d` | Remote VM | Start containerized services | `-d` (detached), `--build` (if rebuilding) |
| `sudo docker compose ps` | Remote VM | Check container health & status | `--format json` or plain table |
| `sudo docker compose logs` | Remote VM | Inspect service logs | `--tail=<n>`, `-f` |
| `sudo docker compose down` | Remote VM | Stop and destroy containers | `-v` (remove volumes) |
| `chmod 600 <key_file>` | Host / VM | Strict permission for private keys | `chmod 600 ~/.ssh/google_compute_engine` |
| `mkdir -p ~/.ssh && chmod 700 ~/.ssh` | Remote VM | Prepare secure SSH directory | Prevents `dest open: No such file` errors |

---

## 3. MCP ツール (Agent Primitives)

Antigravity Model Context Protocol (MCP) primitives utilized by the AI Agent to interact with the environment.

| MCP Primitive | Execution Role | Protocol Guidelines |
|:---|:---|:---|
| `run_command` | Execute `scripts/*.py` and shell utilities | Use `WaitMsBeforeAsync: 10000` for long tasks; monitor background tasks without busy polling. |
| `read_file` | Read Compose YAMLs, environment files, and logs | Always check dependencies before calling deployment scripts. |
| `write_file` / `edit_file` | Create or patch local Compose YAMLs and `.env` | Follow Rule.04 (temporary scripts in `<project-root>/tmp/src/`). |
| `manage_task` | Inspect status of long-running deployments | Use `status` on `task-<id>` when notified. |

---

## 4. 外部 API (External REST / RPC Services)

External network services interacted with during deployment and verification.

| Service / API | Protocol / Method | Endpoint / Resource | Authentication | Purpose |
|:---|:---|:---|:---|:---|
| `dns-worker` API | HTTP POST / GET | `https://dns.btczoa.app/dns` | `Authorization: Bearer <DNS_WORKER_API_KEY>` | Register, update, and inspect Cloudflare DNS A records. |
| Cloudflare DoH | HTTP GET (DNS-JSON) | `https://1.1.1.1/dns-query` | Public (No auth) | Verify global DNS resolution (`accept: application/dns-json`). |
| Cloud Resource Manager | Google Cloud RPC | `cloudresourcemanager.googleapis.com` | Google OAuth2 / ADC | Service enablement and project resource inspection. |
| Service Usage API | Google Cloud RPC | `serviceusage.googleapis.com` | Google OAuth2 / ADC | Quota project verification and API enablement. |
