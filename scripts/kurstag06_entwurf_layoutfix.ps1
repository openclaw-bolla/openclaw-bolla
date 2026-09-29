param(
    [Parameter(Mandatory=$true)][string]$Path
)

function In($inches) { return $inches * 72.0 }

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres = $ppt.Presentations.Open($Path, $false, $false, $true)

$CR = [char]13

function Get-Shape($slideIndex, $shapeName) {
    $slide = $pres.Slides.Item($slideIndex)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq $shapeName) { return $shape }
    }
    Write-Output "!! NICHT GEFUNDEN: Folie $slideIndex / $shapeName"
    return $null
}

function Set-Box($slideIndex, $shapeName, $text, $fontSize, $left, $top, $width, $height) {
    $shape = Get-Shape $slideIndex $shapeName
    if ($null -eq $shape) { return }
    if ($left -ne $null) { $shape.Left = In($left) }
    if ($top -ne $null) { $shape.Top = In($top) }
    if ($width -ne $null) { $shape.Width = In($width) }
    if ($height -ne $null) { $shape.Height = In($height) }
    $tf = $shape.TextFrame
    $tf.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
    $tf.AutoSize = 1  # ppAutoSizeTextToFitShape (Schrumpf-Sicherheitsnetz)
    $tf.TextRange.Text = $text
    if ($fontSize -ne $null) { $tf.TextRange.Font.Size = $fontSize }
    Write-Output "OK Folie $slideIndex / $shapeName"
}

# --- Folie 2: zurueck auf Original (kein Platz fuer Zusatztext, Video-Demos brauchen die Flaeche) ---
Set-Box 2 "Textfeld 2" "Microsoft Clipchamp" 32 $null $null $null $null

# --- Folie 3: Bullets in freien Bereich zwischen Titel und unterem Rand ---
Set-Box 3 "Textfeld 3" (
    "Bordmittel von Windows 11 - keine Installation noetig" + $CR +
    "Kann nicht nur Screenshots, sondern auch den Bildschirm als Video aufnehmen" + $CR +
    [char]0x201E + "Snipping Tool" + [char]0x201C + " in die Suchleiste eintippen, oder Tastenkombination " + [char]0x229E + " Windows + Shift + S" + $CR +
    "Aufgenommenes Video wird automatisch als .mp4 gespeichert" + $CR +
    "Standard-Videoformat .mp4 - laeuft auf fast jedem Geraet, so wie .jpg bei Bildern"
) 24 1.0 2.0 11.3 4.6

# --- Folie 4: Titel-Box zur vollen linken Spalte machen, Ueberschrift gross, Bullets klein ---
$s4 = Get-Shape 4 "Titel 1"
if ($s4 -ne $null) {
    $s4.Left = In(1.20); $s4.Top = In(0.55); $s4.Width = In(3.35); $s4.Height = In(6.70)
    $tf4 = $s4.TextFrame
    $tf4.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
    $tf4.AutoSize = 1
    $tf4.TextRange.Text = (
        "Gamebar" + $CR +
        "Zweites Windows-Bordmittel zum Aufnehmen - ab Windows 10 eingebaut" + $CR +
        "Aufruf: " + [char]0x229E + " Windows + G" + $CR +
        "Urspruenglich fuers Aufnehmen beim Spielen gedacht, funktioniert aber fuer jedes Fenster"
    )
    $tf4.TextRange.Paragraphs(1).Font.Size = 40
    $tf4.TextRange.Paragraphs(2,3).Font.Size = 22
    Write-Output "OK Folie 4 / Titel 1"
}

# --- Folie 5: Titeltext verbreitern (verhindert Umbruch -> Ueberlappung), Inhaltsboxen leicht nach unten ---
Set-Box 5 "Textfeld 2" "Video-Editing - die Grundlagen" 32 1.9 0.12 9.5 1.1
Set-Box 5 "Textfeld 1" ("Bekannte Apps:" + $CR + "Clipchamp, CapCut, Canva, Adobe Premiere/AfterEffects, OBS ...") $null 1.52 1.5 4.91 5.85
Set-Box 5 "Textfeld 3" (
    "Wichtigste Features, die (fast) jeder Editor kann:" + $CR +
    "Schneiden (Trimmen)" + $CR +
    "Vertonen" + $CR +
    "Filtern & Effekte" + $CR +
    "Green Screen"
) $null 7.45 1.5 5.47 5.85

# --- Folie 6: schmaler (bleibt links vom Bild), kleinere Schrift, mehr Hoehe ---
Set-Box 6 "Textfeld 2" (
    "Microsoft Clipchamp" + $CR +
    "Nachfolger vom alten Windows Moviemaker" + $CR +
    "Kostenlos, aber: zum Erstellen/Speichern ist ein Microsoft-Konto noetig (nicht zum Anschauen fremder Videos)" + $CR +
    "Laeuft im Browser - clipchamp.com - noch nicht als App fuer Android/iOS" + $CR +
    "Andere Editoren ohne Kontopflicht: z. B. CapCut (weniger Export-Optionen)"
) 20 0.80 0.51 5.55 5.75

