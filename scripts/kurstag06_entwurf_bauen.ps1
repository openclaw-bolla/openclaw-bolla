param(
    [Parameter(Mandatory=$true)][string]$SourcePath,
    [Parameter(Mandatory=$true)][string]$TargetPath
)

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres = $ppt.Presentations.Open($SourcePath, $false, $false, $true)

function Set-ShapeText {
    param($slideIndex, $shapeName, $newText)
    $slide = $pres.Slides.Item($slideIndex)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq $shapeName) {
            $shape.TextFrame.TextRange.Text = $newText
            Write-Output "OK Folie $slideIndex / $shapeName"
            return
        }
    }
    Write-Output "!! NICHT GEFUNDEN: Folie $slideIndex / $shapeName"
}

$CR = [char]13

# Folie 1: Titel um Untertitel ergaenzen
Set-ShapeText 1 "Title 1" ("Office Grundlagen" + $CR + "Videos & Clipchamp")

# Folie 2: Intro-Text in die Titel-Textbox
Set-ShapeText 2 "TextBox 2" (
    "Microsoft Clipchamp" + $CR +
    "Video-Editor - heute unser Werkzeug fuer eigene Videos" + $CR +
    "Damit machen Leute Videos fuer YouTube, TikTok, Instagram ..." + $CR +
    "Genauso gut fuer Praesentationen in der Schule oder im Studium" + $CR +
    "Die Grundideen gelten auch in anderen Programmen (CapCut, Canva, Premiere ...)"
)

# Folie 3: Snipping Tool Bullets
Set-ShapeText 3 "TextBox 3" (
    "Bordmittel von Windows 11 - keine Installation noetig" + $CR +
    "Kann nicht nur Screenshots, sondern auch den Bildschirm als Video aufnehmen" + $CR +
    [char]0x201E + "Snipping Tool" + [char]0x201C + " in die Suchleiste eintippen, oder Tastenkombination " + [char]0x229E + " Windows + Shift + S" + $CR +
    "Aufgenommenes Video wird automatisch als .mp4 gespeichert" + $CR +
    "Standard-Videoformat .mp4 - laeuft auf fast jedem Geraet (PC, Handy, Tablet), so wie .jpg bei Bildern"
)

# Folie 4: Gamebar - Titel um Bullets ergaenzen
Set-ShapeText 4 "Titel 1" (
    "Gamebar" + $CR +
    "Zweites Windows-Bordmittel zum Aufnehmen - ab Windows 10 eingebaut" + $CR +
    "Aufruf: " + [char]0x229E + " Windows + G" + $CR +
    "Urspruenglich fuers Aufnehmen beim Spielen gedacht, funktioniert aber fuer jedes Fenster"
)

# Folie 5: Video Editing Grundlagen
Set-ShapeText 5 "TextBox 2" "Video-Editing - die Grundlagen"
Set-ShapeText 5 "TextBox 1" ("Bekannte Apps:" + $CR + "Clipchamp, CapCut, Canva, Adobe Premiere/AfterEffects, OBS ...")
Set-ShapeText 5 "TextBox 3" (
    "Wichtigste Features, die (fast) jeder Editor kann:" + $CR +
    "Schneiden (Trimmen)" + $CR +
    "Vertonen" + $CR +
    "Filtern & Effekte" + $CR +
    "Green Screen"
)

# Folie 6: Clipchamp Start (Teil 1)
Set-ShapeText 6 "TextBox 2" (
    "Microsoft Clipchamp" + $CR +
    "Nachfolger vom alten Windows Moviemaker" + $CR +
    "Kostenlos, aber: zum Erstellen/Speichern ist ein Microsoft-Konto noetig (nicht zum Anschauen fremder Videos)" + $CR +
    "Laeuft im Browser - clipchamp.com - noch nicht als App fuer Android/iOS" + $CR +
    "Andere bekannte Editoren ohne diese Kontopflicht: z. B. CapCut (dafuer weniger Export-Optionen)"
)

# Folie 7: Start mit ...
Set-ShapeText 7 "TextBox 6" ("Start mit:" + $CR + "Vorlage, oder" + $CR + "leerem Video, oder" + $CR + "KI-Vorschlag")

# Folie 8: Oberflaeche
Set-ShapeText 8 "TextBox 2" (
    "Microsoft Clipchamp Oberflaeche" + $CR +
    "Drei Grundbereiche: Vorschau (Mitte), Spuren (unten), Medien-Uebersicht (links)" + $CR +
    "Rechts oben: Kontextmenue mit Features zum ausgewaehlten Objekt"
)
Set-ShapeText 8 "TextBox 26" "Medien-Uebersicht"

