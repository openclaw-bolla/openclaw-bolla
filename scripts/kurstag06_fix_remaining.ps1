param([Parameter(Mandatory=$true)][string]$Path)

function In($inches) { return [double]$inches * 72.0 }
$CR = [char]13

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

# --- Folie 5 ---
Do-Fix -Label "Folie 5" -Action {
    param($pres)
    $slide = $pres.Slides.Item(5)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq "TextBox 2") {
            $shape.Left = In(1.9); $shape.Top = In(0.12); $shape.Width = In(9.5); $shape.Height = In(1.1)
            Write-Output "  TextBox2: L=$($shape.Left) T=$($shape.Top)"
        }
        if ($shape.Name -eq "TextBox 1") {
            $shape.Left = In(1.52); $shape.Top = In(1.5); $shape.Width = In(4.91); $shape.Height = In(5.85)
            Write-Output "  TextBox1: L=$($shape.Left) T=$($shape.Top)"
        }
        if ($shape.Name -eq "TextBox 3") {
            $shape.Left = In(7.45); $shape.Top = In(1.5); $shape.Width = In(5.47); $shape.Height = In(5.85)
            Write-Output "  TextBox3: L=$($shape.Left) T=$($shape.Top)"
        }
    }
}

# --- Folie 6 ---
Do-Fix -Label "Folie 6" -Action {
    param($pres)
    $slide = $pres.Slides.Item(6)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq "TextBox 2") {
            $shape.Left = In(0.80); $shape.Top = In(0.51); $shape.Width = In(5.55); $shape.Height = In(5.75)
            Write-Output "  TextBox2: L=$($shape.Left) T=$($shape.Top)"
        }
    }
}

# --- Folie 18 (neue Urheberrechts-Folie) ---
Do-Fix -Label "Folie 18" -Action {
    param($pres)
    $slide = $pres.Slides.Item(18)
    foreach ($shape in $slide.Shapes) {
        if ($shape.Name -eq "Title 1") {
            $shape.Left = In(1.0); $shape.Top = In(0.4); $shape.Width = In(11.3); $shape.Height = In(1.5)
            Write-Output "  Title1: L=$($shape.Left) T=$($shape.Top)"
        }
        if ($shape.Name -eq "TextBox 3") {
            $shape.Left = In(1.0); $shape.Top = In(2.1); $shape.Width = In(11.3); $shape.Height = In(5.0)
            Write-Output "  TextBox3: L=$($shape.Left) T=$($shape.Top)"
        }
    }
}

Write-Output "ALLES FERTIG."
