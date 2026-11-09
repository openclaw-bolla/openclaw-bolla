import json,sys,re,urllib.request,os
S=sys.argv[1]
t=open(S+'/probe/text.txt').read().replace('\n<break time="0.7s"/>\n','\n\n')
rep=[('Das hatte sie sich auch nach','[wryly] Das hatte sie sich auch nach'),
 ('Aber sie war vierunddreißig','[sighs] Aber sie war vierunddreißig'),
 ('wobei es Noah gab','[amused] wobei es Noah gab'),
 ('Ihr Kollege Pawel dagegen','[matter-of-fact] Ihr Kollege Pawel dagegen'),
 ('Es war immer einfacher, ja zu sagen','[dry, resigned] Es war immer einfacher, ja zu sagen'),
 ('Sie nippte an ihrem vierten Kaffee','[deadpan] Sie nippte an ihrem vierten Kaffee')]
for a,b in rep:
    if a not in t: print('FEHLT',a)
    t=t.replace(a,b)
txt=t.replace('\n\n','\n\n')
open(S+'/probe/text_d3.txt','w').write(txt)
key=open(os.path.expanduser('~/.elevenlabs_key')).read().strip()
def go(vs):
    body=json.dumps({'text':txt,'model_id':'eleven_v3','language_code':'de','voice_settings':vs}).encode()
    r=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/aQ8PgTCtUwYuAWhEWTch?output_format=mp3_44100_128',body,{'xi-api-key':key,'Content-Type':'application/json'})
    return urllib.request.urlopen(r,timeout=240).read()
try: a=go({'stability':0.5,'similarity_boost':0.8,'style':0.0,'use_speaker_boost':False,'speed':0.9}); print('mit speed')
except Exception as e:
    print('Fehler',e,e.read()[:300] if hasattr(e,'read') else '')
    a=go({'stability':0.5,'similarity_boost':0.8,'style':0.0,'use_speaker_boost':False}); print('ohne speed')
open(S+'/probe/Probe_Prolog_E1_v3_emotion.mp3','wb').write(a);print(len(a),len(txt))
