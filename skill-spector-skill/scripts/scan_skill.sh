#!/usr/bin/env bash
set -euo pipefail

SKILLSPECTOR_BIN="/mnt/d/tools/skillspector/repo/.venv/bin/skillspector"

if [[ ! -x "$SKILLSPECTOR_BIN" ]]; then
  echo "Error: SkillSpector binary not found at $SKILLSPECTOR_BIN" >&2
  exit 1
fi

TARGET="${1:-}"
OUTPUT="${2:-}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <target_path_or_url> [output_json_path]" >&2
  exit 1
fi

CMD=("$SKILLSPECTOR_BIN" "scan" "$TARGET" "--no-llm")

if [[ -n "$OUTPUT" ]]; then
  CMD+=("--format" "json" "--output" "$OUTPUT")
fi

echo "[*] Running: ${CMD[*]}"
exec "${CMD[@]}"
