# Creation Guide (`kaggle-notebook`)

1. **Scaffold**: Run `python3 scripts/scaffold_kaggle_project.py --dir <dir> --owner <user> --slug <slug> --hf-repo <repo> --model-file <file>`.
2. **Configure**: Copy `.env.example` to `.env` and fill `TUNNEL_TOKEN`, `TUNNEL_HOSTNAME`, `LLM_API_KEY`, `MODEL_NAME`.
3. **Notebook**: Implement single-responsibility `%%writefile` cells (`core/`, `routers/`, `server.py`), startup env dump, `uv venv`, HF API filename check, and snapshot log tail.
4. **Companion Docs**: Generate `README.html` via `readme-html-skill` and verify `http.rest`.
5. **Validate**: Run `python3 scripts/validate_kaggle_bundle.py <dir>`.
