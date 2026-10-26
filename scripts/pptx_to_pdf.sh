#!/bin/bash
# PPTX -> PDF via PowerPoint-COM. Aufruf: pptx_to_pdf.sh <pptx> <pdf>  (Linux-Pfade)
# Das .ps1 liegt auf C: (nicht im WSL-Share), sonst blockt die Execution Policy.
set -eu
[ $# -eq 2 ] || { echo "Usage: $0 <pptx> <pdf>" >&2; exit 2; }
SRC=/home/bolla/workspace/scripts/pptx_to_pdf.ps1
DST=/mnt/c/Users/ernst/bolla_tools/pptx_to_pdf.ps1
cmp -s "$SRC" "$DST" || cp "$SRC" "$DST"
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -File 'C:\Users\ernst\bolla_tools\pptx_to_pdf.ps1' -PptxPath "$(wslpath -w "$1")" -PdfPath "$(wslpath -w "$2")"
