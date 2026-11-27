#!/usr/bin/env bash
# ==============================================================================
# dev-environment-setup: setup_dev_env.sh
# Idempotent installation of developer CLI suite:
# - uv (Python tool manager)
# - nvm + Node.js LTS + Wrangler
# - Google Cloud CLI (gcloud)
# - Google Colab CLI (colab via uv tool)
# - Kaggle CLI (kaggle via uv tool)
# ==============================================================================
set -euo pipefail

echo "==> [1/5] Checking/Installing uv..."
if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "uv is already installed: $(uv --version)"
fi
export PATH="$HOME/.local/bin:$PATH"

echo "==> [2/5] Checking/Installing nvm, Node.js LTS, and Wrangler..."
export NVM_DIR="$HOME/.nvm"
if [ ! -d "$NVM_DIR" ]; then
    echo "Installing nvm v0.40.1..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi
# Load nvm
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

if ! nvm ls --lts >/dev/null 2>&1; then
    echo "Installing Node.js LTS..."
    nvm install --lts
    nvm alias default "lts/*"
    nvm use default
else
    echo "Node.js LTS is already available: $(node -v 2>/dev/null || echo 'loading...')"
    nvm use default || nvm use --lts
fi

if ! command -v wrangler >/dev/null 2>&1; then
    echo "Installing Wrangler globally..."
    npm install -g --allow-scripts=esbuild,workerd wrangler
else
    echo "Wrangler is already installed: $(wrangler --version 2>/dev/null || echo 'available')"
fi

echo "==> [3/5] Checking/Installing Google Cloud CLI (gcloud)..."
if [ -d "$HOME/google-cloud-sdk" ] && [ -x "$HOME/google-cloud-sdk/bin/gcloud" ]; then
    echo "gcloud is already installed: $("$HOME/google-cloud-sdk/bin/gcloud" --version | head -n 1)"
else
    echo "Downloading and installing Google Cloud SDK..."
    curl -fsSL https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz -o /tmp/google-cloud-cli.tar.gz
    tar -xzf /tmp/google-cloud-cli.tar.gz -C "$HOME"
    rm -f /tmp/google-cloud-cli.tar.gz
    "$HOME/google-cloud-sdk/install.sh" --quiet --rc-path="$HOME/.bashrc"
fi
export PATH="$HOME/google-cloud-sdk/bin:$PATH"

echo "==> [4/5] Checking/Installing Google Colab CLI (colab)..."
if ! command -v colab >/dev/null 2>&1; then
    echo "Installing google-colab-cli via uv tool..."
    uv tool install google-colab-cli
else
    echo "colab is already installed."
fi

echo "==> [5/5] Checking/Installing Kaggle CLI (kaggle)..."
if ! command -v kaggle >/dev/null 2>&1 || ! kaggle --version >/dev/null 2>&1; then
    echo "Installing kaggle CLI via uv tool (with six)..."
    uv tool install --with six kaggle --force
else
    echo "kaggle is already installed: $(kaggle --version)"
fi

echo "==> [SUCCESS] All developer CLI tools installed and configured successfully!"
