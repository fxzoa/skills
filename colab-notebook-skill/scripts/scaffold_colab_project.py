#!/usr/bin/env python3
"""Scaffold a Colab Studio project bundle (.env.example, http.rest)."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Colab Studio project files.")
    parser.add_argument("--dir", required=True, help="Target project directory")
    parser.add_argument("--model-name", required=True, help="Default MODEL_NAME for .env.example")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    base.mkdir(parents=True, exist_ok=True)

    (base / ".env.example").write_text(
        f"""MODEL_NAME={args.model_name}
TUNNEL_HOST=127.0.0.1
TUNNEL_PORT=8000
TUNNEL_HOSTNAME=colab-studio.example.com
LLM_API_KEY=change-me-to-your-secret-key
VENV_DIR=/tmp/.venv
MODELS_DIR=/tmp/models
""",
        encoding="utf-8",
    )

    (base / "http.rest").write_text(
        """@localUrl = http://{{$dotenv TUNNEL_HOST}}:{{$dotenv TUNNEL_PORT}}
@tunnelUrl = https://{{$dotenv TUNNEL_HOSTNAME}}
@apiKey = {{$dotenv LLM_API_KEY}}
@modelName = {{$dotenv MODEL_NAME}}

### Health Check (Local)
GET {{localUrl}}/healthz

### Health Check (Tunnel)
GET {{tunnelUrl}}/healthz

### Server Status (Tunnel)
GET {{tunnelUrl}}/api/v1/status
Authorization: Bearer {{apiKey}}

### List Models (Tunnel)
GET {{tunnelUrl}}/v1/models
Authorization: Bearer {{apiKey}}

### Chat Completions (Tunnel)
POST {{tunnelUrl}}/v1/chat/completions
Content-Type: application/json
Authorization: Bearer {{apiKey}}

{
  "model": "{{modelName}}",
  "messages": [{"role": "user", "content": "Hello!"}],
  "max_tokens": 128,
  "stream": false
}
""",
        encoding="utf-8",
    )
    print(f"[OK] Scaffolded Colab project in {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
