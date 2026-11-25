#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <session_name> <notebook_or_script> [gpu_type]" >&2
  exit 1
fi

SESSION="$1"
TARGET="$2"
GPU="${3:-T4}"

if ! colab status -s "${SESSION}" >/dev/null 2>&1; then
  colab new -s "${SESSION}" --gpu "${GPU}"
fi

colab exec -s "${SESSION}" -f "${TARGET}"
colab status -s "${SESSION}"
