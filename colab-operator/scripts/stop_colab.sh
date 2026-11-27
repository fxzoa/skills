#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <session_name>" >&2
  exit 1
fi

SESSION="$1"
colab --auth=adc stop -s "${SESSION}"
