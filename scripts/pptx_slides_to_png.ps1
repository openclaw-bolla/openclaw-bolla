param(
    [Parameter(Mandatory=$true)][string]$PptxPath,
    [Parameter(Mandatory=$true)][string]$OutDir,
    [string]$Slides = ""  # comma-separated slide numbers, empty = all
)

if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($PptxPath, $true, $false, $false)

if ($Slides -ne "") {
    $nums = $Slides -split "," | ForEach-Object { [int]$_.Trim() }
} else {
    $nums = 1..$pres.Slides.Count
}

foreach ($n in $nums) {
    $slide = $pres.Slides.Item($n)
    $outPath = Join-Path $OutDir ("folie_{0:D2}.png" -f $n)
    $slide.Export($outPath, "PNG", 1600, 900)
    Write-Output "exported $outPath"
}

$pres.Close()
$ppt.Quit()
