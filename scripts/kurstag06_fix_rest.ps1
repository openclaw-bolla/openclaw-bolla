param([Parameter(Mandatory=$true)][string]$Path)

function Do-Fix {
    param([scriptblock]$Action, [string]$Label)
    $ppt = New-Object -ComObject PowerPoint.Application
    $ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
    $pres = $ppt.Presentations.Open($Path, $false, $false, $true)
    & $Action $pres
    $pres.Save()
    Write-Output "$Label gespeichert."
    Start-Sleep -Seconds 2
    $pres.Close()
    $ppt.Quit()
    Start-Sleep -Seconds 2
}

function Set-Text {
    param($pres, $slideIndex, $shapeName, $text)
    $slide = $pres.Slides.Item($slideIndex)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq $shapeName) {
            $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
            $shape.TextFrame.TextRange.Text = $text
            Write-Output "  $shapeName Text gesetzt"
        }
    }
}

Do-Fix -Label "Folie 9" -Action { param($pres) Set-Text $pres 9 "TextBox 2" "Import" }
Do-Fix -Label "Folie 10" -Action { param($pres) Set-Text $pres 10 "TextBox 2" "Clipchamp - direkt aufnehmen" }
Do-Fix -Label "Folie 11" -Action { param($pres) Set-Text $pres 11 "TextBox 2" "Aufzeichnen" }
Do-Fix -Label "Folie 12" -Action { param($pres) Set-Text $pres 12 "TextBox 2" "Clipchamp - Format & Gestalten" }
Do-Fix -Label "Folie 13" -Action { param($pres) Set-Text $pres 13 "TextBox 1" "Obere Spur ueberlagert die untere" }
Do-Fix -Label "Folie 14" -Action { param($pres) Set-Text $pres 14 "TextBox 14" "Dauer ueber die Seitenleiste einstellen" }
Do-Fix -Label "Folie 17" -Action { param($pres) Set-Text $pres 17 "TextBox 2" "Export" }
Do-Fix -Label "Folie 20 (Praktikum-Nummerierung)" -Action {
    param($pres)
    $CR = [char]13
    Set-Text $pres 20 "TextBox 8" (
        "Video mit dem Handy aufnehmen (Quick Settings / Kontrollzentrum)" + $CR +
        "Video schneiden - Android: Google Photos, iOS: Fotos-App" + $CR +
        "Fertiges Video auf den USB-Stick uebertragen" + $CR +
        "Genaue Schritt-fuer-Schritt-Anleitung: 06-Praktikum.html"
    )
}

Write-Output "ALLES FERTIG."
