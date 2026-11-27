# Troubleshooting (`colab-notebook`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `FileNotFoundError: .env` | External `.env` not uploaded to `/content/.env` | Upload `.env` before running notebook (Rule.13 forbids `%%writefile .env`) |
| `Address already in use` | Previous Uvicorn or `cloudflared` still bound | Ensure `fuser -k -n tcp {PORT}` and `pkill -9` run before launch |
| `CUDA::cuda_driver` / `Error 137` | Attempted CMake source build of `llama.cpp` | Use prebuilt CUDA wheel (`cu124`) or `scripts/install_llama_cpp.sh` |
