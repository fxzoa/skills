#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <session_name> <notebook_or_script> [gpu_type]" >&2
  exit 1
fi

SESSION="$1"
TARGET="$2"
GPU="${3:-T4}"

if ! colab --auth=adc status -s "${SESSION}" >/dev/null 2>&1; then
  colab --auth=adc new -s "${SESSION}" --gpu "${GPU}"
fi

colab --auth=adc exec -s "${SESSION}" -f "${TARGET}"
colab --auth=adc status -s "${SESSION}"
