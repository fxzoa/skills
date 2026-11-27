# PREREQUISITES.md

## Hardware & Operating System
* **OS:** Linux x86_64 (Ubuntu 22.04+ or WSL2 on Windows 10/11)
* **Kernel:** Linux Kernel 5.15+ with cgroups v2 and user namespace support
* **Architecture:** `x86_64` (or `aarch64` when using arm64 releases)

## Packages & System Tools
* `python3` (3.8+)
* `dpkg` (for deb extraction)
* `sudo` access (for systemd service registration)
* `conf/.env` containing `SUDO_PASSWORD=...` (optional for non-interactive automation)
