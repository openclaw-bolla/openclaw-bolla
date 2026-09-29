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

Do-Fix -Label "Folie 15" -Action {
    param($pres)
    $slide = $pres.Slides.Item(15)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq "TextBox 2") {
            $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
            $shape.TextFrame.TextRange.Text = "Green Screen Filter"
            Write-Output "  TextBox2 Text gesetzt"
        }
        if ($shape.Name -eq "Rectangle 7") {
            $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
            $shape.TextFrame.TextRange.Text = "Hintergrund durch ein anderes Bild/Video ersetzen"
            $shape.TextFrame.TextRange.Font.Size = 20
            Write-Output "  Rectangle7 Text gesetzt"
        }
    }
}

Do-Fix -Label "Folie 16" -Action {
    param($pres)
    $slide = $pres.Slides.Item(16)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq "TextBox 2") {
            $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
            $shape.TextFrame.TextRange.Text = "Automatische Untertitel"
            Write-Output "  TextBox2 Text gesetzt"
        }
        if ($shape.Name -eq "Rectangle 9") {
            $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
            $shape.TextFrame.TextRange.Text = "Erkennt Sprache, erzeugt Text dazu"
            $shape.TextFrame.TextRange.Font.Size = 16
            Write-Output "  Rectangle9 Text gesetzt"
        }
    }
}

Write-Output "ALLES FERTIG."
