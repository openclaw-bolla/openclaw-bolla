param(
    [Parameter(Mandatory=$true)][string]$Path
)

function In($inches) { return [double]$inches * 72.0 }

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres = $ppt.Presentations.Open($Path, $false, $false, $true)

$CR = [char]13
$ErrorActionPreference = "Stop"

# Test zuerst NUR an Folie 3, um das Muster zu verifizieren, bevor der Rest laeuft.
$slide = $pres.Slides.Item(3)
foreach ($shape in $slide.Shapes) {
    if ($shape.Name -eq "Textfeld 3") {
        $shape.Left = In(1.0)
        $shape.Top = In(2.0)
        $shape.Width = In(11.3)
        $shape.Height = In(4.6)
        $shape.TextFrame.WordWrap = [Microsoft.Office.Core.MsoTriState]::msoTrue
        $shape.TextFrame.TextRange.Text = (
            "Bordmittel von Windows 11 - keine Installation noetig" + $CR +
            "Kann nicht nur Screenshots, sondern auch den Bildschirm als Video aufnehmen" + $CR +
            [char]0x201E + "Snipping Tool" + [char]0x201C + " in die Suchleiste eintippen, oder Tastenkombination " + [char]0x229E + " Windows + Shift + S" + $CR +
            "Aufgenommenes Video wird automatisch als .mp4 gespeichert" + $CR +
            "Standard-Videoformat .mp4 - laeuft auf fast jedem Geraet, so wie .jpg bei Bildern"
        )
        $shape.TextFrame.TextRange.Font.Size = 24
        Write-Output "TEST OK: Folie 3 / Textfeld 3 -- Left=$($shape.Left) Top=$($shape.Top)"
    }
}

$pres.Saved = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres.Close()
$ppt.Quit()
