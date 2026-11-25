# PROTOTYPE.md: Reusable Core vs. Project-Specific Replacements (`vm-docker-deploy`)

This document defines the boundary between reusable core assets and project-specific replacements for `vm-docker-deploy`.

---

## 1. Prototype Structure

```text
prototype/
└── docker-compose.yml   # Sample Nginx service with restart policy and healthcheck
```

---

## 2. Reusable Core vs. Project-Specific Replacements

| Component | Reusable Core Design (Keep As-Is) | Project-Specific Replacements (Customize Per Project) |
|:---|:---|:---|
| **Pre-Flight & Deployment (`scripts/inspect_compose.py`, `scripts/deploy_compose.py`)** | Static YAML inspection (volumes, SSH keys, ports, env), remote Docker provisioning, `chmod 700 ~/.ssh` / `chmod 600` key guards, and health verification. | `--compose` file path, `--vm` instance name, `--project` GCP project ID, `--zone`, and local `.env` / SSH key paths. |
| **DNS Registration (`scripts/register_dns.py`)** | External IP discovery from VM metadata and Cloudflare A-record registration via `dns-worker` API. | `--subdomain` name, target domain/worker credentials, and VM `--zone`. |
| **Verification & Teardown (`scripts/verify_vm.py`, `scripts/teardown_vm.py`)** | Deterministic Docker daemon check, container status inspection, and safe stack/volume cleanup. | `--remote-dir` service directory path on the target VM and `--volumes` retention policy. |
| **Compose Stack (`prototype/docker-compose.yml`)** | `restart: unless-stopped` and `healthcheck` contract. | Service images, container names, port mappings, and volume mounts for your workload. |
