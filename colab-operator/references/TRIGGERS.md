# Trigger & Smoke Test Reference (`colab-operator`)

## Positive Trigger Examples
1. **Provision & Run Colab Session**: "Start a Colab L4 session, upload `.env` and `inference.ipynb`, and execute it remotely via `colab` CLI."
2. **Autonomous Log Monitoring & Self-Healing**: "Monitor my running Colab GPU session for OOM or port conflicts and automatically patch/redeploy if it fails."
3. **Teardown & Verification**: "Verify `/healthz` and `/v1/models` on the active Colab session and run `colab stop` when done."

## Negative Trigger Examples
1. **Authoring Notebook Cells**: "Design a new 24-step Colab Studio `.ipynb` with `%%writefile` cells and `tail -f` final cell." → Use `colab-notebook`.
2. **Kaggle Kernel Deployment**: "Push and monitor a notebook on Kaggle Cloud." → Use `kaggle-notebook` or `kaggle-app-hosting`.
3. **Local Docker/Systemd Deployment**: "Deploy a FastAPI service locally using Docker Compose." → Not a Colab CLI task.

## Smoke Test
1. Verify monitor script help exits cleanly:
   ```bash
   python3 -B scripts/schedule_colab_monitor.py --help
   ```
2. Verify `colab` CLI authentication is active (headless check):
   ```bash
   colab whoami
   ```
3. Verify shell scripts are executable and syntactically valid:
   ```bash
   bash -n scripts/deploy_colab.sh scripts/check_colab_run.sh scripts/stop_colab.sh
   ```
