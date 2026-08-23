html = open('/home/bolla/workspace/scratch/aldi_aktuell.html', encoding='utf-8').read()
idx = html.find('LEAFLET_IPAPER_STRUCTURE_GET')
print(html[idx-50:idx+3000])
