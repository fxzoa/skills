# Operation Guide (`colab-operator`)

1. **Deploy**: Run `bash scripts/deploy_colab.sh <session> <nb.ipynb|script.py> [T4|L4|A100]`.
2. **Monitor**: Run `bash scripts/check_colab_run.sh <session>` to inspect status and logs.
3. **Fix Loop**: Patch local notebook/config on error and re-run `deploy_colab.sh`.
4. **Teardown**: Run `bash scripts/stop_colab.sh <session>` when done.
