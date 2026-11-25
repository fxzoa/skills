#!/usr/bin/env sh
set -e

echo "=== [Cloud Run All-in-One Entrypoint] Initializing... ==="

# 1. 永続データディレクトリ
mkdir -p /app/data
mkdir -p /app/.cache/deno

# 2. Redis SSH トンネル起動（オプション）
# ENABLE_REDIS_TUNNEL=true かつ SSH_TARGET が指定されている場合のみ実行
if [ "${ENABLE_REDIS_TUNNEL:-false}" = "true" ] || [ -n "${SSH_TARGET:-}" ]; then
  echo "--- Starting Redis SSH Tunnel in background ---"
  if [ -f /ssh/id_key ]; then
    cp /ssh/id_key /tmp/id_key && chmod 600 /tmp/id_key
  elif [ -n "${SSH_PRIVATE_KEY:-}" ]; then
    echo "$SSH_PRIVATE_KEY" > /tmp/id_key && chmod 600 /tmp/id_key
  fi

  if [ -f /tmp/id_key ]; then
    SSH_PORT="${SSH_PORT:-22}"
    LOCAL_REDIS_PORT="${LOCAL_REDIS_PORT:-6379}"
    REMOTE_REDIS_PORT="${REMOTE_REDIS_PORT:-6379}"

    ssh -N \
      -i /tmp/id_key -p "$SSH_PORT" \
      -o ExitOnForwardFailure=yes \
      -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
      -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/tmp/known_hosts \
      -L "127.0.0.1:${LOCAL_REDIS_PORT}:localhost:${REMOTE_REDIS_PORT}" \
      "$SSH_TARGET" &
    TUNNEL_PID=$!
    echo "Redis tunnel started (PID: $TUNNEL_PID, Local port: $LOCAL_REDIS_PORT)"
  else
    echo "WARNING: Redis tunnel requested, but no /ssh/id_key or SSH_PRIVATE_KEY provided. Skipping tunnel."
  fi
fi

# デフォルトの REDIS_URL 設定（未設定時）
export REDIS_URL="${REDIS_URL:-redis://127.0.0.1:6379}"
export DB_PATH="${DB_PATH:-/app/data/tracker.db}"

# Cloud Run の公開ポート（デフォルト 8080）
export PORT="${PORT:-8080}"
export HOST="0.0.0.0"

# 3. バックグラウンド WebUI 群の内部起動（localhost 専用）
echo "--- Starting Internal WebUI Services ---"

# Top20 Tracker WebUI (Port 8003)
if [ "${ENABLE_TOP20:-true}" = "true" ]; then
  PORT=8003 deno run --allow-net --allow-env --allow-read src/top20_webui/main.ts > /tmp/top20_webui.log 2>&1 &
fi

# Price Monitor WebUI (Port 8005)
if [ "${ENABLE_PRICE_MONITOR:-true}" = "true" ]; then
  PORT=8005 deno run --allow-net --allow-env --allow-read src/price_monitor_webui/server.ts > /tmp/price_monitor_webui.log 2>&1 &
fi

# BTC DCA WebUI (Port 8007)
if [ "${ENABLE_BTC_DCA:-true}" = "true" ]; then
  PORT=8007 deno run --allow-net --allow-env --allow-read src/btc_dca_webui/server/main.ts > /tmp/btc_dca_webui.log 2>&1 &
fi

# Multi DCA WebUI (Port 8008)
if [ "${ENABLE_MULTI_DCA:-true}" = "true" ]; then
  PORT=8008 deno run --allow-net --allow-env --allow-read src/multi_dca_webui/server/main.ts > /tmp/multi_dca_webui.log 2>&1 &
fi

# BTC Grid WebUI (Port 8000)
if [ "${ENABLE_BTC_GRID:-true}" = "true" ]; then
  PORT=8000 deno run --allow-net --allow-env --allow-read src/btc_grid_webui/server.ts > /tmp/btc_grid_webui.log 2>&1 &
fi

# Surge Dip WebUI (Port 8004)
if [ "${ENABLE_SURGE_DIP:-true}" = "true" ]; then
  PORT=8004 deno run --allow-net --allow-env --allow-read src/surge_dip_webui/server/main.ts > /tmp/surge_dip_webui.log 2>&1 &
fi

# Slack Alert WebUI (Port 8010)
if [ "${ENABLE_SLACK_ALERT:-true}" = "true" ]; then
  PORT=8010 deno run --allow-net --allow-env --allow-read src/slack_alert_webui/main.ts > /tmp/slack_alert_webui.log 2>&1 &
fi

# Coin Trade WebUI (Port 8013)
if [ "${ENABLE_COIN_TRADE:-true}" = "true" ]; then
  PORT=8013 deno run --allow-net --allow-env --allow-read src/coin_trade_webui/webui/main.ts > /tmp/coin_trade_webui.log 2>&1 &
fi

# 4. バックグラウンド Bot & Worker 群の起動
echo "--- Starting Bot & Worker Daemons ---"

# Top20 Tracker Worker
if [ "${ENABLE_TOP20_WORKER:-true}" = "true" ]; then
  deno run --unstable-kv --allow-net --allow-read --allow-write --allow-env src/top20_worker/main.ts > /tmp/top20_worker.log 2>&1 &
fi

# Price Monitor Worker
if [ "${ENABLE_PRICE_MONITOR_WORKER:-true}" = "true" ]; then
  deno run --allow-net --allow-env --allow-read src/price_monitor/main.ts > /tmp/price_monitor.log 2>&1 &
fi

# BTC DCA Bot Worker
if [ "${ENABLE_BTC_DCA_BOT:-true}" = "true" ]; then
  deno run --unstable-kv --allow-net --allow-read --allow-write --allow-env src/btc_dca_bot/worker/main.ts > /tmp/btc_dca_bot.log 2>&1 &
fi

# BTC Grid Bot Worker
if [ "${ENABLE_BTC_GRID_BOT:-true}" = "true" ]; then
  deno run --unstable-kv --allow-net --allow-read --allow-write --allow-env src/btc_grid_bot/main.ts > /tmp/btc_grid_bot.log 2>&1 &
fi

# Surge Dip Bot Worker
if [ "${ENABLE_SURGE_DIP_BOT:-true}" = "true" ]; then
  deno run --unstable-kv --allow-net --allow-read --allow-write --allow-env src/surge_dip_bot/main.ts > /tmp/surge_dip_bot.log 2>&1 &
fi

# Multi DCA Bot Worker
if [ "${ENABLE_MULTI_DCA_BOT:-true}" = "true" ]; then
  deno run --unstable-kv --allow-net --allow-read --allow-write --allow-env src/multi_dca_bot/main.ts > /tmp/multi_dca_bot.log 2>&1 &
fi

# Slack Alert Sender Worker
if [ "${ENABLE_SLACK_ALERT_SENDER:-true}" = "true" ]; then
  deno run --allow-net --allow-env --allow-read src/slack_alert_sender/main.ts > /tmp/slack_alert_sender.log 2>&1 &
fi

# 5. メインゲートウェイ（統合ダッシュボード: PORT）をフォアグラウンド実行
echo "=== Starting Unified Dashboard Gateway on port $PORT ==="
exec deno run --allow-net --allow-env --allow-read src/dashboard_webui/server.ts
