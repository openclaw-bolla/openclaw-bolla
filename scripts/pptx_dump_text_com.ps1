param(
    [Parameter(Mandatory=$true)][string]$PptxPath,
    [Parameter(Mandatory=$true)][string]$OutTxt
)

if (-not (Test-Path $PptxPath)) {
    Write-Output "ERROR: file not found: $PptxPath"
    exit 1
}

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
try {
    $pres = $ppt.Presentations.Open($PptxPath, $true, $false, $true)
} catch {
    Write-Output "ERROR opening: $($_.Exception.Message)"
    exit 1
}
Write-Output "Opened. SlideCount raw: $($pres.Slides.Count)"

$lines = New-Object System.Collections.Generic.List[string]
for ($i = 1; $i -le $pres.Slides.Count; $i++) {
    $slide = $pres.Slides.Item($i)
    $lines.Add("=== Folie $i ===")
    foreach ($shape in $slide.Shapes) {
        $typeName = $shape.Type
        $hasPic = ($shape.Type -eq 13) -or ($shape.Type -eq 17 -and $shape.HasTextFrame -eq $false)
        if ($shape.Type -eq 13) {
            $lines.Add("[PICTURE] $($shape.Name)")
        } elseif ($shape.Type -eq 16) {
            $lines.Add("[OLE/EMBED] $($shape.Name)")
        } elseif ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
            $txt = $shape.TextFrame.TextRange.Text
            $lines.Add("[TEXT:$($shape.Name)] $txt")
        } else {
            $lines.Add("[SHAPE type=$typeName] $($shape.Name)")
        }
    }
}

$lines | Out-File -FilePath $OutTxt -Encoding UTF8

$pres.Close()
$ppt.Quit()
Write-Output "done: $($pres.Slides.Count) slides -> $OutTxt"