# --- Folie 8/9/10/12/17: Diagramm-Folien - Titel kurz halten, keine Zusatz-Bullets (Platz fehlt) ---
Set-Box 8 "TextBox 2" "Microsoft Clipchamp Oberflaeche" $null $null $null $null $null
Set-Box 8 "TextBox 26" "Medien-Uebersicht" $null $null $null $null $null
Set-Box 9 "TextBox 2" "Import" $null $null $null $null $null
Set-Box 10 "TextBox 2" "Clipchamp - direkt aufnehmen" $null $null $null $null $null
Set-Box 11 "TextBox 2" "Aufzeichnen" $null $null $null $null $null
Set-Box 12 "TextBox 2" "Clipchamp - Format & Gestalten" $null $null $null $null $null
Set-Box 17 "TextBox 2" "Export" $null $null $null $null $null

# --- Folie 11: Callout-Boxen leicht kuerzer fassen (Originalgroesse beibehalten) ---
Set-Box 11 "TextBox 8" "Video kann direkt in der Vorschau skaliert und platziert werden" $null $null $null $null $null
Set-Box 11 "TextBox 16" "Bildschirm und Webcam landen automatisch in zwei getrennten Videospuren" $null $null $null $null $null

# --- Folie 13/14: Callout-Boxen kurz halten (Originalgroesse) ---
Set-Box 13 "TextBox 1" "Obere Spur ueberlagert die untere" $null $null $null $null $null
Set-Box 14 "TextBox 14" "Dauer ueber die Seitenleiste einstellen" $null $null $null $null $null

# --- Folie 15: Titel kurz, Erklaerung in die VORHANDENE leere Sprechblase (Rechteck 7) ---
Set-Box 15 "TextBox 2" "Green Screen Filter" $null $null $null $null $null
Set-Box 15 "Rechteck 7" "Hintergrund durch ein anderes Bild/Video ersetzen" 20 $null $null $null $null

# --- Folie 16: Titel kurz, Erklaerung in die VORHANDENE leere Box (Rechteck 9) ---
Set-Box 16 "TextBox 2" "Automatische Untertitel" $null $null $null $null $null
Set-Box 16 "Rechteck 9" "Erkennt Sprache, erzeugt Text dazu" 16 $null $null $null $null

# --- Folie 19: doppelte Nummerierung entfernen (Platzhalter nummeriert schon automatisch) ---
Set-Box 19 "TextBox 8" (
    "Video mit dem Handy aufnehmen (Quick Settings / Kontrollzentrum)" + $CR +
    "Video schneiden - Android: Google Photos, iOS: Fotos-App" + $CR +
    "Fertiges Video auf den USB-Stick uebertragen" + $CR +
    "Genaue Schritt-fuer-Schritt-Anleitung: 06-Praktikum.html"
) $null $null $null $null $null

# --- Folie 18: neue Urheberrechts-Folie - Titel- und Textbox vergroessern/repositionieren ---
$t18 = Get-Shape 18 "Title 1"
if ($t18 -ne $null) {
    $t18.Left = In(1.0); $t18.Top = In(0.4); $t18.Width = In(11.3); $t18.Height = In(1.5)
    $tf = $t18.TextFrame
    $tf.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
    $tf.AutoSize = 1
    $tf.TextRange.Text = [char]0x2696 + " Urheberrecht - was ihr wissen solltet"
    $tf.TextRange.Font.Size = 32
    Write-Output "OK Folie 18 / Title 1"
}
Set-Box 18 "TextBox 3" (
    [char]0x201E + "Fuer dich angucken und behalten - meist okay, wenn die Quelle legal ist. Hochladen oder weitergeben - das kann richtig teuer werden, und die Rechnung kriegen eure Eltern." + [char]0x201C + $CR +
    "Bildschirm mitschneiden ist rechtlich wie ein Download zu behandeln" + $CR +
    "Eigene Kopie fuer euch: meist okay, wenn die Quelle legal ist (z. B. offizieller YouTube-Kanal)" + $CR +
    "Weitergeben/Hochladen (Klassenchat, TikTok, YouTube ...): das kann teuer werden - und zahlen muessen eure Eltern" + $CR +
    "Deshalb im Praktikum: nur unbedenkliches Material aufnehmen"
) 22 1.0 2.1 11.3 5.0

$pres.Save()
Write-Output "Gespeichert (ueberschrieben): $Path"
$pres.Close()
$ppt.Quit()
