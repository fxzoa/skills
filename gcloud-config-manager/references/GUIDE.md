# Step-by-Step Guide

## 1. Sync from `.env`
To configure all multi-account profiles defined in `/mnt/d/conf/.env`:
```bash
python3 scripts/manage_gcloud_configs.py sync-env --env-file /mnt/d/conf/.env
```

## 2. Set Single Profile
To create or update a specific configuration profile:
```bash
python3 scripts/manage_gcloud_configs.py set \
  --name myprofile \
  --account myaccount@gmail.com \
  --project my-gcp-project \
  --zone us-central1-a \
  --region us-central1
```

## 3. Switch Profile
To switch between configurations:
```bash
python3 scripts/manage_gcloud_configs.py activate nanbjbank
```

## 4. Authenticate Profile (If Required)
When using a newly registered account profile for the first time:
```bash
gcloud auth login <account_email>
```
