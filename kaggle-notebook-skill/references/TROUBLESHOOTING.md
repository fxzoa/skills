# Troubleshooting (`kaggle-notebook`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `No space left on device` in `/tmp` | Local `/tmp` is tmpfs (~4.7 GB) | Pass a larger work dir to `publish_kaggle_model.sh /mnt/d/tmp/kaggle_models/<slug>` |
| `403` / `404` on `/kaggle/input/...` | Public Model or Private Dataset not published yet | Run `publish_kaggle_model.sh` / `publish_kaggle_dataset.sh create` first |
| `libcudart.so.12` missing | `LD_LIBRARY_PATH` lacks `nvidia/*/lib` or `/usr/local/cuda/lib64` | Prepend `/tmp/.venv/lib/python*/site-packages/nvidia/*/lib` and `/usr/local/cuda/lib64` |
| `kernels output` hangs or hits 20GB limit | Models or `.venv` saved in `/kaggle/working` | Move to `/tmp/.venv` and `/tmp/models` |
| Kernel never finishes (`RUNNING`) | `while True:` log loop at end of notebook | Replace with bounded log snapshot cells |
