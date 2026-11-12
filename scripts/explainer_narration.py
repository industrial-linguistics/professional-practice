#!/usr/bin/env python3
"""Voice an explainer from lesson narratives, keeping word timings for animation.

Reads explainers/<name>/script.json, sends each line to ElevenLabs with timestamps, and writes
narration.mp3, narration.json (lines with word times), narration.js (what the page loads) and
captions.vtt.

    python3 scripts/explainer_narration.py error-budget

script.json may set, besides "model" and "narratives":
  "models":         {"Greg": "eleven_multilingual_v2"}     a model for one speaker
  "voice_settings": {"Greg": {"clone_strength": 1.0}}       extra settings for one speaker
  "tts_overrides":  {"8": "text with a pronunciation hint"}  what to send for one line

Re-voicing does not mean re-timing. The scene's beat times belong to the first take, whose word
times are kept in authored.json. Each later take gets a "warp" table that maps its word times
back to the authored ones, and the scene looks up authored time before drawing. So a new model
or new settings need only this script and a re-render, provided the words are unchanged.

The two voices come back at different levels (Greg on v2 is about four LU quieter than Anna on
v4), so each speaker gets one constant gain that brings their lines to -16 LUFS before the mix.
A music bed made by scripts/explainer_music.py stays named in narration.js; rebuild it with
`explainer_music.py <name> --bed` after a re-voice, because line times may have moved.

Line takes are cached in output/explainers/<name>-takes/ and reused while the text, model and
settings match. Recording costs credits. The key comes from ELEVENLABS_API_KEY or
~/.elevenlabs.io. Requires ffmpeg and ffprobe.
"""
from pathlib import Path
import base64,hashlib,json,os,re,subprocess,sys,urllib.error,urllib.request
ROOT=Path(__file__).resolve().parents[1]
VOICES={'Speaker 1':('Anna','sx8pHRzXdQfuUYPGFK7X'),'Speaker 2':('Greg','vTdXuGkq3ozMNBhP2Hz7')}  # as cmd/voicer
BASE_SETTINGS={'stability':0.5,'similarity_boost':0.75}
LINE_GAP,SECTION_GAP,LEAD_IN,TAIL=0.38,0.85,0.6,1.0
def api_key():
    key=os.environ.get('ELEVENLABS_API_KEY')
    path=Path.home()/'.elevenlabs.io'
    if not key and path.exists():key=path.read_text().strip()
    return key or 'proxy-injected'  # a network proxy may supply the header instead
def speak(text,voice_id,model,settings):
    body={'text':text,'model_id':model,'voice_settings':settings}
    req=urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128',
        data=json.dumps(body).encode(),headers={'Content-Type':'application/json','xi-api-key':api_key()},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=180) as response:return json.loads(response.read())
    except urllib.error.HTTPError as error:
        raise SystemExit(f'ElevenLabs returned {error.code}: {error.read().decode()[:300]}')
def duration(path):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(path)],capture_output=True,text=True,check=True).stdout)
def loudness(paths):
    """Integrated loudness in LUFS of some audio files played end to end."""
    inputs=[x for path in paths for x in ('-i',str(path))];graph=''.join(f'[{k}:a]' for k in range(len(paths)))+f'concat=n={len(paths)}:v=0:a=1,ebur128[out]'
    text=subprocess.run(['ffmpeg','-nostdin','-hide_banner',*inputs,'-filter_complex',graph,'-map','[out]','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',text)[-1])
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
def stamp(t):
    return f'{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}'
def captions(script):
    """WebVTT from the word times: a new cue at sentence ends, or after about ten words."""
    cues=[]
    for line in script:
        chunk=[]
        for i,word in enumerate(line['words']):
            chunk.append(word);last=i==len(line['words'])-1
            if last or (len(chunk)>=5 and word[0][-1] in '.?!') or len(chunk)>=10:
                cues.append(f"{stamp(chunk[0][1])} --> {stamp(chunk[-1][2])}\n<v {line['speaker']}>{' '.join(w[0] for w in chunk)}");chunk=[]
    return 'WEBVTT\n\n'+'\n\n'.join(cues)+'\n'
def warp(script,total,authored):
    """Anchor pairs [time in this take, time in the authored take], one per word where the lines still match."""
    pairs=[[0.0,0.0]]
    for line,old in zip(script,authored['lines']):
        if len(line['words'])==len(old['words']):pairs+=[[w[1],o[1]] for w,o in zip(line['words'],old['words'])]
        else:pairs.append([line['start'],old['start']])
        pairs.append([line['end'],old['end']])
    pairs.append([total,authored['duration']])
    kept=[]
    for real,auth in pairs:  # both sides must keep moving forward
        if not kept or (real>kept[-1][0]+1e-6 and auth>=kept[-1][1]):kept.append([round(real,3),round(auth,3)])
    return kept
