"""Show the first N occurrences (by time) of exact strings, with context.

Usage: python3 show_hits.py 'regex1' 'regex2' ...
Prints time, session label, depth, and +/-160 chars of context. Also reports
how many distinct sessions and the last occurrence time.
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


def clock(t):
    return datetime.datetime.utcfromtimestamp(t / 1000).strftime("%H:%M:%S")


def main():
    pats = sys.argv[1:]
    rxs = [(p, re.compile(p, re.I)) for p in pats]
    hits = {p: [] for p in pats}
    with open(os.path.join(WORK, "tl_assistant.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            txt = r.get("text") or ""
            if not txt:
                continue
            for p, rx in rxs:
                for m in rx.finditer(txt):
                    hits[p].append((r["time"], r["session"], r["depth"],
                                    r.get("label") or "", r.get("turn"),
                                    txt[max(0, m.start() - 160):m.end() + 200]
                                    .replace("\n", " ")))
    for p in pats:
        h = sorted(hits[p])
        print("=" * 100)
        print(f"PATTERN {p!r}  total_hits={len(h)}  distinct_sessions={len(set(x[1] for x in h))}")
        if h:
            print(f"  first={clock(h[0][0])}  last={clock(h[-1][0])}")
        for (t, s, d, lab, turn, ctx) in h[:4]:
            print(f"  [{clock(t)}] d{d} {s[:8]} t{turn} {lab[:34]}")
            print(f"      ...{ctx[:330]}...")
        if len(h) > 4:
            print("  ---- tail ----")
            for (t, s, d, lab, turn, ctx) in h[-2:]:
                print(f"  [{clock(t)}] d{d} {s[:8]} t{turn} {lab[:34]}")
                print(f"      ...{ctx[:330]}...")


if __name__ == "__main__":
    main()
