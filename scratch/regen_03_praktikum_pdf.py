from weasyprint import HTML
base = '/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts/Praktikum/'
HTML(base + '03-Praktikum.html').write_pdf(base + '03-Praktikum.pdf')
print('ok')
