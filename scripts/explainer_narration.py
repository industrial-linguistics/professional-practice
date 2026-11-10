#!/usr/bin/env python3
"""Voice an explainer from lesson narratives, keeping word timings for animation.

Reads explainers/<name>/script.json, sends each line to ElevenLabs with timestamps, and writes
narration.mp3, narration.json (lines with word times) and narration.js (what the page loads).

    python3 scripts/explainer_narration.py error-budget

Every run costs credits and produces a new take with different timings. The beat times in the
explainer's scene.js belong to the committed take, so re-voicing means re-timing the scene.
Line takes are cached in output/explainers/<name>-takes/; delete a take to re-record that line.

The key comes from ELEVENLABS_API_KEY or ~/.elevenlabs.io. Requires ffmpeg and ffprobe.
"""
from pathlib import Path
import base64,hashlib,json,os,re,subprocess,sys,urllib.error,urllib.request
ROOT=Path(__file__).resolve().parents[1]
VOICES={'Speaker 1':('Anna','sx8pHRzXdQfuUYPGFK7X'),'Speaker 2':('Greg','vTdXuGkq3ozMNBhP2Hz7')}  # as cmd/voicer
LINE_GAP,SECTION_GAP,LEAD_IN,TAIL=0.38,0.85,0.6,1.0
def api_key():
    key=os.environ.get('ELEVENLABS_API_KEY')
    path=Path.home()/'.elevenlabs.io'
    if not key and path.exists():key=path.read_text().strip()
    return key or 'proxy-injected'  # a network proxy may supply the header instead
def speak(text,voice_id,model):
    body={'text':text,'model_id':model,'voice_settings':{'stability':0.5,'similarity_boost':0.75}}
    req=urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128',
        data=json.dumps(body).encode(),headers={'Content-Type':'application/json','xi-api-key':api_key()},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=180) as response:return json.loads(response.read())
    except urllib.error.HTTPError as error:
        raise SystemExit(f'ElevenLabs returned {error.code}: {error.read().decode()[:300]}')
def duration(path):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(path)],capture_output=True,text=True,check=True).stdout)
def words(alignment,offset):
    out=[];current='';start=end=None
    for ch,a,b in zip(alignment['characters'],alignment['character_start_times_seconds'],alignment['character_end_times_seconds']):
        if ch.isspace():
            if current:out.append([current,round(start+offset,3),round(end+offset,3)]);current='';start=None
        else:
            if start is None:start=a
            current+=ch;end=b
    if current:out.append([current,round(start+offset,3),round(end+offset,3)])
    return out
def main(name):
    home=ROOT/'explainers'/name;config=json.loads((home/'script.json').read_text());model=config['model']
    takes=ROOT/'output/explainers'/f'{name}-takes';takes.mkdir(parents=True,exist_ok=True)
    lines=[]
    for source in config['narratives']:
        for n,raw in enumerate((ROOT/source).read_text().strip().split('\n')):
            match=re.match(r'(Speaker \d): (.*)',raw.strip())
            if match:lines.append({'source':source,'first':n==0,'speaker':VOICES[match[1]][0],'voice_id':VOICES[match[1]][1],'text':match[2]})
    t=LEAD_IN;script=[];placed=[]
    for i,line in enumerate(lines):
        spoken=config.get('tts_overrides',{}).get(str(i),line['text']);mp3=takes/f'line-{i:02d}.mp3';meta=takes/f'line-{i:02d}.json'
        if not (mp3.exists() and meta.exists() and json.loads(meta.read_text())['spoken']==spoken):
            data=speak(spoken,line['voice_id'],model);mp3.write_bytes(base64.b64decode(data['audio_base64']))
            meta.write_text(json.dumps({'spoken':spoken,'alignment':data['alignment']}))
        if i:t+=SECTION_GAP if line['first'] else LINE_GAP
        length=duration(mp3)
        script.append({'speaker':line['speaker'],'source':line['source'],'text':line['text'],'start':round(t,3),'end':round(t+length,3),'words':words(json.loads(meta.read_text())['alignment'],t)})
        placed.append((t,mp3));t+=length
    total=t+TAIL;inputs=[];filters=[]
    for k,(start,mp3) in enumerate(placed):
        inputs+=['-i',str(mp3)];filters.append(f'[{k}:a]adelay={int(start*1000)}:all=1[a{k}]')
    graph=';'.join(filters)+';'+''.join(f'[a{k}]' for k in range(len(placed)))+f'amix=inputs={len(placed)}:normalize=0:dropout_transition=0,apad,atrim=0:{total:.3f}[out]'
    subprocess.run(['ffmpeg','-nostdin','-y','-v','error',*inputs,'-filter_complex',graph,'-map','[out]','-ar','44100','-ac','1','-b:a','128k',str(home/'narration.mp3')],check=True)
    full={'provider':'ElevenLabs','model':model,'voices':{v[0]:v[1] for v in VOICES.values()},'source':config['narratives'],'audio':'narration.mp3',
        'audio_sha256':hashlib.sha256((home/'narration.mp3').read_bytes()).hexdigest(),'duration':round(total,3),'tts_overrides':config.get('tts_overrides',{}),'lines':script}
    (home/'narration.json').write_text(json.dumps(full,indent=1)+'\n')
    compact={'audio':'narration.mp3','duration':round(total,3),'lines':[{k:l[k] for k in ('speaker','text','start','end')} for l in script]}
    (home/'narration.js').write_text('// Generated from narration.json by scripts/explainer_narration.py. Do not edit.\nwindow.EXPLAINER_NARRATION='+json.dumps(compact,ensure_ascii=False,indent=1)+';\n')
    print(f'{name}: {len(script)} lines, {total:.1f} s, {sum(len(l["text"]) for l in script)} characters')
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit(__doc__)
    main(sys.argv[1])
