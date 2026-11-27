# GUIDE.md

## Step-by-Step Initial Setup Runbook

When setting up a clean machine or re-initializing the container environment:

### 1. Execute Binary and Tooling Installation
```bash
python3 scripts/install_kiri.py
```
This downloads Kiri `v0.2.2`, places the binaries in `~/.local/bin`, wires the Docker CLI plugins into `~/.docker/cli-plugins`, and creates the Docker context `kiri`.

### 2. Configure and Enable Systemd Daemon Service
```bash
python3 scripts/setup_service.py
```
This registers `/etc/systemd/system/kiri.service` with root execution and socket permissions, then reloads systemd and enables the service for persistent auto-start on boot.

### 3. Link Antigravity Skills
```bash
python3 scripts/link_skills.py
```
This scans `/mnt/d/skills` and creates symlinks in both the workspace (`.agents/skills`) and global (`~/.gemini/config/skills`) directories.

### 4. Verification
```bash
docker context use kiri
docker ps
docker run --rm alpine echo "Setup verified!"
```
