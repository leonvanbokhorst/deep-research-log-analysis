import sys, os, json, re, collections
sys.path.insert(0,'/Users/leonvanbokhorst/repos/deep-research-log-analysis/analysis/tools')
from corpus import *

DS='/Users/leonvanbokhorst/repos/deep-research/'

# the eight amplification strands (depth-1 sessions created 1790327928258..61)
AMP = {
 '6f182957-7587-4604-97e9-5b8275f63b51':'S1 concept genealogy',
 '56542a81-0524-4af5-acd1-92a7cbbf9c8b':'S2 risk psychology',
 'b61859d5-9abc-4cc9-8ea7-06c15e81ef05':'S3 computational propaganda',
 'f54b15a3-b0aa-4d8a-961f-1cd6fa0548d6':'S4 agentic capability',
 'f5d926fb-1c4e-4c16-af8f-c7dce00748fd':'S5 drone sightings',
 '46b82e74-e114-4473-b55d-e2c13cfef604':'S6 health/military scares',
 'b0f0ef6b-188b-48bb-a9b0-a808aa6a8393':'S7 counterexamples',
 'dc0b75f5-7e62-49c9-a810-8793a1c7648f':'S8 defensive practice',
}
# the eight parent-study (autonomy) strands
PARENT = {
 '9ab7a0c1-d19a-45d5-b511-696d1d884a19':'P1 Ukraine',
 '99dae34e-50a3-42d8-b818-f7eda5a3f4f6':'P2 Middle East',
 '230a12e6-6703-4fa1-97a8-d3265be4edb1':'P3 swarm audit',
 '2da418c8-78b5-4a1e-bf1c-bde3fd2d89c0':'P4 GNSS/edge AI',
 '214d85c6-dbe8-43ae-bb06-96929af0216d':'P5 criminal misuse',
 'c2e2b954-63bb-4c00-8d45-37e953901183':'P6 NATO/EU assessments',
 'e49930ac-674f-41f7-8ead-2c84161d693d':'P7 defender economics',
 '109e924b-6fb2-4a09-822c-b44e4256f317':'P8 AI planning',
}

def build(sess):
    anc={}
    for sid,s in sess.items():
        cur=sid; seen=set()
        while cur in sess and sess[cur].parent and cur not in seen:
            seen.add(cur); cur=sess[cur].parent
        anc[sid]=cur
    return anc

URL_RE=re.compile(r'https?://[^\s"\'`\)\]>]+')
NET_VERBS=re.compile(r'\b(curl|wget)\b|get\.sh|news\.sh|news-nl\.sh|ddg\.sh|web\.sh|bn\.sh|s\.sh|j\.sh|gn\.sh|wsearch\.sh|pget\.py|search\.sh|fetch\.py|/f\.py')
EVID_RE=re.compile(r'(amplification/(findings|notes|research|sources)|(?:^|[\s/"\'])(findings|notes|sources|research)/[A-Za-z0-9_\-./]+\.(?:md|txt|json|csv))')

def norm_url(u):
    u=u.rstrip('.,;)\'"]')
    return u
