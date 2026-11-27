# Creation Guide (`kaggle-app-hosting`)

1. **Scaffold**: Run `python3 scripts/scaffold_app_hosting.py --dir <dir> --owner <user> --slug <slug>`.
2. **Configure**: Populate `.env` and push initial Private Dataset via `kaggle_private_dataset/publish_kaggle_dataset.sh create`.
3. **Notebook**: Implement the 10-cell CPU app hosting notebook (`sync_dataset.py`, `start_services.sh`, `healthcheck.py`, Cloudflare Tunnel, `tail -f`).
4. **Companion Docs**: Generate `README.html` and verify `http.rest`.
5. **Validate**: Run `python3 scripts/validate_app_hosting.py <dir>`.
