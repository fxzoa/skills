# Step-by-Step Deployment Guide (`gcp-free-tier-mesh`)

1. **Authenticate all GCP accounts**:
   ```bash
   gcloud auth list
   # If any account is missing:
   gcloud auth login <missing-email>
   ```
2. **Link Billing Accounts** (supports cross-account fallback if an account has 0 billing accounts):
   ```bash
   python3 scripts/link_billing.py \
     --pair btczoa@gmail.com:btczoa-project \
     --pair fxzoa2020@gmail.com:fxzoa2020-project \
     --pair nanbingjun@gmail.com:nanbingjun-project \
     --pair nanheishun@gmail.com:nanheishun-project \
     --pair nanzhiyan@gmail.com:nanzhiyan-project \
     --fallback-owner btczoa@gmail.com \
     --fallback-billing-id 0103DF-7EDA87-A9702B
   ```
3. **Provision VMs, VPCs, and sequential VPC Peerings via Terraform**:
   ```bash
   python3 scripts/apply_tf_tokens.py \
     --tf-dir /mnt/d/gcp-always-free-tf \
     --node btczoa:btczoa@gmail.com \
     --node fxzoa2020:fxzoa2020@gmail.com \
     --node nanbingjun:nanbingjun@gmail.com \
     --node nanheishun:nanheishun@gmail.com \
     --node nanzhiyan:nanzhiyan@gmail.com \
     --action apply --auto-approve
   ```
4. **Package local Docker images** (skip for public Hub images like `redis:alpine` or `nanbingjun/coin-trade-bot:latest`):
   ```bash
   python3 scripts/package_images.py --out-dir /mnt/d/coin-trade-kaggle/tmp/src/images \
     --bundle vm1-images=nanbingjun/price-change-monitor:latest,coin-trade-kaggle-slack-alert-sender:latest
   ```
5. **Deploy each node** with `scripts/deploy_mesh.py` (ensures 1 GB Swap, `chmod 777` on new `./data/*` dirs, `.env` sync, and `vm-docker-deploy`).
6. **Verify mesh health** with `scripts/verify_mesh.py`.
