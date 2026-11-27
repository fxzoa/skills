# Troubleshooting

## 1. CLI Hangs on `gcloud config set`
- **Symptom:** Command blocks waiting for user input: `Do you want to continue (Y/n)?`
- **Cause:** Account is not authenticated locally or project ID is not accessible by the active credential.
- **Solution:** Do not use `gcloud config set` directly. Use `python3 scripts/manage_gcloud_configs.py set` which writes directly to the config INI file without triggering CLI interaction.

## 2. Invalid or Unauthenticated Credentials
- **Symptom:** `ERROR: (gcloud.config.set) Your current active account does not have any valid credentials`
- **Cause:** The profile exists but no OAuth refresh token exists in `~/.config/gcloud/credentials.db`.
- **Solution:** Run `gcloud auth login <email>` in an interactive terminal session once to obtain a browser token.

## 3. Quota Project Mismatch
- **Symptom:** `WARNING: Your active project does not match the quota project in your local Application Default Credentials file.`
- **Solution:** This is a non-fatal warning. If required for ADC, run `gcloud auth application-default set-quota-project <project_id>`.
