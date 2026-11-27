# Acceptance Checklist

- [ ] `gcloud` CLI is installed and available in `$PATH`.
- [ ] Python 3.8+ is installed.
- [ ] `scripts/manage_gcloud_configs.py` is executable (`chmod +x`).
- [ ] Target `.env` contains valid `GCP_CONFIG_<NAME>_ACCOUNT` and `GCP_CONFIG_<NAME>_PROJECT`.
- [ ] Running `python3 scripts/manage_gcloud_configs.py list` prints all expected configuration profiles.
- [ ] Profiles contain valid compute zone and region defaults.
- [ ] Profile activation via `manage_gcloud_configs.py activate <name>` executes with exit code `0`.
