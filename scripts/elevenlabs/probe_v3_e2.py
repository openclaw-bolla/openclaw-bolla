import json,sys,re,urllib.request,os
# E2: E1 + langsamer (0.87), Satz-/Absatzpausen via "…", Zusatz-Tags dosiert
S=sys.argv[1]
t=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'prolog_text_v3_tags.txt')).read()
t=t.replace('zwei Uhr siebenundvierzig\n','zwei Uhr siebenundvierzig …\n')
t=t.replace('die Nachtschicht zu übernehmen.','die Nachtschicht zu übernehmen. …')
t=t.replace('Sie nippte an ihrem vierten Kaffee des Abends und starrte auf die Monitore.','Sie nippte an ihrem vierten Kaffee des Abends und starrte auf die Monitore. …')
t=t.replace('Draußen regnete es. Durch','Draußen regnete es. … [quietly] Durch')
t=t.replace('ihr Problem.','ihr Problem. …').replace('grundlegendstes Problem.','grundlegendstes Problem. …')
t=t.replace('Nachbar.','Nachbar. …')
key=open(os.path.expanduser('~/.elevenlabs_key')).read().strip()
body=json.dumps({'text':t,'model_id':'eleven_v3','language_code':'de','voice_settings':{'stability':0.5,'similarity_boost':0.8,'style':0.0,'use_speaker_boost':False,'speed':0.87}}).encode()
r=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/aQ8PgTCtUwYuAWhEWTch?output_format=mp3_44100_128',body,{'xi-api-key':key,'Content-Type':'application/json'})
a=urllib.request.urlopen(r,timeout=240).read()
open(S+'/probe/Probe_Prolog_E2_v3_tempo_pausen.mp3','wb').write(a);print(len(a),len(t))
