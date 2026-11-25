# cloudrun-deploy: Operation Guide

## Overview
This guide provides the standard step-by-step procedure to deploy and operate containerized applications to GCP Cloud Run using named `gcloud` configurations.

---

## Step 1: Inspect Target Configuration
Confirm that the requested configuration (e.g., `nanzhiyan`) points to the desired GCP project:
```bash
python3 scripts/inspect_gcloud_config.py --configuration nanzhiyan
```

## Step 2: Provision APIs and Repository
Run the deterministic provisioner to ensure APIs, Artifact Registry, and IAM permissions are configured:
```bash
python3 scripts/provision_apis_and_repo.py --configuration nanzhiyan --region asia-northeast1 --repo coin-trade-repo
```

## Step 3: Trigger Build and Deployment
Deploy the service using the repository's `cloudbuild.yaml`:
```bash
cd /mnt/d/coin-trade-kaggle
python3 /mnt/d/skills/cloudrun-deploy-skill/scripts/deploy_cloudrun.py \
  --configuration nanzhiyan \
  --service coin-trade-all-in-one \
  --config-file deploy/cloudrun/cloudbuild.yaml
```

## Step 4: Verify Deployment Health
Verify the service readiness and HTTP endpoint:
```bash
python3 /mnt/d/skills/cloudrun-deploy-skill/scripts/verify_cloudrun.py \
  --configuration nanzhiyan \
  --service coin-trade-all-in-one \
  --path /api/health
```
