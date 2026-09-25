import sys, json, os, re, collections
sys.path.insert(0,'/Users/leonvanbokhorst/repos/deep-research-log-analysis/analysis/tools')
from corpus import *

_S=None
def S():
    global _S
    if _S is None: _S=load_all()
    return _S

def atext(d):
    """Flatten assistant message data dict."""
    m = d.get('message') or {}
    c = m.get('content')
    if c is None: c = d.get('content')
    return text_of(c)

def evtext(o):
    """Get all human-visible text from any event, tagged by part."""
    t=o.get('type'); d=o.get('data') or {}
    out=[]
    if t=='assistant/message':
        m=d.get('message') or {}
        for c in (m.get('content') or []):
            if not isinstance(c,dict): continue
            ct=c.get('type')
            if ct=='text': out.append(('asst-text',c.get('text') or ''))
            elif ct=='reasoning': out.append(('asst-reasoning',c.get('text') or ''))
            elif ct=='tool-call': out.append(('asst-toolcall',c.get('arguments') or ''))
    elif t=='tool/call':
        out.append(('tool/call:'+str(d.get('name')), d.get('arguments') if isinstance(d.get('arguments'),str) else json.dumps(d.get('arguments'))))
    elif t=='tool/result':
        out.append(('tool/result', text_of((d.get('message') or {}).get('content'))))
    elif t=='user/message':
        out.append(('user/message', text_of(d.get('content'))))
    elif t=='agent/inbox/spliced':
        for ins in (d.get('inserted') or []):
            out.append(('inbox/spliced', text_of(ins.get('content'))))
    elif t=='subagent/catalog':
        out.append(('catalog', json.dumps(d)))
    elif t=='subagent/descriptor':
        out.append(('descriptor', json.dumps(d)))
    return out

def search(pat, flags=re.I, types=None, limit=200):
    rx=re.compile(pat, flags)
    hits=[]
    for sid,s in S().items():
        for o in s.events:
            for tag,txt in evtext(o):
                if types and not any(tag.startswith(t) for t in types): continue
                if not txt: continue
                for m in rx.finditer(txt):
                    a=max(0,m.start()-160); b=min(len(txt),m.end()+200)
                    hits.append(dict(sid=sid,depth=s.depth,label=s.label,time=o.get('time'),seq=o.get('seq'),
                                     tag=tag,snip=txt[a:b].replace('\n',' ')))
                    if len(hits)>=limit: return hits
    return hits
