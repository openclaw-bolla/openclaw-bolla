# Druckt die Osteoporose-Zentrum-Terminanfrage-Mail im Standard-Word-Format (Chris' Druck-Vorgabe)
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
$sel.TypeText("Terminanfrage Ersttermin - Osteoporose")
$sel.TypeParagraph()
$sel.TypeParagraph()

# Kopfzeilen
New-Line "Von" "renatemandel@wtnet.de"
New-Line "An" "info@osteoporose.hamburg"
New-Line "Betreff" "Terminanfrage Ersttermin - Osteoporose"
New-Line "Gesendet" "14.07.2026"
$sel.TypeParagraph()

# Abschnittsueberschrift
$sel.Font.Name = "Calibri"
$sel.Font.Size = 13
$sel.Font.Bold = $true
$sel.Font.ColorIndex = 3
$sel.TypeText("Nachricht")
$sel.TypeParagraph()

# Fliesstext
$sel.Font.Size = 11
$sel.Font.Bold = $false
$sel.Font.ColorIndex = 0
$sel.Font.Color = 0
$body = @"
Sehr geehrte Damen und Herren,

ich moechte gerne einen Ersttermin bei Ihnen vereinbaren, da bei mir kuerzlich radiologisch eine Osteoporose diagnostiziert wurde. Ueber die Online-Terminbuchung via Doctolib wird jedoch nur eine Knochendichtemessung angeboten, die bei mir bereits vorliegt - daher wende ich mich direkt per E-Mail an Sie.

Der vorliegende radiologische Befund lautet:
T-Wert: -3,8 (bestimmt im linken Schenkelhals)
Z-Wert: -2,3

Ich bitte um einen zeitnahen Termin und stehe fuer Rueckfragen gerne zur Verfuegung, auch telefonisch unter 0160-99182840.

Mit freundlichen Gruessen
Renate Mandel
"@
$sel.TypeText($body)

# Fusszeile
$footerRange = $doc.Sections.Item(1).Footers.Item(1).Range
$footerRange.Font.Name = "Calibri"
$footerRange.Font.Size = 9
$footerRange.Font.Color = 8421504
$footerRange.Text = "Gedruckt am 16.07.2026"

$word.ActivePrinter = "HPCE59BF (HP ENVY Inspire 7900 series)"
$doc.PrintOut()
Start-Sleep -Seconds 3
$doc.Close([ref]$false)
$word.Quit()
