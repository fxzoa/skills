#!/usr/bin/env python3
"""
register_chat_service.py
Notebook (.env) または CLI 引数から AI サービス情報を読み込み、
chat-worker の src/client/domains.ts と src/server/secrets.ts へ冪等に登録・更新する。
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def parse_env_file(env_path: Path) -> dict[str, str]:
    if not env_path.is_file():
        raise FileNotFoundError(f".env が見つかりません: {env_path}")
    data: dict[str, str] = {}
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def infer_model_from_env(env: dict[str, str]) -> str:
    for key in ("MAYA_MODEL", "MODEL_NAME", "DEFAULT_MODEL", "LLM_MODEL", "SERVED_MODEL_NAME"):
        if env.get(key):
            return env[key]
    return ""


def build_preset_block(
    service_id: str,
    label: str,
    url: str,
    port: int,
    api_key: str,
    category: str,
    description: str,
    model_id: str,
) -> str:
    lines = [
        "  {",
        f"    id: '{service_id}',",
        f"    label: '{label}',",
        f"    url: '{url}',",
        f"    port: {port},",
        f"    apiKey: '{api_key}',",
        f"    category: '{category}',",
        f"    description: '{description}',",
    ]
    if model_id:
        lines.extend([
            "    models: [",
            f"      {{ id: '{model_id}', label: '{model_id}' }},",
            "    ],",
            f"    defaultModel: '{model_id}',",
        ])
    lines.append("  },")
    return "\n".join(lines)


def upsert_domains_ts(
    domains_path: Path,
    service_id: str,
    preset_block: str,
    dry_run: bool,
) -> str:
    content = domains_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"  \{{\s*\n\s*id:\s*['\"]{re.escape(service_id)}['\"].*?\n  \}},",
        re.DOTALL,
    )
    if pattern.search(content):
        updated = pattern.sub(preset_block, content, count=1)
        action = f"updated preset '{service_id}' in {domains_path}"
    else:
        anchor = "export const ENDPOINT_PRESETS: TargetEndpointPreset[] = ["
        idx = content.find(anchor)
        if idx == -1:
            raise ValueError(f"ENDPOINT_PRESETS が見つかりません: {domains_path}")
        insert_pos = content.find("\n", idx) + 1
        updated = content[:insert_pos] + preset_block + "\n" + content[insert_pos:]
        action = f"inserted preset '{service_id}' into {domains_path}"

    if not dry_run:
        domains_path.write_text(updated, encoding="utf-8")
    return action


def upsert_secrets_ts(
    secrets_path: Path,
    hostname: str,
    service_id: str,
    api_key: str,
    dry_run: bool,
) -> str:
    content = secrets_path.read_text(encoding="utf-8")
    if not api_key:
        return f"skipped secrets.ts (empty apiKey for {hostname})"

    block = (
        f"  // {service_id} ({hostname})\n"
        f"  if (domain.includes('{hostname}')) {{\n"
        f"    if (cleanKey && !cleanKey.toLowerCase().includes('dummy') && cleanKey !== env.CHAT_API_TOKEN) {{\n"
        f"      return cleanKey;\n"
        f"    }}\n"
        f"    return '{api_key}';\n"
        f"  }}\n\n"
    )

    host_pattern = re.compile(
        rf"  //[^\n]*\n  if \(domain\.includes\('{re.escape(hostname)}'\)\) \{{.*?\n  \}}\n*",
        re.DOTALL,
    )
    if host_pattern.search(content):
        updated = host_pattern.sub(block, content, count=1)
        action = f"updated domain rule '{hostname}' in {secrets_path}"
    else:
        anchor = "  // 6. 一般ドメイン"
        idx = content.find(anchor)
        if idx == -1:
            raise ValueError(f"フォールバックアンカー '{anchor}' が見つかりません: {secrets_path}")
        updated = content[:idx] + block + content[idx:]
        action = f"inserted domain rule '{hostname}' into {secrets_path}"

    if not dry_run:
        secrets_path.write_text(updated, encoding="utf-8")
    return action


def main() -> int:
    parser = argparse.ArgumentParser(description="Register an AI service into chat-worker")
    parser.add_argument("--chat-worker-dir", default="/mnt/d/cf-workers/chat-worker", help="Path to chat-worker repo")
    parser.add_argument("--env", dest="env_file", default=None, help="Path to notebook .env file")
    parser.add_argument("--id", dest="service_id", required=True, help="Preset ID (e.g. code-ai)")
    parser.add_argument("--label", default=None, help="Display label")
    parser.add_argument("--hostname", default=None, help="Public hostname (e.g. code-ai.btczoa.app)")
    parser.add_argument("--port", type=int, default=None, help="Service port (e.g. 8007)")
    parser.add_argument("--api-key", default=None, help="Upstream Bearer API key")
    parser.add_argument("--model", default=None, help="Default model ID")
    parser.add_argument("--category", default="Colab AI Studio", help="Preset category")
    parser.add_argument("--description", default=None, help="Service description")
    parser.add_argument("--no-deploy", action="store_true", help="Skip typecheck, test, and wrangler deploy after registration")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files or deploying")

    args = parser.parse_args()
    env_data = parse_env_file(Path(args.env_file)) if args.env_file else {}

    hostname = (args.hostname or env_data.get("TUNNEL_HOSTNAME") or "").strip()
    if not hostname:
        print("[ERROR] --hostname または .env の TUNNEL_HOSTNAME が必要です。", file=sys.stderr)
        return 1

    port = args.port or int(env_data.get("TUNNEL_PORT", "8000"))
    api_key = (args.api_key if args.api_key is not None else env_data.get("LLM_API_KEY", "")).strip()
    model_id = (args.model if args.model is not None else infer_model_from_env(env_data)).strip()
    url = hostname if hostname.startswith("http") else f"https://{hostname}"
    clean_host = url.replace("https://", "").replace("http://", "").split("/")[0]
    label = args.label or f"{args.service_id} ({model_id or clean_host})"
    description = args.description or f"{args.service_id}: {model_id or clean_host} (Port: {port})"

    cw_dir = Path(args.chat_worker_dir)
    domains_path = cw_dir / "src" / "client" / "domains.ts"
    secrets_path = cw_dir / "src" / "server" / "secrets.ts"

    preset_block = build_preset_block(
        service_id=args.service_id,
        label=label,
        url=url,
        port=port,
        api_key=api_key,
        category=args.category,
        description=description,
        model_id=model_id,
    )

    msg1 = upsert_domains_ts(domains_path, args.service_id, preset_block, args.dry_run)
    msg2 = upsert_secrets_ts(secrets_path, clean_host, args.service_id, api_key, args.dry_run)

    prefix = "[DRY-RUN]" if args.dry_run else "[OK]"
    print(f"{prefix} {msg1}")
    print(f"{prefix} {msg2}")

    if args.dry_run or args.no_deploy:
        return 0

    verify_script = Path(__file__).resolve().parent / "verify_and_deploy_chat_worker.py"
    cmd = [
        sys.executable,
        str(verify_script),
        "--chat-worker-dir",
        str(cw_dir),
        "--deploy",
        "--upstream-url",
        url,
    ]
    if api_key:
        cmd.extend(["--api-key", api_key])
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
