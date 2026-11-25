# TRIGGERS.md: Trigger & Smoke Test Guide (`setup-run-crawl4ai`)

## Positive Trigger Examples
1. **Initial Crawl4AI Docker setup**: "Set up a self-hosted Crawl4AI container on this machine with `--shm-size=1g`, generate an API token, and save it to `.env`."
2. **Verify Crawl4AI health and scraping**: "Check that the local Crawl4AI container is healthy and run a test scrape against `https://example.com`."
3. **Extract clean Markdown from a URL**: "Use the running Crawl4AI container to crawl `https://docs.example.com` and output Markdown."

## Negative Trigger Examples
1. **Deploying arbitrary Docker Compose stacks to cloud VMs**: "Deploy my Nginx + Postgres `docker-compose.yml` to a GCE VM and register DNS." (Use `vm-docker-deploy` instead.)
2. **Simple static HTTP health check without browser rendering**: "Curl `http://localhost:8080/healthz`." (Standard `curl` suffices; no headless Chromium needed.)
3. **Deploying a Kaggle GPU notebook**: "Push this LLM inference notebook to Kaggle." (Use `kaggle-operator` instead.)

## Smoke Test
1. Verify all Crawl4AI CLI scripts respond cleanly to `--help`:
   ```bash
   python3 -B scripts/setup_crawl4ai.py --help
   python3 -B scripts/verify_crawl4ai.py --help
   python3 -B scripts/crawl_url.py --help
   ```
2. Validate the skill structure:
   ```bash
   python3 -B /home/ppbb/.gemini/antigravity-cli/skills/create-new-skill/scripts/validate_skill.py .
   ```
3. (When Docker is running) Run `python3 -B scripts/verify_crawl4ai.py --env-file .env` and confirm exit code `0`.
