# Prototype: Multi-Account gcloud Configuration Model

## Reusable Assets
- `scripts/manage_gcloud_configs.py`: Generic Python script capable of reading any `.env` file adhering to standard prefix `GCP_CONFIG_<NODE>_*`.
- Standard Configuration INI format under `~/.config/gcloud/configurations/config_<name>`.

## Project-Specific Customization Points
1. **Target `.env` file path**: Defaults to `/mnt/d/conf/.env`, but can be pointed to any repository root `.env`.
2. **Account email & Project IDs**: Specific to tenant credentials (e.g. `btczoa`, `nanbjbank`, `fxzoa2020`).
3. **Default Compute Zone / Region**: Defaults to `us-central1-a` / `us-central1`, customizable via `GCP_DEFAULT_ZONE` and `GCP_DEFAULT_REGION`.
