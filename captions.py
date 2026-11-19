"""Independent word-timed ASR, editable transcript and styled ASS/SRT."""
from pathlib import Path
import json,os,threading,subprocess
MODELS={}

def _load(WhisperModel,spec,data):
    """GPU first (int8_float16, ~10x faster than CPU), CPU int8 as fallback. Never crashes on a missing CUDA runtime."""
    import sys
    site=Path(sys.prefix)/'Lib'/'site-packages'/'nvidia'
    for sub in ('cublas','cudnn'):
        b=site/sub/'bin'
        if b.exists():
            try:os.add_dll_directory(str(b))
            except (OSError,AttributeError):pass
            os.environ['PATH']=str(b)+os.pathsep+os.environ['PATH']
    if os.environ.get('NEONCLIPPING_CPU')!='1':
        try:
            m=WhisperModel(spec,device='cuda',compute_type='int8_float16',download_root=str(data/'models'))
            list(m.transcribe(__import__('numpy').zeros(16000,dtype='float32'))[0])   # prove cuDNN/cuBLAS really load
            return m
        except Exception:pass
    return WhisperModel(spec,device='cpu',compute_type='int8',cpu_threads=max(1,(os.cpu_count() or 4)-2),download_root=str(data/'models'))
LOCK=threading.Lock()

def transcribe(source,start,end,data,report=lambda message:None,language=None,model=None):
    report('Loading local speech model (first use may download it)')
    from faster_whisper import WhisperModel
    spec=model or os.environ.get('FACECAM_ASR_MODEL','')
    if not spec:
        snapshots=Path.home()/'.cache/huggingface/hub/models--mobiuslabsgmbh--faster-whisper-large-v3-turbo/snapshots'
        available=[p for p in snapshots.glob('*') if (p/'model.bin').exists()]
        spec=str(available[0]) if available else 'base'
    model_tag=Path(spec).name[:14]
    key=f'{source.stem}-{start:.2f}-{end:.2f}-{language or "auto"}-{model_tag}-v2'
    cached=data/(key+'.words.json')
    if cached.exists():return json.loads(cached.read_text(encoding='utf-8'))
    with LOCK:
        MODEL=MODELS.get(spec)
        if MODEL is None:
            MODEL=MODELS[spec]=_load(WhisperModel,spec,data)
        audio=data/(key+'.wav')
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(start),'-t',str(end-start),'-i',str(source),'-vn','-ac','1','-ar','16000',str(audio)],capture_output=True,check=True,timeout=300)
        try:
            report('Transcribing selected clip locally')
            prompt='यह हिंदी और अंग्रेज़ी में गेमिंग वीडियो है। GTA, गेमप्ले, क्लिपिंग, वीडियो, टूल।' if language=='hi' else None
            segments,info=MODEL.transcribe(str(audio),beam_size=3,language=language or None,initial_prompt=prompt,word_timestamps=True,vad_filter=True,condition_on_previous_text=False)
            words=[]
            for segment in segments:
                for w in segment.words or []:
                    text=w.word.strip()
                    if text and w.end>w.start:words.append({'start':round(max(0,w.start),3),'end':round(min(end-start,w.end),3),'text':text})
            result={'words':words,'language':info.language,'duration':end-start,'model':model_tag}
            cached.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8');return result
        finally:audio.unlink(missing_ok=True)

def stamp(t,ass=False):
    units=int(round(max(0,float(t))*(100 if ass else 1000)));h,units=divmod(units,(360000 if ass else 3600000));m,units=divmod(units,(6000 if ass else 60000));s,u=divmod(units,(100 if ass else 1000))
    return f'{h}:{m:02}:{s:02}.{u:02}' if ass else f'{h:02}:{m:02}:{s:02},{u:03}'

def safe(text):return str(text).replace('\\','/').replace('{','(').replace('}',')').replace('\n',' ')

def write(words,style,folder,name,hook='',position=1450):
    # Font fallback resolves Hindi through installed Windows Nirmala UI.
    ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','WrapStyle: 2',
         '[V4+ Styles]','Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding',
         'Style: Main,Arial,72,&H00FFFFFF,&H0000FFFF,&H00100B18,&H99000000,-1,0,0,0,100,100,0,0,1,5,2,5,50,50,0,1',
         '[Events]','Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
    srt=[];groups=[words[i:i+3] for i in range(0,len(words),3)]
    for i,group in enumerate(groups):
        if not group:continue
        begin=group[0]['start'];end=group[-1]['end']
        line=' '.join(safe(w['text']) for w in group)
        srt.append(f'{i+1}\n{stamp(begin)} --> {stamp(end)}\n{line}\n')
        if style=='clean':
            ass.append(f'Dialogue: 1,{stamp(begin,True)},{stamp(end,True)},Main,,0,0,0,,{{\\pos(540,{position})\\fs58\\bord3}}{line}')
        else:
            for n,word in enumerate(group):
                a=max(begin,word['start']);b=group[n+1]['start'] if n+1<len(group) else end
                if b<=a:continue
                chunks=[]
                for k,w in enumerate(group):
                    color='&H003DF3CB&' if style=='bold' else ('&H00EFFF43&' if k!=n else '&H00A845FF&')
                    if style=='bold' and k!=n:color='&H00FFFFFF&'
                    chunks.append('{\\c'+color+'}'+safe(w['text']).upper())
                extra='\\bord6\\shad4' if style=='bold' else '\\bord4\\3c&H00560C31&\\shad5\\4c&H00FFCC00&\\blur0.7'
                text='{\\pos(540,'+str(position)+')'+extra+'}'+' '.join(chunks)
                ass.append(f'Dialogue: 1,{stamp(a,True)},{stamp(b,True)},Main,,0,0,0,,{text}')
    if hook.strip():
        ass.append(f'Dialogue: 2,0:00:00.00,0:00:03.00,Main,,0,0,0,,{{\\pos(540,250)\\fs82\\c&H00A845FF&\\bord7}}{safe(hook)[:65]}')
    (folder/(name+'.ass')).write_text('\n'.join(ass),encoding='utf-8')
    (folder/(name+'.srt')).write_text('\n'.join(srt),encoding='utf-8')
    return name+'.ass',name+'.srt'
