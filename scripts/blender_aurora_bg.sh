#!/bin/bash
# AURORA-Hintergrund: Cover I (orange Punkte) -> Cover II (Nordlicht-Maedchen), 20 s, land + port
P=/mnt/c/Tools/blender_proj; B=/mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe
cd /home/bolla/workspace/scripts
for F in land port; do
  rm -rf $P/aurora_bg/$F; mkdir -p $P/aurora_bg/$F
  python3 -c "from job_status import report; report('blender-aurora-bg-$F','AURORA Punkte-Hintergrund ($F)','laeuft','480 Bilder')"
  S=$(date +%s)
  $B -b -P 'C:\Tools\blender_proj\aurora_bg.py' -- anim 1 $F "C:/Tools/blender_proj/aurora_bg/$F/" > $P/aurora_bg/render_$F.log 2>&1
  E=$(date +%s); n=$(ls $P/aurora_bg/$F/f_*.png 2>/dev/null | wc -l)
  if [ "$n" -ge 480 ]; then
    ffmpeg -y -v error -framerate 24 -i $P/aurora_bg/$F/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 16 $P/aurora_bg/AURORA_Punkte_Hintergrund_$F.mp4
    mkdir -p "/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer_Blender"
    cp $P/aurora_bg/AURORA_Punkte_Hintergrund_$F.mp4 "/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer_Blender/"
    cp $P/aurora_bg/AURORA_Punkte_Hintergrund_$F.mp4 /mnt/d/OneDrive/Desktop/temp/
    python3 -c "from job_status import report; report('blender-aurora-bg-$F','AURORA Punkte-Hintergrund ($F)','ok','fertig in $((E-S)) s, Desktop\\\\temp')"
  else
    python3 -c "from job_status import report; report('blender-aurora-bg-$F','AURORA Punkte-Hintergrund ($F)','fehler','nur $n von 480, Log aurora_bg/render_$F.log')"
  fi
done
