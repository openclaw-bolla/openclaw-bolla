#!/bin/bash
# AURORA-II-Trailer Eevee-Test (10 s, 1080p) -> mp4 + Zeitmessung
P=/mnt/c/Tools/blender_proj
cd /home/bolla/workspace/scripts
rm -f $P/trailer_test/f_*.png
python3 -c "from job_status import report; report('blender-trailer','AURORA-II-Trailer Eevee-Test','laeuft','240 Bilder 1080p, Zeitmessung')"
S=$(date +%s)
/mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\trailer.py' -- anim > $P/trailer_render.log 2>&1
E=$(date +%s)
n=$(ls $P/trailer_test/f_*.png 2>/dev/null | wc -l)
ffmpeg -y -v error -framerate 24 -i $P/trailer_test/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 17 $P/trailer_test/trailer_test.mp4
echo "frames=$n sekunden=$((E-S))" > $P/trailer_test/zeit.txt
python3 -c "from job_status import report; report('blender-trailer','AURORA-II-Trailer Eevee-Test','ok','$n Bilder in $((E-S)) s')"
