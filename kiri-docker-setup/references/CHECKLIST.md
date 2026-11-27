# CHECKLIST.md

## Acceptance Criteria

- [ ] `~/.local/bin/kiri` exists and is executable (`0755`).
- [ ] `~/.local/bin/docker` is linked to `~/.local/libexec/kiri/bin/docker`.
- [ ] `~/.docker/cli-plugins/docker-compose` and `docker-buildx` are linked and report valid versions.
- [ ] `/etc/systemd/system/kiri.service` is loaded, active, and enabled.
- [ ] `/run/kiri/docker.sock` exists with readable/writable permissions for the non-root user.
- [ ] `docker context ls` shows `kiri *` as the current active context.
- [ ] `docker run --rm alpine echo hello` succeeds with exit code `0`.
- [ ] `/mnt/d/.agents/skills/` contains symlinks for all skills present in `/mnt/d/skills`.
