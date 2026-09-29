param(
    [Parameter(Mandatory=$true)][string]$SourcePath,
    [Parameter(Mandatory=$true)][string]$TargetPath
)

function In($inches) { return [double]$inches * 72.0 }
$CR = [char]13

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres = $ppt.Presentations.Open($SourcePath, $false, $false, $true)

function Set-Box {
    param($slideIndex, $shapeName, $text, $fontSize, $left, $top, $width, $height)
    $slide = $pres.Slides.Item($slideIndex)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq $shapeName) {
            $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
            $shape.TextFrame.TextRange.Text = $text
            if ($fontSize -ne $null) { $shape.TextFrame.TextRange.Font.Size = $fontSize }
            if ($left -ne $null)   { $shape.Left = In($left) }
            if ($top -ne $null)    { $shape.Top = In($top) }
            if ($width -ne $null)  { $shape.Width = In($width) }
            if ($height -ne $null) { $shape.Height = In($height) }
            Write-Output "OK Folie $slideIndex / $shapeName"
            return
        }
    }
    Write-Output "!! NICHT GEFUNDEN: Folie $slideIndex / $shapeName"
}

# Folie 1
Set-Box 1 "Title 1" ("Office Grundlagen" + $CR + "Videos & Clipchamp") $null $null $null $null $null

# Folie 2 (keine Aenderung noetig -- kein Platz, Video-Demos brauchen die Flaeche)

# Folie 3
Set-Box 3 "TextBox 3" (
    "Bordmittel von Windows 11 - keine Installation noetig" + $CR +
    "Kann nicht nur Screenshots, sondern auch den Bildschirm als Video aufnehmen" + $CR +
    [char]0x201E + "Snipping Tool" + [char]0x201C + " in die Suchleiste eintippen, oder Tastenkombination " + [char]0x229E + " Windows + Shift + S" + $CR +
    "Aufgenommenes Video wird automatisch als .mp4 gespeichert" + $CR +
    "Standard-Videoformat .mp4 - laeuft auf fast jedem Geraet, so wie .jpg bei Bildern"
) 24 1.0 2.0 11.3 4.6

# Folie 4
Set-Box 4 "Titel 1" (
    "Gamebar" + $CR +
    "Zweites Windows-Bordmittel zum Aufnehmen - ab Windows 10 eingebaut" + $CR +
    "Aufruf: " + [char]0x229E + " Windows + G" + $CR +
    "Urspruenglich fuers Aufnehmen beim Spielen gedacht, funktioniert aber fuer jedes Fenster"
) 22 1.20 0.55 3.35 6.70
$s4 = $pres.Slides.Item(4)
foreach ($shape in $s4.Shapes) {
    if ($shape.Name -eq "Titel 1") { $shape.TextFrame.TextRange.Paragraphs(1,1).Font.Size = 40 }
}

# Folie 5
Set-Box 5 "TextBox 2" "Video-Editing - die Grundlagen" 32 1.9 0.12 9.5 1.1
Set-Box 5 "TextBox 1" ("Bekannte Apps:" + $CR + "Clipchamp, CapCut, Canva, Adobe Premiere/AfterEffects, OBS ...") $null 1.52 1.5 4.91 5.85
Set-Box 5 "TextBox 3" (
    "Wichtigste Features, die (fast) jeder Editor kann:" + $CR +
    "Schneiden (Trimmen)" + $CR + "Vertonen" + $CR + "Filtern & Effekte" + $CR + "Green Screen"
) $null 7.45 1.5 5.47 5.85

# Folie 6
Set-Box 6 "TextBox 2" (
    "Microsoft Clipchamp" + $CR +
    "Nachfolger vom alten Windows Moviemaker" + $CR +
    "Kostenlos, aber: zum Erstellen/Speichern ist ein Microsoft-Konto noetig (nicht zum Anschauen fremder Videos)" + $CR +
    "Laeuft im Browser - clipchamp.com - noch nicht als App fuer Android/iOS" + $CR +
    "Andere Editoren ohne Kontopflicht: z. B. CapCut (weniger Export-Optionen)"
) 20 0.80 0.51 5.55 5.75

# Folie 7
Set-Box 7 "TextBox 6" ("Start mit:" + $CR + "Vorlage, oder" + $CR + "leerem Video, oder" + $CR + "KI-Vorschlag") $null $null $null $null $null

