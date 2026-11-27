# Tools & Interfaces Reference (`gcp-free-tier-mesh`)

Tools are organized into four categories: **Command**, **Shell**, **MCP**, and **外部 API**.

---

## 1. Command ツール (Python CLI / `scripts/`)

| Script | Role | Invocation | Exit Codes |
|:---|:---|:---|:---|
| `link_billing.py` | Multi-project & cross-account Billing Account linker | `python3 scripts/link_billing.py --pair <email>:<proj> [--fallback-owner <e> --fallback-billing-id <id>]` | `0`: Linked, `1`: Error |
| `apply_tf_tokens.py` | Multi-account OAuth2 token injector for Terraform | `python3 scripts/apply_tf_tokens.py --tf-dir <dir> --node <key>:<email> --action plan\|apply\|output [--auto-approve]` | `0`: OK, non-zero: TF error |
| `package_images.py` | Export & gzip local Docker images | `python3 scripts/package_images.py --bundle <name>=<img1>,<img2> --out-dir <dir>` | `0`: Exported, `1`: Error |
| `deploy_mesh.py` | Swap, `.env`, image load, and `deploy_compose.py` wrapper | `python3 scripts/deploy_mesh.py --compose <yml> --vm <vm> --project <p> --account <e> [--tar <gz>] [--env-map <l>:<r>] [--data-dir <d>]` | `0`: Healthy, non-zero: Error |
| `verify_mesh.py` | Verify peerings, `free -m`, `docker compose ps`, and logs | `python3 scripts/verify_mesh.py --node "<acc>\|<vm>\|<proj>\|<stack>" [--hub-account <a> --hub-project <p>]` | `0`: Verified, `1`: Error |
| `sync_env_secret.py` | Secret-safe `.env` key sync without printing values | `python3 scripts/sync_env_secret.py --src <master.env> --dst <target.env> --key <KEY>` | `0`: Synced, `1`: Missing/Empty |

---

## 2. Shell コマンド (OS & Infrastructure)

| Command | Layer | Purpose |
|:---|:---|:---|
| `gcloud auth login <email>` | Host CLI | Authenticate missing Google accounts prior to `link_billing.py` / `apply_tf_tokens.py`. |
| `gcloud compute networks peerings list` | GCP API | Confirm all hub-to-spoke peerings reach `STATE: ACTIVE`. |
| `sudo docker compose up -d --force-recreate <svc>` | Remote VM | Recreate a container after updating `./env/<svc>.env` (`restart` alone does not reload `env_file`). |
| `free -m` | Remote VM | Verify `e2-micro` RAM (~300–350 MB used) and Swap (1 GB) headroom. |

---

## 3. MCP ツール (Agent Primitives)

| Primitive | Role | Guidelines |
|:---|:---|:---|
| `run_command` | Execute `scripts/*.py`, `terraform`, and `gcloud` | Use `BypassSandbox: true` for `gcloud`/`terraform`/`docker`; use `WaitMsBeforeAsync: 10000` for long tasks. |
| `read_file` / `write_file` / `edit_file` | Manage `.tf`, Compose YAMLs, and docs | Never print secret `.env` values to stdout. |
| `manage_task` | Monitor background Terraform / SCP / Docker tasks | Use `status` only when notified or inspecting progress. |

---

## 4. 外部 API (External Services)

| Service / API | Protocol | Purpose |
|:---|:---|:---|
| Cloud Billing API (`cloudbilling.googleapis.com`) | RPC / REST | Link Billing Accounts across projects (`roles/billing.projectManager`). |
| Compute Engine API (`compute.googleapis.com`) | RPC / REST | Provision `e2-micro` VMs, custom VPCs, CIDR firewalls, and VPC Network Peering. |
| Service Usage & Resource Manager APIs | RPC / REST | Enable required GCP APIs per project. |
