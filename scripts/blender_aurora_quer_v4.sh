#!/bin/bash
# AURORA-Quervideo v4 (20.10.2026): Roehre ueber die GANZE Laufzeit als Tunnel sichtbar, Horn erst hinter dem Gesicht.
# Rendert nach frames_v4, resumable (Blender ueberspringt vorhandene Frames). Loescht nichts.
P=/mnt/c/Tools/blender_proj/aurora_quer
cd /home/bolla/workspace/scripts
TOT=5400
NAME=AURORA_Partikelvideo_Quer_3min_Tunnel_v4_ohne_Ton.mp4
touch $P/running.flag
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Tools\blender_proj\aurora_quer\keepawake.ps1' >/dev/null 2>&1 &
python3 -c "from job_status import report; report('aurora-quer-v4','AURORA-Quervideo Tunnel v4','laeuft','5400 Bilder 1080p, ca. 3,5 h')"
S=$(date +%s)
for try in 1 2 3 4; do
  n=$(ls $P/frames_v4/f_*.png 2>/dev/null | wc -l)
  [ "$n" -ge "$TOT" ] && break
  /mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\aurora_quer\aurora_quer3.py' -- anim 1 $TOT >> $P/render_v4.log 2>&1
done
n=$(ls $P/frames_v4/f_*.png 2>/dev/null | wc -l)
E=$(date +%s)
if [ "$n" -ge "$TOT" ]; then
  OUT=$P/$NAME
  ffmpeg -y -v error -framerate 30 -i $P/frames_v4/f_%04d.png -vf "fade=t=in:st=0:d=1.5,fade=t=out:st=178.5:d=1.5,format=yuv420p" -c:v libx264 -crf 16 -preset slow -movflags +faststart $OUT
  DST="/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer_Blender"; TMP=/mnt/d/OneDrive/Desktop/temp
  if [ -s "$OUT" ]; then
    cp "$OUT" "$DST/$NAME"; cp "$OUT" "$TMP/$NAME"
    /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "foreach(\$f in 'D:\OneDrive\Dokumente\Bolla\AURORA II\7_Trailer_Blender\\$NAME','D:\OneDrive\Desktop\temp\\$NAME'){ (Get-Item \$f).LastWriteTime = Get-Date }" >/dev/null 2>&1
    python3 -c "from job_status import report; report('aurora-quer-v4','AURORA-Quervideo Tunnel v4','ok','fertig in $((E-S)) s: Desktop\\\\temp\\\\$NAME')"
  else
    python3 -c "from job_status import report; report('aurora-quer-v4','AURORA-Quervideo Tunnel v4','fehler','ffmpeg lieferte keine Datei')"
  fi
else
  python3 -c "from job_status import report; report('aurora-quer-v4','AURORA-Quervideo Tunnel v4','fehler','nur $n von $TOT Bildern, Log aurora_quer/render_v4.log')"
fi
rm -f $P/running.flag