# Folie 8/9/10/11/12/17: Titel kurz halten
Set-Box 8 "TextBox 2" "Microsoft Clipchamp Oberflaeche" $null $null $null $null $null
Set-Box 8 "TextBox 26" "Medien-Uebersicht" $null $null $null $null $null
Set-Box 9 "TextBox 2" "Import" $null $null $null $null $null
Set-Box 10 "TextBox 2" "Clipchamp - direkt aufnehmen" $null $null $null $null $null
Set-Box 11 "TextBox 2" "Aufzeichnen" $null $null $null $null $null
Set-Box 11 "TextBox 8" "Video kann direkt in der Vorschau skaliert und platziert werden" $null $null $null $null $null
Set-Box 11 "TextBox 16" "Bildschirm und Webcam landen automatisch in zwei getrennten Videospuren" $null $null $null $null $null
Set-Box 12 "TextBox 2" "Clipchamp - Format & Gestalten" $null $null $null $null $null
Set-Box 13 "TextBox 1" "Obere Spur ueberlagert die untere" $null $null $null $null $null
Set-Box 14 "TextBox 14" "Dauer ueber die Seitenleiste einstellen" $null $null $null $null $null
Set-Box 15 "TextBox 2" "Green Screen Filter" $null $null $null $null $null
Set-Box 15 "Rectangle 7" "Hintergrund durch ein anderes Bild/Video ersetzen" 20 $null $null $null $null
Set-Box 16 "TextBox 2" "Automatische Untertitel" $null $null $null $null $null
Set-Box 16 "Rectangle 9" "Erkennt Sprache, erzeugt Text dazu" 16 $null $null $null $null
Set-Box 17 "TextBox 2" "Export" $null $null $null $null $null

Write-Output "--- Textedits fertig. Baue Urheberrechts-Folie (Duplikat von Folie 3) ---"

# Neue Urheberrechts-Folie: Duplikat von (bereits gefixter) Folie 3, hinter Folie 17 einsortiert -> Position 18
$dup = $pres.Slides.Item(3).Duplicate()
$newSlide = $dup.Item(1)
$newSlide.MoveTo(18)
foreach ($shape in $newSlide.Shapes) {
    if ($shape.Name -eq "Title 1") {
        $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
        $shape.TextFrame.TextRange.Text = [char]0x2696 + " Urheberrecht - was ihr wissen solltet"
        $shape.TextFrame.TextRange.Font.Size = 32
        $shape.Left = In(1.0); $shape.Top = In(0.4); $shape.Width = In(11.3); $shape.Height = In(1.5)
    }
    if ($shape.Name -eq "TextBox 3") {
        $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
        $shape.TextFrame.TextRange.Text = (
            [char]0x201E + "Fuer dich angucken und behalten - meist okay, wenn die Quelle legal ist. Hochladen oder weitergeben - das kann richtig teuer werden, und die Rechnung kriegen eure Eltern." + [char]0x201C + $CR +
            "Bildschirm mitschneiden ist rechtlich wie ein Download zu behandeln" + $CR +
            "Eigene Kopie fuer euch: meist okay, wenn die Quelle legal ist (z. B. offizieller YouTube-Kanal)" + $CR +
            "Weitergeben/Hochladen (Klassenchat, TikTok, YouTube ...): das kann teuer werden - und zahlen muessen eure Eltern" + $CR +
            "Deshalb im Praktikum: nur unbedenkliches Material aufnehmen"
        )
        $shape.TextFrame.TextRange.Font.Size = 22
        $shape.Left = In(1.0); $shape.Top = In(2.1); $shape.Width = In(11.3); $shape.Height = In(5.0)
    }
}
Write-Output "Neue Folie an Position 18 eingefuegt."

# Folie 20 = Praktikum (nach Einfuegen um 1 verschoben, vorher 19)
Set-Box 20 "TextBox 8" (
    "Video mit dem Handy aufnehmen (Quick Settings / Kontrollzentrum)" + $CR +
    "Video schneiden - Android: Google Photos, iOS: Fotos-App" + $CR +
    "Fertiges Video auf den USB-Stick uebertragen" + $CR +
    "Genaue Schritt-fuer-Schritt-Anleitung: 06-Praktikum.html"
) $null $null $null $null $null

Write-Output "--- Alles fertig. Speichere per SaveAs (robuster als Save() bei grosser Datei) ---"
$pres.SaveAs($TargetPath)
Write-Output "Gespeichert: $TargetPath"
$pres.Close()
$ppt.Quit()
