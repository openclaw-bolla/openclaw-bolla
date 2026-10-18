#!/bin/bash
# AURORA-Partikelvideo 3 min hochkant (Roehre -> Gesicht I -> Gesicht II) -> frames -> mp4 (ohne Ton)
# Resumable: Blender ueberspringt vorhandene Frames. Wachhalte-Flag verhindert Standby.
P=/mnt/c/Tools/blender_proj/aurora_partikel
cd /home/bolla/workspace/scripts
TOT=5400
touch $P/running.flag
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Tools\blender_proj\aurora_partikel\keepawake.ps1' >/dev/null 2>&1 &
python3 -c "from job_status import report; report('aurora-partikel','AURORA-Partikelvideo 3 min hochkant','laeuft','5400 Bilder 1080x1920, ca. 3,5 h')"
S=$(date +%s)
for try in 1 2 3 4; do
  n=$(ls $P/frames/f_*.png 2>/dev/null | wc -l)
  [ "$n" -ge "$TOT" ] && break
  /mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\aurora_partikel\aurora_partikel.py' -- anim 1 $TOT >> $P/render.log 2>&1
done
n=$(ls $P/frames/f_*.png 2>/dev/null | wc -l)
E=$(date +%s)
if [ "$n" -ge "$TOT" ]; then
  OUT=$P/AURORA_Partikelvideo_3min_hochkant_ohne_Ton.mp4
  ffmpeg -y -v error -framerate 30 -i $P/frames/f_%04d.png -vf "fade=t=in:st=0:d=1.5,fade=t=out:st=178.5:d=1.5,format=yuv420p" -c:v libx264 -crf 16 -preset slow -movflags +faststart $OUT
  DST="/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer_Blender"
  cp $OUT "$DST/"; cp $OUT /mnt/d/OneDrive/Desktop/temp/
  /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "(Get-Item 'D:\OneDrive\Dokumente\Bolla\AURORA II\7_Trailer_Blender\AURORA_Partikelvideo_3min_hochkant_ohne_Ton.mp4').LastWriteTime = Get-Date" >/dev/null 2>&1
  python3 -c "from job_status import report; report('aurora-partikel','AURORA-Partikelvideo 3 min hochkant','ok','fertig in $((E-S)) s: Desktop\\\\temp + Bolla\\\\AURORA II\\\\7_Trailer_Blender')"
else
  python3 -c "from job_status import report; report('aurora-partikel','AURORA-Partikelvideo 3 min hochkant','fehler','nur $n von $TOT Bildern, Log C:\\\\Tools\\\\blender_proj\\\\aurora_partikel\\\\render.log')"
fi
rm -f $P/running.flag
