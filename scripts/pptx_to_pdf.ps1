param(
    [Parameter(Mandatory=$true)][string]$PptxPath,
    [Parameter(Mandatory=$true)][string]$PdfPath
)

# ppSaveAsPDF = 32. ExportAsFixedFormat scheitert an COM-Typkonvertierung (int->Object) - SaveAs ist robuster.
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres = $ppt.Presentations.Open($PptxPath, $null, $null, $false)
$pres.SaveAs($PdfPath, 32)
$pres.Close()
$ppt.Quit()

Write-Output "DONE: $PdfPath"
