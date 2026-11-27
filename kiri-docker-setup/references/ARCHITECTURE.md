# ARCHITECTURE.md

## System Topology & Permissions Model

Kiri operates on Linux by interfacing directly with the Linux kernel (namespaces, cgroups, clone3) without an intermediary virtual machine layer.

```mermaid
flowchart TD
    Client["Docker CLI / Compose / Buildx (Non-Root)"]
    Socket["Unix Domain Socket: /run/kiri/docker.sock (0666)"]
    Service["systemd: kiri.service (Root)"]
    Kernel["Linux Kernel (Namespaces / cgroups v2 / clone3)"]
    Containers["Isolated Containers (Alpine / Nginx)"]

    Client -->|HTTP Engine API| Socket
    Socket --> Service
    Service -->|Syscalls| Kernel
    Kernel --> Containers
```

## Key Configuration Paths
* **Kiri Binary:** `~/.local/bin/kiri`
* **Docker CLI:** `~/.local/bin/docker` -> `~/.local/libexec/kiri/bin/docker`
* **CLI Plugins:** `~/.docker/cli-plugins/{docker-compose, docker-buildx}`
* **Systemd Service:** `/etc/systemd/system/kiri.service`
* **Root Unix Socket:** `/run/kiri/docker.sock`
* **Docker Context:** `kiri` (`host=unix:///run/kiri/docker.sock`)