# Folie 9: Import
Set-ShapeText 9 "TextBox 2" (
    "Import" + $CR +
    "Import moeglich: eigene Dateien, oder direkt vom Handy" + $CR +
    "Shortcuts lassen sich in der App anzeigen - z. B. S fuers Schneiden"
)

# Folie 10: direkt aufnehmen (Teil 1)
Set-ShapeText 10 "TextBox 2" ("Clipchamp - direkt aufnehmen" + $CR + "Auswahl zwischen Bildschirm- und Webcam-Aufnahme")

# Folie 11: direkt aufnehmen (Teil 2)
Set-ShapeText 11 "TextBox 2" "Clipchamp - direkt aufnehmen"
Set-ShapeText 11 "TextBox 8" "Video kann direkt in der Vorschau skaliert und platziert werden"
Set-ShapeText 11 "TextBox 16" "Bildschirm und Webcam landen automatisch in zwei getrennten Videospuren"

# Folie 12: Format & Gestalten (Teil 1: Seitenverhaeltnis)
Set-ShapeText 12 "TextBox 2" (
    "Clipchamp - Format & Gestalten" + $CR +
    "Seitenverhaeltnis je nach Ziel waehlbar: Instagram Reels/Story, TikTok, Post, Breitbild-TV, Computer-Monitor ..."
)

# Folie 13: Video-/Audiospuren
Set-ShapeText 13 "TextBox 1" "Video-/Audiospuren liegen uebereinander - die obere Spur ueberlagert die untere"

# Folie 14: Uebergaenge
Set-ShapeText 14 "TextBox 14" "Uebergaenge (Transitions) zwischen Clips einfuegen, Dauer ueber die Seitenleiste einstellen"

# Folie 15: Green Screen
Set-ShapeText 15 "TextBox 2" "Green-Screen-Filter: Hintergrund durch ein anderes Bild/Video ersetzen"

# Folie 16: Automatische Untertitel
Set-ShapeText 16 "TextBox 2" (
    "Automatische Untertitel: Clipchamp erkennt Sprache und erzeugt Text dazu" + $CR +
    "Green Screen & Untertitel heute nur kurz zeigen - zum spaeteren Selbst-Ausprobieren, nicht Teil des Praktikums"
)

# Folie 17: Export
Set-ShapeText 17 "TextBox 2" (
    "Export" + $CR +
    "Qualitaet auswaehlen -> Clipchamp beginnt automatisch mit dem Rendern" + $CR +
    "Direktes Teilen zu manchen Plattformen moeglich (z. B. YouTube), bei anderen nur per Link (z. B. Facebook)"
)

# Folie 19: Praktikum-Text bereinigen
Set-ShapeText 19 "TextBox 8" (
    "1. Video mit dem Handy aufnehmen (Quick Settings / Kontrollzentrum)" + $CR +
    "2. Video schneiden - Android: Google Photos, iOS: Fotos-App" + $CR +
    "3. Fertiges Video auf den USB-Stick uebertragen" + $CR +
    "Genaue Schritt-fuer-Schritt-Anleitung: 06-Praktikum.html"
)

Write-Output "--- Text-Edits fertig. Baue neue Urheberrechts-Folie (Duplikat von Folie 3) ---"

# Neue Folie fuer Urheberrecht: Folie 3 (Titel+Text, keine Bilder) duplizieren, hinter Folie 17 (Export) einsortieren
$dup = $pres.Slides.Item(3).Duplicate()
$newSlide = $dup.Item(1)
$newSlide.MoveTo(18)

foreach ($shape in $newSlide.Shapes) {
    if ($shape.Name -eq "Title 1") {
        $shape.TextFrame.TextRange.Text = [char]0x2696 + " Urheberrecht - was ihr wissen solltet"
    }
    if ($shape.Name -eq "TextBox 3") {
        $shape.TextFrame.TextRange.Text = (
            [char]0x201E + "Fuer dich angucken und behalten - meist okay, wenn die Quelle legal ist. Hochladen oder weitergeben - das kann richtig teuer werden, und die Rechnung kriegen eure Eltern." + [char]0x201C + $CR +
            "Bildschirm mitschneiden ist rechtlich wie ein Download zu behandeln" + $CR +
            "Eigene Kopie fuer euch: meist okay, wenn die Quelle legal ist (z. B. offizieller YouTube-Kanal)" + $CR +
            "Weitergeben/Hochladen (Klassenchat, TikTok, YouTube ...): das kann teuer werden - und zahlen muessen eure Eltern" + $CR +
            "Deshalb im Praktikum: nur unbedenkliches Material aufnehmen (euer eigenes Handy-Display, eigenes Gameplay, eigene kleine Praesentation)"
        )
    }
}
Write-Output "Neue Folie an Position 18 eingefuegt."

$pres.SaveAs($TargetPath)
Write-Output "Gespeichert nach: $TargetPath"
$pres.Close()
$ppt.Quit()
