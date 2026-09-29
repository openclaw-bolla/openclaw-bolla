param([Parameter(Mandatory=$true)][string]$Path)

function In($inches) { return [double]$inches * 72.0 }

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres = $ppt.Presentations.Open($Path, $false, $false, $true)

$slide = $pres.Slides.Item(3)
foreach ($shape in $slide.Shapes) {
    if ($shape.Name -eq "TextBox 3") {
        $shape.Left = In(1.0)
        $shape.Top = In(2.0)
        $shape.Width = In(11.3)
        $shape.Height = In(4.6)
        Write-Output "Folie 3 gefixt: Left=$($shape.Left) Top=$($shape.Top) W=$($shape.Width) H=$($shape.Height)"
    }
}

$pres.Save()
Write-Output "Gespeichert (Save, keine weiteren Operationen danach)."
Start-Sleep -Seconds 2
$pres.Close()
$ppt.Quit()
