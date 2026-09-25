"""Probe search: first appearance time of each important finding's evidence.

Streams analysis/work/tl_assistant.jsonl (all sessions' assistant text, which
includes tool-call arguments, i.e. written file contents) and records the first
and last time each regex probe fires, with a context snippet.

Usage:  python3 probes.py [probe_file.json]
Default probes are the ~25 findings extracted from the final report's
sections 1, 5, 7.5, 8 and 12.1-12.3.
"""

from __future__ import annotations

import json
import os
import re
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

WORK = os.path.join(C.WORKSPACE, "analysis", "work")

DEFAULT = {
    # id: (description, regex, flags)
    "nj_5000": ("New Jersey 5,000+ sightings / nothing anomalous",
                r"5,?0\d\d\s+(?:reported\s+)?(?:sighting|tip|report)|New Jersey", 0),
    "gatwick": ("Gatwick 2018", r"Gatwick", 0),
    "copenhagen": ("Copenhagen 2025 airport closure", r"Copenhagen", 0),
    "boston_2013": ("Boston 2013 emergent amplification", r"Boston", 0),
    "institution_amplifier": ("the amplifier is the institution",
                              r"amplifier is (?:not|the)|institutional stage", re.I),
    "central_negative": ("no documented AI-enabled drone-wave amplification",
                         r"central negative finding|no credible,? documented case", re.I),
    "eeas_540": ("EEAS 540 FIMI incidents, 27% AI", r"\b540\b", 0),
    "eeas_147": ("EEAS 41->147 AI-related cases", r"\b147\b", 0),
    "galati": ("Galati Romania 116,014 posts", r"Gala[tț]i|116,?014", 0),
    "com2026_81": ("COM(2026) 81 zero disinfo terms", r"COM\(?2026\)?\s*81", 0),
    "iran_china_agents": ("Iran/China agentic influence ops", r"hundreds of AI agents|80,?000 followers", re.I),
    "usc_sim": ("USC arXiv 2510.25003 simulation-only", r"2510\.25003", 0),
    "openai_150k": ("OpenAI 150,000 views vs 57 / factor 2,600", r"150,?000 views|2,?600", 0),
    "openai_quote": ("OpenAI 'do not appear to have meaningfully increased'",
                     r"meaningfully increased their audience", re.I),
    "liars_dividend": ("liar's dividend 45-54%", r"liar'?s dividend", re.I),
    "reach_billion": ("40 accounts -> 1bn views", r"billion views", re.I),
    "botometer": ("Botometer AUC 0.85 / 76% human", r"Botometer|0\.85\b", 0),
    "gallwitz": ("Gallwitz & Kreil 'not a single social bot'", r"Gallwitz", 0),
    "detect_555": ("55.5% pooled synthetic detection, 56 papers", r"55\.5\s?%|86,?155", 0),
    "dawel": ("Dawel PNAS 40%->80%", r"Dawel", 0),
    "cost_524": ("524:1 cost asymmetry", r"\b524\b", 0),
    "persuasion_005": ("0.05-0.06 SD measured persuasion", r"0\.0[56]\s*SD|49 experiments", 0),
    "synthetic_3749": ("3,749 AI-generated news sites", r"3,?749", 0),
    "indian_chronicles": ("Indian Chronicles 750+ fake outlets", r"Indian Chronicles", 0),
    "repetition_not_number": ("repetition, not number of sources (2012)",
                              r"repetition,? not (?:the )?number", re.I),
    "correction_lag": ("62.9-hour lag vs 6.25-hour half-life", r"62\.9|6\.25", 0),
    "rounds_43": ("43 rounds fired at Borris", r"43 rounds", re.I),
    "six_conditions": ("six conditions for second-order risk", r"six conditions", re.I),
    "cib_starbird": ("CIB critique Starbird / Meta 21 Oct 2019",
                     r"Starbird|21 October 2019", 0),
    "schiff_apsr": ("Schiff et al APSR 2024 >15,000 adults", r"Schiff", 0),
    "indistinguishable_withdrawn": ("withdrawn 'indistinguishable in more than half' claim",
                                    r"indistinguishable in (?:more than )?half", re.I),
    "twitter25_bots": ("withdrawn '25% of Twitter activity is bots'", r"25%\s+of\s+Twitter", re.I),
    "temporal_decoupling": ("temporal-decoupling test", r"temporal[- ]decoupl", re.I),
    "denmark_not_named": ("EEAS does not name Denmark or Norway",
                          r"(?:explicitly )?does not name (?:Denmark|Norway)|not name Denmark", re.I),
    "havana": ("Havana syndrome ambiguity", r"Havana", 0),
    "vilnius_birds": ("Vilnius 2026 birds / 38 minutes", r"Vilnius", 0),
}


def ts(ms):
    return datetime.datetime.utcfromtimestamp(ms / 1000).strftime("%H:%M:%S")


def main():
    probes = DEFAULT
    if len(sys.argv) > 1:
        probes = json.load(open(sys.argv[1]))
    compiled = {k: (v[0], re.compile(v[1], v[2] if len(v) > 2 else 0))
                for k, v in probes.items()}
    first = {}
    counts = {k: 0 for k in compiled}
    with open(os.path.join(WORK, "tl_assistant.jsonl"), encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            txt = r.get("text") or ""
            if not txt:
                continue
            tm = r["time"]
            for k, (desc, rx) in compiled.items():
                m = rx.search(txt)
                if m:
                    counts[k] += 1
                    if k not in first or tm < first[k]["time"]:
                        s = max(0, m.start() - 120)
                        e = min(len(txt), m.end() + 160)
                        first[k] = {
                            "id": k, "desc": desc, "time": tm, "clock": ts(tm),
                            "session": r["session"], "depth": r["depth"],
                            "label": r.get("label"), "turn": r.get("turn"),
                            "step": r.get("step"),
                            "snippet": txt[s:e].replace("\n", " ")[:280],
                        }
    out = os.path.join(WORK, "probe_first_hits.json")
    json.dump({"first": first, "counts": counts}, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"{'id':<28}{'first':<10}{'n':>6}  desc")
    for k in sorted(first, key=lambda x: first[x]["time"]):
        r = first[k]
        print(f"{k:<28}{r['clock']:<10}{counts[k]:>6}  {r['desc']}")
    missing = [k for k in compiled if k not in first]
    if missing:
        print("\nNEVER FOUND:", missing)


if __name__ == "__main__":
    main()
