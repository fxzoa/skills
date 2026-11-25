---
name: vm-docker-deploy
description: Deploys, inspects, verifies, and tears down Docker Compose workloads on cloud VMs (GCE/Linux) with automated Docker provisioning, SSH key/env syncing, health checks, and Cloudflare DNS registration. Use when deploying or managing Docker Compose stacks on remote VMs. Do NOT use for local-only Crawl4AI setup or Kaggle notebook deployments.
---

# vm-docker-deploy

Deploy, configure, verify, and manage containerized workloads defined in Docker Compose YAML onto cloud VMs (such as Google Compute Engine instances).

## Pre-Built Operations (`scripts/`)

> [!NOTE]
> Detailed CLI flags, schemas, exit codes, and agent execution protocols are documented in [references/TOOLS.md](references/TOOLS.md).

| Operation | Invocation | Purpose | Reference |
|:---|:---|:---|:---|
| `inspect_compose` | `python3 scripts/inspect_compose.py --compose <file> [--json]` | Statically analyzes YAML for volume mounts, SSH keys, ports, and env dependencies. | [TOOLS.md#21](references/TOOLS.md#21-inspect_composepy) |
| `deploy_compose` | `python3 scripts/deploy_compose.py --compose <file> --vm <vm> [--project <p>] [--zone <z>]` | Provisions Docker (if missing), syncs keys/env, deploys Compose stack, and checks health. | [TOOLS.md#22](references/TOOLS.md#22-deploy_composepy) |
| `register_dns` | `python3 scripts/register_dns.py --vm <vm> --subdomain <sub> [--zone <z>]` | Discovers VM external IP and registers Cloudflare DNS A record via `dns-worker` API. | [TOOLS.md#23](references/TOOLS.md#23-register_dnspy) |
| `verify_vm` | `python3 scripts/verify_vm.py --vm <vm> [--remote-dir <dir>]` | Checks Docker daemon and container status on the target VM. | [TOOLS.md#24](references/TOOLS.md#24-verify_vmpy) |
| `teardown_vm` | `python3 scripts/teardown_vm.py --vm <vm> --remote-dir <dir> [--volumes]` | Stops containers, cleans up volumes, and removes remote service directories. | [TOOLS.md#25](references/TOOLS.md#25-teardown_vmpy) |

## Document Index
| Document | Purpose |
|:---|:---|
| [prototype/PROTOTYPE.md](prototype/PROTOTYPE.md) | Reusable core design vs. project-specific replacements |
| [references/TOOLS.md](references/TOOLS.md) | CLI flags, schemas, and exit codes for `scripts/` |
| [references/ARCHITECTURE.md](references/ARCHITECTURE.md) | VM provisioning, SSH sync, and DNS architecture |
| [references/CHECKLIST.md](references/CHECKLIST.md) | Deployment & post-deploy verification checklist |
| [references/GUIDE.md](references/GUIDE.md) | Step-by-step VM Docker Compose deployment guide |
| [references/PREREQUISITES.md](references/PREREQUISITES.md) | `gcloud`, SSH keys, and Cloudflare worker prerequisites |
| [references/TRIGGERS.md](references/TRIGGERS.md) | Positive/negative trigger examples and smoke tests |
| [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) | Fixes for volume mount dir issues, SSH perms, and health failures |

## Workflow Calls
1. `inspect_compose(--compose)` → pre-flight check of volume mounts and dependencies.
2. `deploy_compose(--compose, --vm, --project, --zone)` → complete automated deployment pipeline.
3. `register_dns(--vm, --subdomain, --zone)` → bind external IP to DNS record.
4. `verify_vm(--vm, --remote-dir)` → inspect container statuses and logs.
5. `teardown_vm(--vm, --remote-dir)` → safely stop and destroy remote stack.

## Trigger & Exit Criteria
- **Trigger**: When the user requests deploying, inspecting, DNS-mapping, or managing a Docker Compose YAML on a cloud VM.
- **Exit Criteria**: `scripts/deploy_compose.py` completes with exit code `0`, containers reach `healthy` or `running` state, and DNS resolution passes.

## Anti-Patterns
- Never run `docker compose up` before ensuring that host files referenced in volume mounts already exist (prevents Docker from auto-creating empty directories).
- Never scp to `~/.ssh/` before confirming the remote `~/.ssh` directory exists with `chmod 700`.
- Never leave SSH private keys with world-readable permissions (`chmod 600` is mandatory).
- Never ignore container health checks or exit without verifying logs.
