# TRIGGERS.md: Trigger & Smoke Test Guide (`vm-docker-deploy`)

## Positive Trigger Examples
1. **Deploy Docker Compose to a GCE VM**: "Inspect `docker-compose.yml` for volume/key dependencies and deploy it to my GCE VM `api-prod-1`."
2. **Register Cloudflare DNS for a VM**: "Look up the external IP of VM `api-prod-1` and register an A record for `api` via `register_dns.py`."
3. **Verify or tear down a remote VM stack**: "Check container health on `api-prod-1` or tear down the remote Compose stack and clean up volumes."

## Negative Trigger Examples
1. **Local Crawl4AI container setup**: "Spin up a local Crawl4AI Docker container on my laptop and save the token to `.env`." (Use `setup-run-crawl4ai` instead.)
2. **Kaggle notebook deployment**: "Push a notebook and dataset to Kaggle Cloud." (Use `kaggle-operator` instead.)
3. **Kubernetes / Helm chart authoring**: "Write a Helm chart for a GKE cluster." (Out of scope for single-VM Docker Compose deployment.)

## Smoke Test
1. Verify all 5 VM deployment scripts respond cleanly to `--help`:
   ```bash
   python3 -B scripts/inspect_compose.py --help
   python3 -B scripts/deploy_compose.py --help
   python3 -B scripts/register_dns.py --help
   python3 -B scripts/verify_vm.py --help
   python3 -B scripts/teardown_vm.py --help
   ```
2. Run static inspection on the prototype Compose file and validate the skill:
   ```bash
   python3 -B scripts/inspect_compose.py --compose prototype/docker-compose.yml
   python3 -B /home/ppbb/.gemini/antigravity-cli/skills/create-new-skill/scripts/validate_skill.py .
   ```
