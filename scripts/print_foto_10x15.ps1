param([string]$File,[switch]$Go)
Add-Type -AssemblyName System.Printing, PresentationFramework, PresentationCore, WindowsBase
$srv=New-Object System.Printing.LocalPrintServer
$q=$srv.GetPrintQueue('HPCE59BF (HP ENVY Inspire 7900 series)')
$delta=@'
<psf:PrintTicket xmlns:psf="http://schemas.microsoft.com/windows/2003/08/printing/printschemaframework" xmlns:psk="http://schemas.microsoft.com/windows/2003/08/printing/printschemakeywords" xmlns:ns0000="http://schemas.hp.com/ptpc/2006/1" version="1">
<psf:Feature name="psk:PageMediaSize"><psf:Option name="ns0000:HP_4X6_IN_10X15_CM"/></psf:Feature>
<psf:Feature name="psk:JobInputBin"><psf:Option name="ns0000:_6"/></psf:Feature>
<psf:Feature name="psk:PageMediaType"><psf:Option name="ns0000:_5_1069_0000_0_600x600"/></psf:Feature>
<psf:Feature name="psk:PageBorderless"><psf:Option name="psk:Borderless"/></psf:Feature>
<psf:Feature name="psk:PageOutputQuality"><psf:Option name="psk:High"/></psf:Feature>
<psf:Feature name="psk:PageOrientation"><psf:Option name="psk:Landscape"/></psf:Feature>
</psf:PrintTicket>
'@
$ms=New-Object System.IO.MemoryStream(,[Text.Encoding]::UTF8.GetBytes($delta))
$r=$q.MergeAndValidatePrintTicket($q.UserPrintTicket,$ms)
$t=$r.ValidatedPrintTicket
"ValidationResult: " + $r.ConflictStatus
"Bin=" + $t.InputBin + " Media=" + $t.PageMediaType + " Border=" + $t.PageBorderless + " Orient=" + $t.PageOrientation + " Quality=" + $t.OutputQuality
"Size=" + $t.PageMediaSize.PageMediaSizeName + " " + $t.PageMediaSize.Width + "x" + $t.PageMediaSize.Height
$xx=(New-Object System.IO.StreamReader($t.GetXmlStream())).ReadToEnd()
foreach($m in [regex]::Matches($xx,'<psf:Feature name="(psk:PageMediaSize|psk:JobInputBin|psk:PageMediaType)">\s*<psf:Option name="([^"]+)"')){ $m.Groups[1].Value + ' = ' + $m.Groups[2].Value }
$pd=New-Object System.Windows.Controls.PrintDialog
$pd.PrintQueue=$q; $pd.PrintTicket=$t
"Printable: " + $pd.PrintableAreaWidth + " x " + $pd.PrintableAreaHeight
if($Go){
 $bmp=New-Object System.Windows.Media.Imaging.BitmapImage
 $bmp.BeginInit(); $bmp.UriSource=New-Object Uri($File); $bmp.CacheOption='OnLoad'; $bmp.EndInit()
 $img=New-Object System.Windows.Controls.Image
 $img.Source=$bmp; $img.Stretch='Fill'
 $img.Width=$pd.PrintableAreaWidth; $img.Height=$pd.PrintableAreaHeight
 $img.Measure((New-Object System.Windows.Size($img.Width,$img.Height)))
 $img.Arrange((New-Object System.Windows.Rect(0,0,$img.Width,$img.Height)))
 $pd.PrintVisual($img,'GTA VI Gutschein Robin')
 "GESENDET"
}
