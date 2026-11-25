#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE_DIR="/tmp/sample-llm-env-dataset_stage"
MODE="${1:-version}"
MESSAGE="${2:-Update .env}"
python3 "${SCRIPT_DIR}/prepare_dataset.py" --stage-dir "${STAGE_DIR}"
case "${MODE}" in
  create) kaggle datasets create -p "${STAGE_DIR}" -r zip ;;
  version) kaggle datasets version -p "${STAGE_DIR}" -m "${MESSAGE}" -r zip ;;
  *) echo "Usage: $0 [create|version] [message]" >&2; exit 1 ;;
esac
