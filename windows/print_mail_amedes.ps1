# Druckt die Amedes-Terminanfrage-Mail im Standard-Word-Format (Chris' Druck-Vorgabe)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Add()
$sel = $word.Selection

function New-Line($label, $value) {
    $sel.Font.Name = "Calibri"
    $sel.Font.Size = 11
    $sel.Font.Bold = $true
    $sel.Font.Color = 0
    $sel.TypeText("$label`: ")
    $sel.Font.Bold = $false
    $sel.Font.Color = 8421504  # grau
    $sel.TypeText($value)
    $sel.TypeParagraph()
}

# Titel
$sel.Font.Name = "Calibri"
$sel.Font.Size = 22
$sel.Font.Bold = $true
$sel.Font.Color = 0
$sel.TypeText("Terminanfrage Ersttermin internistische Endokrinologie")
$sel.TypeParagraph()
$sel.TypeParagraph()

# Kopfzeilen
New-Line "Von" "renatemandel@wtnet.de"
New-Line "An" "experts-hamburg@amedes-group.com"
New-Line "Betreff" "Terminanfrage Ersttermin internistische Endokrinologie - Osteoporose"
New-Line "Gesendet" "10.07.2026"
$sel.TypeParagraph()

# Abschnittsüberschrift
$sel.Font.Name = "Calibri"
$sel.Font.Size = 13
$sel.Font.Bold = $true
$sel.Font.ColorIndex = 3
$sel.TypeText("Nachricht")
$sel.TypeParagraph()

# Fließtext
$sel.Font.Size = 11
$sel.Font.Bold = $false
$sel.Font.ColorIndex = 0
$sel.Font.Color = 0
$body = @"
Sehr geehrte Damen und Herren,

ich moechte gerne einen Ersttermin in der internistischen Endokrinologie bei Ihnen vereinbaren, da bei mir kuerzlich radiologisch eine Osteoporose diagnostiziert wurde. Bei der Online-Terminbuchung ueber Clickdoc wird diese Terminart jedoch leider nicht zur Auswahl angeboten, daher wende ich mich direkt per E-Mail an Sie.

Der vorliegende radiologische Befund lautet:
T-Wert: -3,8 (bestimmt im linken Schenkelhals)
Z-Wert: -2,3

Ich bitte um einen zeitnahen Termin und stehe fuer Rueckfragen gerne zur Verfuegung.

Mit freundlichen Gruessen
Renate Mandel
"@
$sel.TypeText($body)

# Fusszeile
$footerRange = $doc.Sections.Item(1).Footers.Item(1).Range
$footerRange.Font.Name = "Calibri"
$footerRange.Font.Size = 9
$footerRange.Font.Color = 8421504
$footerRange.Text = "Gedruckt am 10.07.2026"

$word.ActivePrinter = "HPCE59BF (HP ENVY Inspire 7900 series)"
$doc.PrintOut()
Start-Sleep -Seconds 3
$doc.Close([ref]$false)
$word.Quit()
