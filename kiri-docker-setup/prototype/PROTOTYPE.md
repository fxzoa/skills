# PROTOTYPE.md

## Reusable Assets & Replacement Boundaries

### Reusable Assets (100% Shared Across Linux/WSL2)
* `scripts/install_kiri.py`: Standard binary extraction and Docker CLI plugin wiring logic.
* `scripts/setup_service.py`: Generic systemd unit template for persistent container daemon management.
* `scripts/link_skills.py`: Workspace and global skill linking automation.

### Replacement Boundaries (Environment-Specific)
* **Architecture:** In `scripts/install_kiri.py`, replace `amd64` with `arm64` when running on Apple Silicon (via Linux VM) or ARM-based servers.
* **Credentials:** In `scripts/setup_service.py`, `conf/.env` path can be pointed to alternative secret stores or interactive prompts.
* **Socket Paths:** Default socket `/run/kiri/docker.sock` can be modified via the `KIRI_SOCKET` environment variable.
