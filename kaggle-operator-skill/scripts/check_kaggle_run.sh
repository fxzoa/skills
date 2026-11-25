#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <kaggle_dir> [output_dir]" >&2
  exit 1
fi

KAGGLE_DIR="$(cd "$1" && pwd)"
OUT_DIR="${2:-/tmp/kaggle_output}"
KERNEL_ID="$(python3 -c "import json; print(json.load(open('${KAGGLE_DIR}/kernel-metadata.json'))['id'])")"

STATUS_OUT="$(kaggle kernels status "${KERNEL_ID}")"
echo "${STATUS_OUT}"

if echo "${STATUS_OUT}" | grep -qiE "ERROR|COMPLETE"; then
  mkdir -p "${OUT_DIR}"
  kaggle kernels output "${KERNEL_ID}" -p "${OUT_DIR}"
  ls -la "${OUT_DIR}"
fi
