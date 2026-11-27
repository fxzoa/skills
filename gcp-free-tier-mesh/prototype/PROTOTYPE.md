# Prototype & Reuse Boundary (`gcp-free-tier-mesh`)

## 1. Reusable Core Design (Keep Across Projects)
1. **5-Project Star-Topology VPC Peering (`templates/terraform/`)**:
   - Single-zone placement (`us-central1-a`) across distinct GCP projects for **$0.00 cross-project internal egress**.
   - Non-overlapping `/24` CIDRs (`10.0.0.0/24`, `10.10.0.0/24`, ..., `10.40.0.0/24`).
   - Sequential `depends_on` chaining across all hub and spoke `google_compute_network_peering` resources to avoid GCP API race conditions.
   - CIDR-based `source_ranges` firewall rules (`allow-internal`, `allow-redis-from-peered-vpcs`) because network tags do not cross VPC peering boundaries.
   - `access_tokens` + `credentials_files` dual-mode provider aliases in `versions.tf`.
2. **Always Free GCE Node Module (`templates/terraform/modules/free-tier-node/`)**:
   - `e2-micro` + `pd-standard` (<= 30 GB) + `STANDARD` network tier + optional budget safeguard alerts.
3. **3-Container-Per-VM Distribution (`templates/compose/`)**:
   - Cap each `e2-micro` (1 GB RAM) to `<= 3` containers (`redis-tunnel` + 2 worker/bot services) with `DENO_V8_FLAGS=--max-old-space-size=96` and 1 GB Swap safety margin.
   - Offload WebUIs to ad-hoc Cloud Run instead of running them 24/7 on `e2-micro`.

## 2. Project-Specific Replacements (Replace When Adapting)
| File / Field | Current Sample Value (`coin-trade`) | What to Replace |
| :--- | :--- | :--- |
| `templates/terraform/variables.tf` (`nodes`) | `btczoa-project`, `fxzoa2020-project`, `nanbingjun-project`, `nanheishun-project`, `nanzhiyan-project` | Target GCP project IDs, instance names, billing IDs, and roles. |
| `templates/terraform/variables.tf` (`ssh_public_key`) | `ssh-ed25519 ... nanbingjun@gmail.com` | Your operator SSH public key. |
| `templates/compose/vm*.yml` | `price-monitor`, `btc-dca-bot`, `coin-trade-bot`, etc. | Target application images, `./env/*.env` paths, and `./data/*` mounts. |
| `REDIS_SSH_HOST` in `vm1..vm4` | `10.0.0.3` | Actual `redis_internal_target` output from `terraform output`. |
