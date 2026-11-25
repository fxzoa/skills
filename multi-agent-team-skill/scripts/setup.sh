#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEMPLATE_FILE="${REPO_ROOT}/templates/team_model_delegation.md"

TARGET_DIR="${HOME}/.gemini/config/rules"
TARGET_FILE="${TARGET_DIR}/team_model_delegation.md"
GLOBAL_AGENTS="${HOME}/.gemini/AGENTS.md"

echo "=== Installing Multi-Agent Team Delegation Rules ==="

mkdir -p "${TARGET_DIR}"
cp "${TEMPLATE_FILE}" "${TARGET_FILE}"
echo "✓ Installed rule to: ${TARGET_FILE}"

if [ ! -f "${GLOBAL_AGENTS}" ]; then
  cp "${TEMPLATE_FILE}" "${GLOBAL_AGENTS}"
  echo "✓ Created global AGENTS.md: ${GLOBAL_AGENTS}"
else
  if ! grep -q "Global Multi-Agent Team" "${GLOBAL_AGENTS}"; then
    echo -e "\n\n" >> "${GLOBAL_AGENTS}"
    cat "${TEMPLATE_FILE}" >> "${GLOBAL_AGENTS}"
    echo "✓ Appended delegation rule to existing global AGENTS.md: ${GLOBAL_AGENTS}"
  else
    echo "ℹ Global AGENTS.md already contains team delegation rules. Skipping append."
  fi
fi

echo "=== Setup complete! Multi-agent team delegation is now active globally across all projects. ==="
