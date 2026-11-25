# Operation Guide (`kaggle-operator`)

1. **Deploy**: Run `python3 scripts/deploy_kaggle.py <kaggle_dir> [--model-work-dir <dir>]` to auto-create missing Datasets/Models and push the notebook.
2. **Monitor**: Poll `bash scripts/check_kaggle_run.sh <kaggle_dir> [out_dir]` until `COMPLETE` or `ERROR`.
3. **Fix Loop**: On `ERROR`, inspect `<out_dir>/<slug>.log` and `logs/*.log`, patch locally, and re-run `deploy_kaggle.py`.
4. **Verify**: Execute `http.rest` requests against the live tunnel URL.
