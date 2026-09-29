param([Parameter(Mandatory=$true)][string]$Path)

"START" | Out-File -FilePath "C:\temp_debug.txt" -Encoding UTF8
try {
    $ppt = New-Object -ComObject PowerPoint.Application
    "PPT created" | Out-File -FilePath "C:\temp_debug.txt" -Append
    $ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
    $pres = $ppt.Presentations.Open($Path, $false, $false, $true)
    "Opened. Slides: $($pres.Slides.Count)" | Out-File -FilePath "C:\temp_debug.txt" -Append
    $slide = $pres.Slides.Item(3)
    "Got slide 3. Shapes: $($slide.Shapes.Count)" | Out-File -FilePath "C:\temp_debug.txt" -Append
    foreach ($shape in $slide.Shapes) {
        "Shape: $($shape.Name)" | Out-File -FilePath "C:\temp_debug.txt" -Append
        if ($shape.Name -eq "Textfeld 3") {
            "Found target shape. Left=$($shape.Left) Top=$($shape.Top)" | Out-File -FilePath "C:\temp_debug.txt" -Append
            try {
                $shape.Left = 72.0
                "Set Left OK, new value: $($shape.Left)" | Out-File -FilePath "C:\temp_debug.txt" -Append
            } catch {
                "ERROR setting Left: $($_.Exception.Message)" | Out-File -FilePath "C:\temp_debug.txt" -Append
            }
        }
    }
    $pres.Saved = [Microsoft.Office.Core.MsoTriState]::msoTrue
    $pres.Close()
    $ppt.Quit()
    "DONE" | Out-File -FilePath "C:\temp_debug.txt" -Append
} catch {
    "TOP-LEVEL ERROR: $($_.Exception.Message)" | Out-File -FilePath "C:\temp_debug.txt" -Append
}
