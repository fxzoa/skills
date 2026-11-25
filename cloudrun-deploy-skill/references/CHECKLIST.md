# cloudrun-deploy: Acceptance Checklist

## Pre-Flight Checks
- [ ] `gcloud` CLI executable is present in PATH (`/snap/bin/gcloud` or standard path).
- [ ] User has authenticated the target configuration (`gcloud auth login`).
- [ ] Target configuration exists (`gcloud config configurations list`).

## Execution & Script Validation
- [ ] `scripts/inspect_gcloud_config.py --configuration <cfg>` prints valid Project ID.
- [ ] `scripts/provision_apis_and_repo.py --configuration <cfg>` successfully completes:
  - [ ] `run.googleapis.com` enabled
  - [ ] `cloudbuild.googleapis.com` enabled
  - [ ] `artifactregistry.googleapis.com` enabled
  - [ ] Docker repository created in Artifact Registry
  - [ ] Cloud Build service account has `roles/run.admin`
- [ ] `scripts/deploy_cloudrun.py --configuration <cfg>` builds and deploys service without errors.
- [ ] `scripts/verify_cloudrun.py --configuration <cfg>` returns HTTP 200 and Ready condition `True`.

## Security & Reliability Guardrails
- [ ] CPU Throttling is disabled (`cpu-throttling: false`) for continuous background bot execution.
- [ ] Max instances is constrained (`maxScale: 1`) to eliminate double-order risks.
- [ ] Gen2 execution environment is activated.
