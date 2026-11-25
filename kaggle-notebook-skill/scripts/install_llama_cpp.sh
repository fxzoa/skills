#!/usr/bin/env bash
# Kaggle / Colab (Ubuntu x64 + CUDA 13 / 12) 向け llama.cpp 公式プリコンパイル済みバイナリ自動導入スクリプト
set -euo pipefail

INSTALL_DIR="${1:-/opt/llama.cpp}"
mkdir -p "$INSTALL_DIR"

DOWNLOAD_URL=$(python3 - <<'EOF'
import json, urllib.request

url = "https://api.github.com/repos/ggml-org/llama.cpp/releases/latest"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())

assets = data.get("assets", [])
candidates = [
    a["browser_download_url"]
    for a in assets
    if "ubuntu" in a["name"].lower()
    and "x64" in a["name"].lower()
    and "cuda" in a["name"].lower()
    and (a["name"].endswith(".tar.gz") or a["name"].endswith(".zip"))
]

cuda13 = [u for u in candidates if "cuda-13" in u.lower() or "cuda13" in u.lower()]
selected = cuda13[0] if cuda13 else (candidates[0] if candidates else "")
if not selected:
    raise SystemExit("Error: Suitable Ubuntu CUDA binary not found in latest release.")
print(selected)
EOF
)

echo "Downloading: $DOWNLOAD_URL"
cd /tmp
if [[ "$DOWNLOAD_URL" == *.tar.gz ]]; then
    curl -fL "$DOWNLOAD_URL" -o llama.tar.gz
    tar -xzf llama.tar.gz -C "$INSTALL_DIR" --strip-components=1 2>/dev/null || tar -xzf llama.tar.gz -C "$INSTALL_DIR"
    rm -f llama.tar.gz
else
    curl -fL "$DOWNLOAD_URL" -o llama.zip
    unzip -qo llama.zip -d "$INSTALL_DIR"
    rm -f llama.zip
fi

echo "$INSTALL_DIR" > /etc/ld.so.conf.d/llama-cpp.conf
ldconfig

for bin in llama-cli llama-server llama-bench llama-quantize; do
    BIN_PATH=$(find "$INSTALL_DIR" -type f -name "$bin" | head -n 1 || true)
    if [[ -n "$BIN_PATH" ]]; then
        chmod +x "$BIN_PATH"
        ln -sf "$BIN_PATH" "/usr/local/bin/$bin"
    fi
done

echo "Installation complete: $INSTALL_DIR"
