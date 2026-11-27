# Prerequisites (`gcp-free-tier-mesh`)

1. **CLI Tools**: `gcloud`, `terraform` (>= 1.5.0), `docker`, `python3` (>= 3.10).
2. **Companion Skill**: `vm-docker-deploy` installed at `/home/ppbb/.gemini/antigravity-cli/skills/vm-docker-deploy`.
3. **GCP Accounts**: All target Google accounts authenticated via `gcloud auth login`.
4. **Billing**: At least one active (`OPEN = True`) GCP Billing Account available (can be shared cross-account via `roles/billing.projectManager`).
5. **Region / Zone Policy**: All Always Free `e2-micro` VMs placed in the **same US Always Free zone** (e.g., `us-central1-a`) with `pd-standard` (<= 30 GB) and `STANDARD` network tier.
