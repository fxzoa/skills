# cloudrun-deploy: Prerequisites & Requirements

## Runtime Requirements
- **Python:** 3.9+ (Standard library only; no external pip requirements needed)
- **Google Cloud SDK (`gcloud`):** Version 400.0.0+ installed at `/snap/bin/gcloud` or in PATH.
- **Docker:** Optional (Cloud Build builds remotely on GCP infrastructure).

## GCP Account & IAM Requirements
The active account under the specified configuration (e.g. `nanzhiyan@gmail.com`) must possess:
- `roles/owner` or `roles/editor` OR the following granular roles:
  - `roles/run.admin`
  - `roles/artifactregistry.admin`
  - `roles/cloudbuild.builds.editor`
  - `roles/resourcemanager.projectIamAdmin` (to grant Cloud Build service account permissions)
  - `roles/serviceusage.serviceUsageAdmin` (to enable required APIs)
