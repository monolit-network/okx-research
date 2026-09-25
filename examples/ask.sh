#!/usr/bin/env bash
# Synchronous question. Usage: X_API_KEY=... ./ask.sh "your question"
set -euo pipefail
Q=${1:-'Candles and current price for "OKB-USDT" on OKX - what is going on?'}
curl -s https://mcp.monolit.network/okx/v1/messages \
  -H "x-api-key: ${X_API_KEY:?set X_API_KEY}" \
  -H "content-type: application/json" \
  -d "$(python3 - "$Q" <<'PY'
import json, sys
print(json.dumps({
    "model": "okx-research",
    "max_cost_usd": 0.5,
    "messages": [{"role": "user", "content": sys.argv[1]}],
}))
PY
)" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['content'][0]['text']); print('---'); print('cost_usd:', d.get('usage',{}).get('cost_usd'), '| credits left:', d.get('_billing',{}).get('credits_remaining'))"
