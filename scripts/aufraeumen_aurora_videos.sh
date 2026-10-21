#!/bin/bash
# AURORA-Video-Aufraeumen (neu 21.10.2026). Behaelt ALLES, was man zum Neu-Rendern/Verbessern braucht
# (Blender-Skripte, data.npz, Prep-Skript, Wrapper, Vorschau-Bilder, Endvideo v5) und loescht nur
# regenerierbare Rohbilder (PNG-Frames), verworfene Videos und Logs.
B=/mnt/c/Tools/blender_proj
Q=$B/aurora_quer
T="/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer_Blender"
D=/mnt/d/OneDrive/Desktop/temp
V5=AURORA_Partikelvideo_Quer_3min_Tunnel_v5_ohne_Ton.mp4
[ -s "$T/$V5" ] || { echo "v5-Video fehlt im Trailer-Ordner - Abbruch"; exit 1; }

# 1) Arbeitsstand sichern: Skripte, Daten, Wrapper in einen Ordner neben dem Video (klein, ~10 MB)
A="$T/_Arbeitsstand_Quervideo_v5"; mkdir -p "$A"
cp -f $Q/aurora_quer4.py $Q/aurora_quer3.py $Q/aurora_quer2.py $Q/aurora_quer.py $Q/data.npz $Q/keepawake.ps1 "$A/"
cp -f /home/bolla/workspace/scripts/aurora_quer_prep.py /home/bolla/workspace/scripts/blender_aurora_quer_v5.sh "$A/"
cp -f $Q/stills_v5/*.png "$A/" 2>/dev/null
cat > "$A/LIES_MICH.txt" <<'EOT'
Quer-Video AURORA (3 Min, 1080p, 30 fps) - Arbeitsstand v5 (21.10.2026)
Neu rendern / verbessern:
 1. aurora_quer_prep.py <Spalten> erzeugt data.npz (Punktwolken aus Cover I + Cover II; v5 = 1250 Spalten, ~103k Punkte).
    Pfade im Skript: Cover I/II (Cover-Datei bei neuem AURORA-II-Cover anpassen), Ausgabe nach C:\Tools\blender_proj\aurora_quer\.
 2. aurora_quer4.py = Blender-Szene (Roehre, Punkte, Wandlung orange->Nordlicht, Kamera). Testbild:
    blender.exe -b -P aurora_quer4.py -- still 2300 5399   | Voll: ... -- anim 1 5400  (frames_v5, ~4 h)
 3. blender_aurora_quer_v5.sh = Wrapper (resumable, ffmpeg-Encode, Kopie). Dateien dafuer nach C:\Tools\blender_proj\aurora_quer\ legen.
Ordner C:\Tools\blender_proj\aurora_quer\ muss existieren (BASE-Pfad in aurora_quer4.py).
EOT

# 2) verworfene Videos
rm -f "$T/AURORA_Partikelvideo_3min_hochkant_ohne_Ton.mp4" "$T/AURORA_Video_3min_ohne_Ton.mp4" \
      "$T/AURORA_Partikelvideo_Quer_3min_Roehrenflug_ohne_Ton.mp4" "$T/AURORA_Partikelvideo_Quer_3min_Tunnel_v4_ohne_Ton.mp4" \
      "$D/AURORA_Partikelvideo_Quer_3min_Roehrenflug_ohne_Ton.mp4" "$D/AURORA_Partikelvideo_Quer_3min_Tunnel_v4_ohne_Ton.mp4" \
      $B/aurora_partikel/AURORA_Partikelvideo_3min_hochkant_ohne_Ton.mp4 $B/aurora_video/AURORA_Video_3min_ohne_Ton.mp4 \
      $Q/AURORA_Partikelvideo_Quer_3min_Roehrenflug_ohne_Ton.mp4 $Q/AURORA_Partikelvideo_Quer_3min_Tunnel_v4_ohne_Ton.mp4

# 3) Rohbilder (PNG-Frames), alte Stills und Logs - alles per Skript reproduzierbar (Skripte + data.npz bleiben)
rm -rf $B/aurora_partikel/frames $B/aurora_partikel/stills $B/aurora_video/frames $B/aurora_video/stills \
       $B/aurora_bg/land $B/aurora_bg/port $B/frames $B/frames_hq $B/trailer_test $B/trailer_face \
       $B/render.log $B/render_hq.log $B/hq_9x16.mp4 $B/hq_16x9.mp4 \
       $Q/frames $Q/frames_v3 $Q/frames_v4 $Q/frames_v5 $Q/stills_v3 $Q/stills_v4 \
       $Q/render.log $Q/render_neu.log $Q/render_v3.log $Q/render_v4.log
echo fertig; ls "$A"; df -h /mnt/c | tail -1
