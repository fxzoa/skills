---
name: gcp-free-tier-mesh
description: Provisions multi-project GCP Always Free (e2-micro) VM meshes with star-topology VPC peering ($0.00 cross-project internal egress), cross-account billing linking, and <=3-container Docker Compose distribution. Use when building or operating multi-project Free Tier VM clusters with Terraform and Redis hub-and-spoke networking. Do NOT use for single-VM Compose deploys (use vm-docker-deploy) or Cloud Run deployments.
---

# gcp-free-tier-mesh

Orchestrate multi-project GCP Always Free (`e2-micro`) clusters connected via same-zone star-topology VPC Network Peering ($0.00 cross-project internal egress) and distributed `<= 3` container-per-VM Docker Compose workloads.

## Operations (`scripts/`)

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `link_billing` | `python3 scripts/link_billing.py --pair <email>:<proj> [...]` | Link open Billing Accounts (supports cross-account fallback). | [TOOLS.md](references/TOOLS.md) |
| `apply_tf_tokens` | `python3 scripts/apply_tf_tokens.py --tf-dir <dir> --node <k>:<email> --action apply` | Run multi-account Terraform with per-project OAuth2 tokens. | [TOOLS.md](references/TOOLS.md) |
| `package_images` | `python3 scripts/package_images.py --bundle <name>=<imgs> --out-dir <dir>` | Export & gzip local Docker images without registry push. | [TOOLS.md](references/TOOLS.md) |
| `deploy_mesh` | `python3 scripts/deploy_mesh.py --compose <yml> --vm <vm> --project <p> --account <e>` | Setup 1 GB Swap, data perms, `.env`, image load, and `deploy_compose.py`. | [TOOLS.md](references/TOOLS.md) |
| `verify_mesh` | `python3 scripts/verify_mesh.py --node "<acc>\|<vm>\|<proj>\|<stack>" [...]` | Verify `ACTIVE` VPC peerings, `free -m`, `ps`, and logs. | [TOOLS.md](references/TOOLS.md) |
| `sync_env_secret` | `python3 scripts/sync_env_secret.py --src <master.env> --dst <target.env> --key <KEY>` | Safely sync non-empty secret keys without printing values. | [TOOLS.md](references/TOOLS.md) |

## Document Index

| Document | Role |
|:---|:---|
| [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) | Reusable core design vs. project-specific replacements (`templates/`) |
| [references/ARCHITECTURE.md](references/ARCHITECTURE.md) | Star-topology VPC peering & provisioning sequence diagrams |
| [references/GUIDE.md](references/GUIDE.md) | End-to-end 6-step provisioning & deployment workflow |
| [references/TOOLS.md](references/TOOLS.md) | 4-category tool specification (`Command`, `Shell`, `MCP`, `外部 API`) |
| [references/PREREQUISITES.md](references/PREREQUISITES.md) | Required CLIs, accounts, billing, and Always Free constraints |
| [references/CHECKLIST.md](references/CHECKLIST.md) | Acceptance criteria for mesh health and memory headroom |
| [references/TRIGGERS.md](references/TRIGGERS.md) | Positive/Negative triggers and CLI smoke tests |
| [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) | Field-tested fixes for 10 multi-project / `e2-micro` issues |

## Trigger & Exit Criteria
- **Trigger**: Building or operating multi-project GCP Always Free VM clusters with VPC peering and distributed Docker Compose stacks.
- **Exit Criteria**: All projects billing-enabled, all VPC peerings `ACTIVE`, all VMs running `<= 3` containers within ~30–35% RAM (`free -m`), and `verify_mesh.py` exits `0`.

## Anti-Patterns
- Never use `source_tags` for cross-VPC peering firewalls (tags do not cross VPC boundaries; use CIDR `source_ranges`).
- Never create hub-and-spoke `google_compute_network_peering` resources in parallel (chain all pairs sequentially with `depends_on`).
- Never run `docker compose build` or > 3 Deno containers on `e2-micro` (pre-package with `package_images.py` and set `DENO_V8_FLAGS=--max-old-space-size=96`).
- Never run `chmod -R 777` over existing Deno KV SQLite directories owned by UID 1000 (`chmod 777` only newly created service data subdirs).
- Never leave `allow_ssh` / `allow_icmp` `source_ranges` open to `0.0.0.0/0` in production; restrict external SSH/ICMP to the operator CIDR (e.g., `60.71.0.0/16`). Internal VPC-peered traffic remains permitted via `allow_internal`.
- Keep each GCP account's billing independent unless cross-account fallback linking is explicitly requested.
