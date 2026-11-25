# Operation Guide (`vm-docker-deploy`)

This guide explains how agents and operators use `vm-docker-deploy` tools to inspect, deploy, register DNS, and maintain Docker workloads on remote cloud VMs.

---

## 1. Complete Workflow (End-to-End)

### Step 1: Pre-Flight Inspection
Check compose dependencies, SSH keys, and volume mounts before deploying:
```bash
python3 scripts/inspect_compose.py --compose /path/to/docker-compose.yml
```

### Step 2: Automated Deployment
Provisions Docker if missing, sets up directories/keys, and starts containers with healthcheck monitoring:
```bash
python3 scripts/deploy_compose.py \
  --compose /path/to/docker-compose.yml \
  --vm my-vm-instance \
  --project my-gcp-project \
  --zone us-central1-a
```

### Step 3: DNS Record Registration (Optional)
Automatically maps the VM's public IP to a Cloudflare subdomain via `dns-worker`:
```bash
python3 scripts/register_dns.py \
  --vm my-vm-instance \
  --subdomain kline \
  --zone btczoa.app
```

### Step 4: Health and Log Verification
Verify container runtime status and logs:
```bash
python3 scripts/verify_vm.py \
  --vm my-vm-instance \
  --remote-dir ~/app/kline-collector
```

### Step 5: Teardown and Cleanup (When needed)
Safely stop the stack and remove remote directories:
```bash
python3 scripts/teardown_vm.py \
  --vm my-vm-instance \
  --remote-dir ~/app/kline-collector \
  --volumes
```

---

## 2. Command Reference

| Script | Primary Arguments | Purpose |
|:---|:---|:---|
| `inspect_compose.py` | `--compose <file> [--json]` | Identify volumes, ports, and .env dependencies |
| `deploy_compose.py` | `--compose <file> --vm <vm> [--env-file <.env>]` | Full deployment lifecycle with healthchecks |
| `register_dns.py` | `--vm <vm> --subdomain <subdomain> [--zone <zone>]` | Cloudflare DNS mapping via API |
| `verify_vm.py` | `--vm <vm> [--remote-dir <dir>]` | Quick remote container status check |
| `teardown_vm.py` | `--vm <vm> --remote-dir <dir> [--volumes]` | Stop stack and cleanup |
