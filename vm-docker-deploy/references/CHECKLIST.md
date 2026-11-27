# Acceptance Checklist (`vm-docker-deploy`)

- [ ] Remote VM is reachable via `gcloud compute ssh <vm>`.
- [ ] Docker Engine and Docker Compose Plugin are verified or auto-installed.
- [ ] SSH private keys (if needed for container tunnels) have strict `600` permissions.
- [ ] Compose file transferred and placed in isolated `~/app/<service>/` directory.
- [ ] Host-side mount paths exist prior to container start (avoiding directory creation bug).
- [ ] All containers report `running` or `healthy` state in `docker compose ps`.
- [ ] Application logs confirm successful initialization without fatal crashes.
