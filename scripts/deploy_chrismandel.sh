#!/bin/bash
# Deploy chrismandel.de (Cloudflare Pages, Projekt "chrismandel") — nur nach Chris' Freigabe im Chat.
# Ablauf: EN-Paritäts-Check (Dauerregel 21.08.2026) -> wrangler pages deploy --branch=main
set -euo pipefail
W=/home/bolla/workspace
cd "$W/chrismandel-site"
bash scripts/check_en_parity.sh
export CLOUDFLARE_API_TOKEN="$(python3 -c "import json;print(json.load(open('$W/config/cloudflare_token.json'))['api_token'])")"
export CLOUDFLARE_ACCOUNT_ID=fdb35536a858c7fac78778c57625cd70
cd "$W"
npx wrangler pages deploy chrismandel-site --project-name=chrismandel --branch=main --commit-dirty=true
