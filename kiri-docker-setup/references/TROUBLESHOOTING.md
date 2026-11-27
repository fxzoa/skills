# TROUBLESHOOTING.md

## 1. `dial unix /run/kiri/docker.sock: no such file or directory`
* **Cause:** The systemd daemon is not running or crashed upon startup.
* **Fix:** Check service status with `sudo systemctl status kiri.service`. Ensure `HOME=/root` and `KIRI_SOCKET=/run/kiri/docker.sock` are defined in the unit file.

## 2. `on Linux, Kiri runs containers on this machine's kernel and needs root: sudo kiri daemon`
* **Cause:** Kiri daemon was started under a non-root user instead of root/systemd.
* **Fix:** Stop user daemon with `pkill -f "kiri daemon"` and start the systemd service via `sudo systemctl start kiri.service`.

## 3. `permission denied while trying to connect to the Docker daemon socket`
* **Cause:** `/run/kiri/docker.sock` permissions do not permit access by the user.
* **Fix:** Verify `ExecStartPost=/bin/sh -c "sleep 0.5 && chmod 666 /run/kiri/docker.sock || true"` is present in `/etc/systemd/system/kiri.service`.
