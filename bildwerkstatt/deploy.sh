#!/bin/bash
# Veröffentlicht die Bild-Werkstatt für alle Klassen (je eigenes Pages-Projekt, gleicher Code).
set -euo pipefail
H=$(cd "$(dirname "$0")" && pwd); W=$(dirname "$H")
export CLOUDFLARE_API_TOKEN="$(python3 -c "import json;print(json.load(open('$W/config/cloudflare_token.json'))['api_token'])")"
export CLOUDFLARE_ACCOUNT_ID="$(python3 -c "import json;print(json.load(open('$W/config/cloudflare_token.json'))['account_id'])")"
for k in ${1:-7a 7b 7c 7d}; do
  T=$(mktemp -d); cp -r "$H/public" "$H/functions" "$H/wrangler.toml" "$T/"
  sed -i "s/bildwerkstatt-7c/bildwerkstatt-$k/" "$T/wrangler.toml"
  (cd "$T" && npx --prefix "$W" wrangler pages deploy --project-name="bildwerkstatt-$k" --branch=main --commit-dirty=true | tail -2)
  rm -rf "$T"
done
