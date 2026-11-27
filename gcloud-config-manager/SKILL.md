---
name: gcloud-config-manager
description: Automates and manages multi-account gcloud configurations syncing from .env or CLI without interactive prompts. Use when creating, switching, or auditing gcloud profiles. Do NOT use for provisioning GCP VMs (use gcp-free-tier-mesh) or Cloud Run deployment (use cloudrun-deploy).
---

# gcloud-config-manager

Deterministic multi-account Google Cloud CLI (`gcloud`) configuration manager and `.env` synchronizer.

## Core Principle: Code over Prompt

> [!IMPORTANT]
> `gcloud config set` often pauses waiting for interactive confirmation (`Do you want to continue (Y/n)?`) or throws authentication errors when an account hasn't completed local browser login.
> Use `scripts/manage_gcloud_configs.py` to deterministically create, inspect, and sync configurations from `.env` directly into `~/.config/gcloud/configurations/` without interactive interruptions.

## Operations (`scripts/`)

| Operation | Invocation | Purpose |
|:---|:---|:---|
| `sync-env` | `python3 scripts/manage_gcloud_configs.py sync-env --env-file /mnt/d/conf/.env` | Sync multi-account definitions from `.env` directly into gcloud configurations |
| `set` | `python3 scripts/manage_gcloud_configs.py set --name <name> --account <email> --project <id>` | Deterministically set or create a single gcloud configuration profile |
| `list` | `python3 scripts/manage_gcloud_configs.py list` | List all available gcloud configurations and their active status |
| `activate` | `python3 scripts/manage_gcloud_configs.py activate <name>` | Switch active gcloud configuration profile |

## Document Index & Criteria

| Document | Role | When to read |
|:---|:---|:---|
| **[prototype/PROTOTYPE.md](prototype/PROTOTYPE.md)** | Reusable configuration models & project boundaries | When adapting multi-account gcloud setups to another project |
| **[references/TOOLS.md](references/TOOLS.md)** | Detailed script specifications, CLI parameters & exit codes | When integrating `manage_gcloud_configs.py` into automated pipelines |
| **[references/ARCHITECTURE.md](references/ARCHITECTURE.md)** | Dual Logical & Infrastructure views, file locations & data flow | When understanding config storage topology and gcloud directory layouts |
| **[references/CHECKLIST.md](references/CHECKLIST.md)** | Acceptance checklist for configuration validation | When verifying profile completeness before running Terraform or deployment scripts |
| **[references/GUIDE.md](references/GUIDE.md)** | Step-by-step management and authentication guide | When adding new team accounts or logging into new GCP profiles |
| **[references/PREREQUISITES.md](references/PREREQUISITES.md)** | Required tools (`gcloud`, Python 3) & environment requirements | When bootstrapping a fresh workstation or VM |
| **[references/TRIGGERS.md](references/TRIGGERS.md)** | Positive/negative triggers and smoke testing commands | When assessing skill invocation accuracy |
| **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** | Common errors (interactive prompt hangs, unauthenticated accounts) | When encountering gcloud authorization or CLI freeze issues |

## Trigger & Exit Criteria
- **Trigger**: Requests to create, clone, update, switch, or sync multi-account `gcloud` profiles from `.env` or variables.
- **Exit Criteria**: `python3 scripts/manage_gcloud_configs.py list` verifies the requested profiles exist and reflect exact account/project pairings without hanging.

## Anti-Patterns
- **No Interactive `gcloud config set`**: Do not invoke `gcloud config set project` for unverified accounts in batch agent turns as it prompts `(Y/n)?` and halts.
- **No Manual Desynchronized Edits**: Avoid modifying INI files without updating `conf/.env`.
- **No Hardcoded Credentials**: Never store plain-text secrets or service account keys directly in `.env`.
