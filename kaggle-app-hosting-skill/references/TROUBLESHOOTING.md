# Troubleshooting (`kaggle-app-hosting`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `kaggle datasets create` exits `0` with `already in use` | Dataset slug already exists | Always use `kaggle datasets version -p <stage> -m "<msg>" -r zip` for updates |
| `git clone` fails with `exit 128` | Private repo without credentials | Make repo Public or pass PAT; ensure `.gitignore` excludes secrets first |
| `kaggle kernels output` empty while `RUNNING` | Batch outputs finalize only on completion | Check Kaggle UI Logs tab or download Private Dataset |
| Need to stop `tail -f` kernel | `kaggle` CLI lacks kernel cancel command | Cancel via Kaggle Web UI (**Cancel Run**) |
