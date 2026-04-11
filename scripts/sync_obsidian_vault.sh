#!/bin/bash
# Sync Bolla's workspace to Obsidian Vault on Windows
# Kopiert nur .md Dateien + .obsidian Config

SRC="/home/bolla/workspace"
DST="/mnt/c/Bolla/Vault"

mkdir -p "$DST/memory" "$DST/mission-control"

# Markdown files im Root
cp "$SRC"/*.md "$DST/" 2>/dev/null

# Memory folder
cp "$SRC"/memory/*.md "$DST/memory/" 2>/dev/null

# Obsidian config (nur wenn neuer)
cp -r "$SRC/.obsidian" "$DST/" 2>/dev/null

echo "$(date '+%Y-%m-%d %H:%M:%S') Vault sync done"
