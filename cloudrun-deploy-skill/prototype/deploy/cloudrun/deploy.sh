#!/usr/bin/env bash
# ==============================================================================
# deploy.sh: Cloud Run 統合デプロイスクリプト
# ==============================================================================
set -euo pipefail

# プロジェクト設定（環境変数またはデフォルト値）
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo "")}"
REGION="${GCP_REGION:-asia-northeast1}"
SERVICE_NAME="${CLOUDRUN_SERVICE_NAME:-coin-trade-all-in-one}"
REPO_NAME="${ARTIFACT_REPO_NAME:-coin-trade-repo}"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"

echo "=== [GCP Cloud Run Deploy Script] ==="
echo "Project ID:    ${PROJECT_ID}"
echo "Region:        ${REGION}"
echo "Service Name:  ${SERVICE_NAME}"
echo "Target Image:  ${IMAGE_NAME}"
echo "====================================="

if [ -z "$PROJECT_ID" ]; then
  echo "ERROR: GCP Project ID is not specified. Please set GCP_PROJECT_ID or run 'gcloud config set project <ID>'." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "$ROOT_DIR"

# 1. Artifact Registry リポジトリの存在確認 & 作成（未存在時）
echo "--> Checking Artifact Registry repository..."
if ! gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" >/dev/null 2>&1; then
  echo "Creating Artifact Registry repository: $REPO_NAME in $REGION..."
  gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --description="Docker repository for coin-trade-kaggle Cloud Run deployment"
fi

# 2. Docker 認証設定
echo "--> Configuring Docker credentials for Artifact Registry..."
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

# 3. Docker イメージのビルド
echo "--> Building Docker image: ${IMAGE_NAME}..."
docker build -t "${IMAGE_NAME}" -f docker/Dockerfile.cloudrun .

# 4. イメージのプッシュ
echo "--> Pushing Docker image to Artifact Registry..."
docker push "${IMAGE_NAME}"

# 5. Cloud Run へデプロイ
echo "--> Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image="$IMAGE_NAME" \
  --platform=managed \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --allow-unauthenticated \
  --port=8080 \
  --cpu=2 \
  --memory=2Gi \
  --no-cpu-throttling \
  --min-instances=1 \
  --max-instances=1 \
  --execution-environment=gen2 \
  --set-env-vars="PORT=8080,HOST=0.0.0.0,DB_PATH=/app/data/tracker.db"

echo "=== Deployment Successfully Completed! ==="
gcloud run services describe "$SERVICE_NAME" --platform=managed --region="$REGION" --format="value(status.url)"
