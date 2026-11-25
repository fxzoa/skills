# Troubleshooting (`vm-docker-deploy`)

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| `bash: docker: command not found` | The VM was newly provisioned and Docker Engine has not been installed yet. | `deploy_compose.py` will auto-detect and run apt-get provisioning. Alternatively, run the installation script manually. |
| `cp: omitting directory '/ssh-key/id_key'` | Host-side mount target (`~/.ssh/google_compute_engine`) did not exist when Docker started, causing Docker daemon to auto-create a directory instead of a file. | Run `mkdir -p ~/.ssh && touch ~/.ssh/google_compute_engine` before container launch, sync the actual key, and run `docker compose down && docker compose up -d`. |
| `scp: dest open ".ssh/...": No such file` | The remote user home directory does not yet contain a `.ssh` directory. | Run `mkdir -p ~/.ssh && chmod 700 ~/.ssh` via `gcloud compute ssh` before attempting `scp`. |
| `container is unhealthy` | Health check command failed or depends_on timeout expired (e.g., SSH tunnel target unreachable). | Inspect logs using `sudo docker compose logs <service>`. Verify tunnel host/port and remote authentication. |
| `Permission denied (publickey)` in tunnel | SSH key permissions on VM are too permissive or user is incorrect. | Ensure remote key permissions are strictly `chmod 600 ~/.ssh/google_compute_engine`. |
