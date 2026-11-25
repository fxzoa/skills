# setup-run-crawl4ai: Troubleshooting & Known Issues

## 1. Port 11235 Already in Use
- **Symptom:** `ERROR: Port 11235 is already in use by another process.`
- **Cause:** Another service is binding port 11235.
- **Fix:** Specify an alternative port using `--port <another_port>`:
  ```bash
  python3 scripts/setup_crawl4ai.py --port 11236 --env-file /path/to/.env
  ```

## 2. Chromium Crash (SIGSEGV / OOM)
- **Symptom:** Headless browser crashes when loading heavy pages.
- **Cause:** Docker's default `/dev/shm` size (64MB) is insufficient for Chromium.
- **Fix:** Ensure `--shm-size=1g` is passed to `docker run` (automated by `setup_crawl4ai.py`).

## 3. HTTP 401 Unauthorized
- **Symptom:** API returns `{"detail":"Invalid or missing token"}`.
- **Cause:** Missing `Authorization: Bearer <token>` header, or token mismatch.
- **Fix:** Run `verify_crawl4ai.py --env-file <path>` to check if the token in `.env` matches the running container.

## 4. Corporate Proxy / SSL Interception
- **Symptom:** Connection timeout while pulling image or fetching external sites.
- **Cause:** Office network firewall or TLS inspection.
- **Fix:** Pass `--env HTTP_PROXY=... --env HTTPS_PROXY=...` to Docker daemon configuration.
