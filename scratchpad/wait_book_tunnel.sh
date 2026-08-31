#!/bin/bash
# Wartet, bis der Surface-Book-Reverse-Tunnel (Port 2222) nach einem Neustart
# einmal weg war und wieder da ist. Gibt genau eine Zeile aus und endet.
seen_down=0
for i in $(seq 1 96); do
  if ss -tln 2>/dev/null | grep -q ':2222 '; then
    if [ "$seen_down" = "1" ]; then
      echo "TUNNEL BACK UP nach Book-Reboot (nach ~$((i*5))s)"
      exit 0
    fi
  else
    seen_down=1
  fi
  sleep 5
done
if ss -tln 2>/dev/null | grep -q ':2222 '; then
  echo "TIMEOUT nach 8min - Tunnel UP, aber Neustart nie erkannt (seen_down=$seen_down)"
else
  echo "TIMEOUT nach 8min - Tunnel DOWN, Book noch nicht zurueck"
fi
