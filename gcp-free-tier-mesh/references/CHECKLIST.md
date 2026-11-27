# Acceptance Checklist (`gcp-free-tier-mesh`)

- [ ] All target GCP projects are linked to an open Billing Account (`billingEnabled: true`).
- [ ] All `e2-micro` VMs reside in the **same zone** (e.g., `us-central1-a`) with `pd-standard` (<= 30 GB) and `STANDARD` network tier.
- [ ] Each VPC uses a **non-overlapping** `/24` CIDR (`10.0.0.0/24` .. `10.40.0.0/24`).
- [ ] All hub-and-spoke VPC Peerings report `STATE: ACTIVE (Connected)`.
- [ ] Hub VM (`vm-btczoa-redis`) has SSH user/key configured (`ppbb` or OS Login) and 1 GB Swap enabled.
- [ ] Each VM runs `<= 3` containers (`redis-tunnel` + max 2 Deno services) with `DENO_V8_FLAGS=--max-old-space-size=96`.
- [ ] `free -m` shows comfortable RAM headroom (~300–350 MB used / ~958 MB total) with minimal Swap usage.
- [ ] No container is stuck in `Restarting` or `unhealthy` state; Redis Pub/Sub connections are established.
