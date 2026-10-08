#!/bin/bash
# Führt einen PowerShell-Befehl am Surface Book aus (SSH-Tunnel :2222, Fallback Heim-IP).
# Aufruf: book_ps.sh 'Get-PnpDevice -Class Bluetooth'
# Nutzt -EncodedCommand (UTF-16LE base64), da die Remote-Shell cmd ist.
set -u
[ $# -ge 1 ] || { echo "Usage: $0 '<PowerShell-Befehl>'" >&2; exit 2; }
enc=$(printf '%s' "$*" | iconv -f UTF-8 -t UTF-16LE | base64 -w0)
OPTS="-o ConnectTimeout=8 -o BatchMode=yes -i /home/bolla/.ssh/id_ed25519"
ssh $OPTS -p 2222 ernst@localhost "powershell -NoProfile -EncodedCommand $enc" 2>/dev/null \
  || ssh $OPTS ernst@192.168.178.38 "powershell -NoProfile -EncodedCommand $enc"