def main(name):
    home=ROOT/'explainers'/name;config=json.loads((home/'script.json').read_text())
    takes=ROOT/'output/explainers'/f'{name}-takes';takes.mkdir(parents=True,exist_ok=True)
    lines=[]
    for source in config['narratives']:
        for n,raw in enumerate((ROOT/source).read_text().strip().split('\n')):
            match=re.match(r'(Speaker \d): (.*)',raw.strip())
            if match:lines.append({'source':source,'first':n==0,'speaker':VOICES[match[1]][0],'voice_id':VOICES[match[1]][1],'text':match[2]})
    t=LEAD_IN;script=[];placed=[];models={}
    for i,line in enumerate(lines):
        spoken=config.get('tts_overrides',{}).get(str(i),line['text']);model=config.get('models',{}).get(line['speaker'],config['model'])
        settings=dict(BASE_SETTINGS,**config.get('voice_settings',{}).get(line['speaker'],{}));models[line['speaker']]=model
        mp3=takes/f'line-{i:02d}.mp3';meta=takes/f'line-{i:02d}.json';want={'spoken':spoken,'model':model,'settings':settings}
        cached=json.loads(meta.read_text()) if mp3.exists() and meta.exists() else None
        if not cached or {'spoken':cached['spoken'],'model':cached.get('model',config['model']),'settings':cached.get('settings',BASE_SETTINGS)}!=want:
            data=speak(spoken,line['voice_id'],model,settings);mp3.write_bytes(base64.b64decode(data['audio_base64']))
            meta.write_text(json.dumps(dict(want,alignment=data['alignment'])));print(f'recorded line {i} ({line["speaker"]}, {model})')
        if i:t+=SECTION_GAP if line['first'] else LINE_GAP
        length=duration(mp3)
        script.append({'speaker':line['speaker'],'model':model,'source':line['source'],'text':line['text'],'start':round(t,3),'end':round(t+length,3),'words':words(json.loads(meta.read_text())['alignment'],t)})
        placed.append((t,mp3,line['speaker']));t+=length
    total=round(t+TAIL,3);inputs=[];filters=[]
    gains={who:-16.0-loudness([mp3 for _,mp3,speaker in placed if speaker==who]) for who in {speaker for _,_,speaker in placed}}  # one gain a speaker
    for k,(start,mp3,speaker) in enumerate(placed):
        inputs+=['-i',str(mp3)];filters.append(f'[{k}:a]volume={gains[speaker]:.2f}dB,adelay={int(start*1000)}:all=1[a{k}]')
    graph=';'.join(filters)+';'+''.join(f'[a{k}]' for k in range(len(placed)))+f'amix=inputs={len(placed)}:normalize=0:dropout_transition=0,alimiter=limit=0.84:level=false,apad,atrim=0:{total:.3f}[out]'
    subprocess.run(['ffmpeg','-nostdin','-y','-v','error',*inputs,'-filter_complex',graph,'-map','[out]','-ar','44100','-ac','1','-b:a','128k',str(home/'narration.mp3')],check=True)
    authored_path=home/'authored.json'
    if not authored_path.exists():  # the first take is the one the scene was timed against
        authored_path.write_text(json.dumps({'duration':total,'lines':[{'start':l['start'],'end':l['end'],'words':l['words']} for l in script]})+'\n')
    authored=json.loads(authored_path.read_text());table=warp(script,total,authored)
    full={'provider':'ElevenLabs','models':models,'voices':{v[0]:v[1] for v in VOICES.values()},'source':config['narratives'],'audio':'narration.mp3',
        'audio_sha256':hashlib.sha256((home/'narration.mp3').read_bytes()).hexdigest(),'duration':total,'authored_duration':authored['duration'],
        'speaker_gain_db':{who:round(g,2) for who,g in gains.items()},'tts_overrides':config.get('tts_overrides',{}),'lines':script}
    (home/'narration.json').write_text(json.dumps(full,indent=1)+'\n')
    compact={'audio':'narration.mp3','duration':total,'authored_duration':authored['duration'],'warp':table,'lines':[{k:l[k] for k in ('speaker','text','start','end')} for l in script]}
    if config.get('music') and (home/'music.mp3').exists():compact['music']='music.mp3'
    (home/'narration.js').write_text('// Generated by scripts/explainer_narration.py. Do not edit.\nwindow.EXPLAINER_NARRATION='+json.dumps(compact,ensure_ascii=False,separators=(',',':'))+';\n')
    (home/'captions.vtt').write_text(captions(script))
    drift=max(abs(a-b) for a,b in table)
    print(f'{name}: {len(script)} lines, {total:.1f} s (authored {authored["duration"]:.1f} s, largest shift {drift:.2f} s), {sum(len(l["text"]) for l in script)} characters')
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit(__doc__)
    main(sys.argv[1])
