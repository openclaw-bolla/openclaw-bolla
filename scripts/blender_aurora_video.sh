#!/bin/bash
# AURORA-Video 3 min (Cover I fliegt durch die Roehre, explodiert zu Cover II) -> frames -> mp4 (ohne Ton)
# Resumable: Blender ueberspringt vorhandene Frames (use_overwrite=False). Wachhalte-Flag verhindert Standby.
P=/mnt/c/Tools/blender_proj/aurora_video
cd /home/bolla/workspace/scripts
TOT=3600
touch $P/running.flag
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Tools\blender_proj\aurora_video\keepawake.ps1' >/dev/null 2>&1 &
python3 -c "from job_status import report; report('aurora-video','AURORA-Video 3 min (Roehre, Cover I -> II)','laeuft','3600 Bilder 1080p, ca. 1,5-2 h')"
S=$(date +%s)
for try in 1 2 3 4; do
  n=$(ls $P/frames/f_*.png 2>/dev/null | wc -l)
  [ "$n" -ge "$TOT" ] && break
  /mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\aurora_video\aurora_video.py' -- anim 1 $TOT >> $P/render.log 2>&1
done
n=$(ls $P/frames/f_*.png 2>/dev/null | wc -l)
E=$(date +%s)
if [ "$n" -ge "$TOT" ]; then
  OUT=$P/AURORA_Video_3min_ohne_Ton.mp4
  ffmpeg -y -v error -framerate 24 -i $P/frames/f_%04d.png -vf "tpad=stop_mode=clone:stop_duration=30,fade=t=in:st=0:d=2,format=yuv420p" -c:v libx264 -crf 14 -preset slow -movflags +faststart $OUT
  cp $OUT "/mnt/d/OneDrive/Desktop/temp/AURORA_Video_3min_ohne_Ton.mp4"
  cp $OUT "/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer/Video/AURORA_Video_3min_ohne_Ton.mp4"
  python3 -c "from job_status import report; report('aurora-video','AURORA-Video 3 min (Roehre, Cover I -> II)','ok','fertig in $((E-S)) s: Desktop\\\\temp\\\\AURORA_Video_3min_ohne_Ton.mp4')"
else
  python3 -c "from job_status import report; report('aurora-video','AURORA-Video 3 min (Roehre, Cover I -> II)','fehler','nur $n von $TOT Bildern, Log C:\\\\Tools\\\\blender_proj\\\\aurora_video\\\\render.log')"
fi
rm -f $P/running.flag
