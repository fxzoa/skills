# setup-run-crawl4ai: Acceptance Checklist

## Pre-Flight Checks
- [ ] Docker CLI is installed and running (`docker info` succeeds).
- [ ] Target host port (default: `11235`) is available.
- [ ] Destination `.env` directory is writable.

## Execution Checklist
- [ ] `scripts/setup_crawl4ai.py` completes with exit code `0`.
- [ ] Container `crawl4ai` status is `Up` and `healthy`.
- [ ] `CRAWL4AI_BASE_URL` and `CRAWL4AI_API_TOKEN` are recorded in target `.env`.
- [ ] `scripts/verify_crawl4ai.py` returns exit code `0` on test URL scrape.
- [ ] PROTOTYPE.md documents reusable vs. replaceable boundaries.
- [ ] TOOLS.md covers Command, Shell, MCP, and 外部 API.
