"""Independently surface candidate correction/challenge events in the corpus.

This is a cross-check on the delegated correction analysis: it locates every
message that contains explicit correction language, so that the narrative
reconstruction can be validated against a mechanical search.

Outputs:
  analysis/data/correction_candidates.csv
  analysis/tables/challenge_edges.csv  (who challenged whom)
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

OUT = os.path.join(C.WORKSPACE, "analysis", "data")
TAB = os.path.join(C.WORKSPACE, "analysis", "tables")

PATTERNS = [
    (r"\bwithdraw(n|s|ing)?\b", "withdraw"),
    (r"\bwithdrew\b", "withdraw"),
    (r"\bretract(ed|ion|s|ing)?\b", "retract"),
    (r"\bcorrect(ed|ion|s)?\b", "correct"),
    (r"\bI was wrong\b", "self_error"),
    (r"\bmy earlier\b", "self_error"),
    (r"\bI previously\b", "self_error"),
    (r"\bactually (?:not|no|false|wrong)\b", "contradict"),
    (r"\bdoes not (?:hold|support|survive)\b", "contradict"),
    (r"\bcollaps(?:es|ed|ing)\b", "collapse"),
    (r"\bdebunk(?:ed|s|ing)?\b", "debunk"),
    (r"\bno evidence\b", "negative_evidence"),
    (r"\bnot supported\b", "negative_evidence"),
    (r"\bfalsif(?:y|ied|ies|ication)\b", "falsify"),
    (r"\boverstat(?:e|ed|es|ing|ement)\b", "overstate"),
    (r"\bmisleading\b", "misleading"),
    (r"\bcontradict(?:s|ed|ion|ory)?\b", "contradict"),
    (r"\bsupersed(?:e|ed|es)\b", "supersede"),
    (r"\breplac(?:e|ed|es|ing) (?:the|this|that|an? earlier)\b", "supersede"),
    (r"\bincorrect\b", "correct"),
    (r"\bunverifiable\b", "unverifiable"),
    (r"\bsingle[- ]source\b", "weak_sourcing"),
    (r"\bcannot be verified\b", "unverifiable"),
    (r"\bno longer\b", "revision"),
    (r"\brevis(?:e|ed|es|ion)\b", "revision"),
]
COMPILED = [(re.compile(p, re.I), k) for p, k in PATTERNS]

# explicit meta-language markers that are stronger signals of a real correction
STRONG = re.compile(
    r"(?i)(must (?:be )?withdraw|is withdrawn|was withdrawn|earlier draft|"
    r"initially (?:described|used|repeated|claimed)|I was wrong|"
    r"this report initially|correction is important|report initially|"
    r"corrected (?:on|meta)|replaced here|that earlier|earlier figure|"
    r"earlier claim|no longer use|do not use|withdrawn)")

CORRECTION_FILES = ("retractions", "corrections", "retract", "correction")


def main():
    sessions = C.load_all()
    rows = []
    challenge_edges = Counter()
    deep_challenges = []

    for sid, s in sessions.items():
        for o in s.events:
            t = o.get("type")
            txt = ""
            who = ""
            if t == "assistant/message":
                d = o.get("data") or {}
                txt = C.text_of((d.get("message") or {}).get("content"))
                who = "assistant"
            elif t == "agent/inbox/spliced":
                for ins in (o.get("data") or {}).get("inserted", []):
                    txt += C.text_of(ins.get("content")) + "\n"
                    src = ins.get("source") or {}
                    if src.get("senderSessionId"):
                        who = "agent:" + str(src["senderSessionId"])
                    elif src.get("kind"):
                        who = src["kind"]
            elif t == "user/message":
                txt = C.text_of((o.get("data") or {}).get("message", {}).get("content"))
                who = "user"
            if not txt:
                continue
            hits = [k for rx, k in COMPILED if rx.search(txt)]
            if not hits:
                continue
            strong = bool(STRONG.search(txt))
            if not strong and len(set(hits)) < 2:
                continue
            rows.append({
                "session": sid, "depth": s.depth, "label": s.label,
                "time": o.get("time"), "seq": o.get("seq"), "kind": t, "who": who,
                "strength": "strong" if strong else "weak",
                "markers": "|".join(sorted(set(hits))),
                "excerpt": re.sub(r"\s+", " ", txt)[:600],
            })

    rows.sort(key=lambda r: (r["time"] or 0))
    with open(os.path.join(OUT, "correction_candidates.csv"), "w",
              newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        cw.writeheader()
        cw.writerows(rows)
    print(f"  correction_candidates.csv: {len(rows)} rows "
          f"({sum(1 for r in rows if r['strength']=='strong')} strong)")

    # corrections appearing in agent-to-agent traffic, by depth
    by_depth = Counter((r["depth"], r["strength"]) for r in rows if r["kind"] != "assistant/message")
    print("  agent-traffic correction signals by (depth,strength):", dict(by_depth))

    # find files whose names signal retraction
    import subprocess
    ws = "/Users/leonvanbokhorst/repos/deep-research"
    found = []
    for root, dirs, files in os.walk(ws):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            if any(k in fn.lower() for k in CORRECTION_FILES):
                p = os.path.join(root, fn)
                found.append({"path": os.path.relpath(p, ws),
                              "bytes": os.path.getsize(p)})
    with open(os.path.join(TAB, "correction_artifacts.csv"), "w",
              newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=["path", "bytes"])
        cw.writeheader()
        cw.writerows(found)
    print(f"  correction_artifacts.csv: {len(found)} files")

    # console: the strongest signals
    print("\n  strongest correction signals (first 25):")
    for r in [x for x in rows if x["strength"] == "strong"][:25]:
        print(f"    d{r['depth']} {str(r['label'])[:34]:<34} {r['kind'][:16]:<16} "
              f"{r['markers'][:28]:<28} {r['excerpt'][:110]}")


if __name__ == "__main__":
    main()
