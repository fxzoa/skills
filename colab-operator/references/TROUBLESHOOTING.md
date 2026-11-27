# Troubleshooting (`colab-operator`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `colab` command hangs indefinitely | Interactive command (`repl`, `console`, `auth`, `drivemount`) called | Never use interactive commands; use `colab exec -s <name> -f <file>` |
| ADC auth expired / 401 | Missing `colaboratory` or `cloud-platform` scope | Re-run `gcloud auth application-default login` with all 4 scopes |
| Quota exceeded on `colab new` | Requested A100/L4 unavailable | Fall back to `--gpu T4` or CPU |
