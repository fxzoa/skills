# cloudrun-deploy: Troubleshooting & Known Issues

## 1. Invalid Reference Format in Docker Build
- **Symptom:** `invalid argument "...:" for "-t, --tag" flag: invalid reference format` in Cloud Build.
- **Cause:** Using `$COMMIT_SHA` in `cloudbuild.yaml` when running `gcloud builds submit` manually from a dirty or non-git directory (which substitutes an empty string).
- **Fix:** In `cloudbuild.yaml`, tag explicitly with `:latest` or provide default substitutions for `COMMIT_SHA`.

## 2. HTTP 403 Forbidden on Deployed Cloud Run URL
- **Symptom:** `curl` returns `HTTP/2 403` with Google Frontend page.
- **Cause:** Unauthenticated invocations are disallowed by default.
- **Fix:** Run `gcloud run services add-iam-policy-binding <service> --member="allUsers" --role="roles/run.invoker"`. (Automated by `scripts/deploy_cloudrun.py`).

## 3. Bot Background Loop Pausing / Timeout
- **Symptom:** Trading loops or price monitors stop executing after HTTP requests finish.
- **Cause:** Cloud Run CPU throttling is enabled by default.
- **Fix:** Set `--no-cpu-throttling` (or `run.googleapis.com/cpu-throttling: "false"` in Knative YAML) and configure `--min-instances=1`.

## 4. Permission Denied for Cloud Build Service Account
- **Symptom:** `Cloud Run error: The user-provided container failed to deploy... Access denied.`
- **Cause:** Default Cloud Build service account (`<project-number>@cloudbuild.gserviceaccount.com`) lacks Cloud Run Admin permissions.
- **Fix:** Run `scripts/provision_apis_and_repo.py` which automatically grants `roles/run.admin` and `roles/iam.serviceAccountUser`.
