# Creation Guide (`colab-notebook`)

1. **Scaffold**: Run `python3 scripts/scaffold_colab_project.py --dir <dir> --model-name <model>`.
2. **Configure**: Create external `.env` from `.env.example`.
3. **Notebook**: Build the 24-step Colab Studio notebook using `%%writefile` cells (`core/`, `routers/`, `server.py`).
4. **Companion Docs**: Generate `README.html` and verify `http.rest`.
5. **Validate**: Run `python3 scripts/validate_colab_bundle.py <dir> <notebook.ipynb>`.
