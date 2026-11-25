#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="${1:-/mnt/d/tmp/kaggle_models/sample-llm-model}"
python3 "${SCRIPT_DIR}/download_model.py" --output-dir "${WORK_DIR}"
cp "${SCRIPT_DIR}/model-instance-metadata.json" "${WORK_DIR}/model-instance-metadata.json"
kaggle models create -p "${SCRIPT_DIR}" 2>&1 || true
if ! kaggle models instances create -p "${WORK_DIR}" -r tar 2>&1; then
  kaggle models instances versions create "example-user/sample-llm-model/other/default" -p "${WORK_DIR}" -r tar -n "Update model"
fi
