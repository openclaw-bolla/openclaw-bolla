#!/bin/bash
# AURORA-Partikelvideo quer, NEUE ROEHRE (19.10.2026): gleichmaessige durchgehende Roehre mit Horn zum Gesicht.
# Rendert nach frames_v3 (alte Frames bleiben bis zum Erfolg). Resumable: Blender ueberspringt vorhandene Frames.
# Nach Erfolg: mp4 -> Desktop\temp + Bolla\AURORA II\7_Trailer_Blender, ALTE Versionen werden geloescht.
P=/mnt/c/Tools/blender_proj/aurora_quer
cd /home/bolla/workspace/scripts
TOT=5400
NAME=AURORA_Partikelvideo_Quer_3min_Roehrenflug_ohne_Ton.mp4
touch $P/running.flag
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Tools\blender_proj\aurora_quer\keepawake.ps1' >/dev/null 2>&1 &
python3 -c "from job_status import report; report('aurora-quer-flug','AURORA-Quervideo neue Roehre','laeuft','5400 Bilder 1080p, ca. 3,5 h')"
S=$(date +%s)
for try in 1 2 3 4; do
  n=$(ls $P/frames_v3/f_*.png 2>/dev/null | wc -l)
  [ "$n" -ge "$TOT" ] && break
  /mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\aurora_quer\aurora_quer2.py' -- anim 1 $TOT >> $P/render_v3.log 2>&1
done
n=$(ls $P/frames_v3/f_*.png 2>/dev/null | wc -l)
E=$(date +%s)
if [ "$n" -ge "$TOT" ]; then
  OUT=$P/$NAME
  ffmpeg -y -v error -framerate 30 -i $P/frames_v3/f_%04d.png -vf "fade=t=in:st=0:d=1.5,fade=t=out:st=178.5:d=1.5,format=yuv420p" -c:v libx264 -crf 16 -preset slow -movflags +faststart $OUT
  DST="/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer_Blender"
  TMP=/mnt/d/OneDrive/Desktop/temp
  if [ -s "$OUT" ]; then
    cp "$OUT" "$DST/$NAME"; cp "$OUT" "$TMP/$NAME"
    # alte Versionen weg (Chris-Regel 19.10.2026)
    rm -f "$DST/AURORA_Partikelvideo_Quer_3min_ohne_Ton.mp4" "$TMP/AURORA_Partikelvideo_Quer_3min_ohne_Ton.mp4" "$P/AURORA_Partikelvideo_Quer_3min_ohne_Ton.mp4" "$DST/AURORA_Partikelvideo_Quer_3min_neue_Roehre_ohne_Ton.mp4" "$TMP/AURORA_Partikelvideo_Quer_3min_neue_Roehre_ohne_Ton.mp4" "$P/AURORA_Partikelvideo_Quer_3min_neue_Roehre_ohne_Ton.mp4" "$P/frames_neu"
    rm -rf "$P/frames" "$P/frames_alt_ohne_roehre" "$P/frames_alt_tuerkis" "$P/stills" "$P/stills_neu" "$P/vorschau_I.png" "$P/vorschau_II.png"
    mv "$P/frames_v3" "$P/frames"
    /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "foreach(\$f in 'D:\OneDrive\Dokumente\Bolla\AURORA II\7_Trailer_Blender\\$NAME','D:\OneDrive\Desktop\temp\\$NAME'){ (Get-Item \$f).LastWriteTime = Get-Date }" >/dev/null 2>&1
    python3 -c "from job_status import report; report('aurora-quer-flug','AURORA-Quervideo neue Roehre','ok','fertig in $((E-S)) s: Desktop\\\\temp\\\\$NAME')"
  else
    python3 -c "from job_status import report; report('aurora-quer-flug','AURORA-Quervideo neue Roehre','fehler','ffmpeg lieferte keine Datei')"
  fi
else
  python3 -c "from job_status import report; report('aurora-quer-flug','AURORA-Quervideo neue Roehre','fehler','nur $n von $TOT Bildern, Log C:\\\\Tools\\\\blender_proj\\\\aurora_quer\\\\render_v3.log')"
fi
rm -f $P/running.flag
