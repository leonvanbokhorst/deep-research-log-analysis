#!/usr/bin/env python3
"""Count distinct sessions (and event types) containing a regex; print first/last times."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import corpus  # noqa: E402
from grepcorpus import blob_of  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern")
    ap.add_argument("--case", action="store_true")
    ap.add_argument("--list", action="store_true", help="list per-session hits")
    args = ap.parse_args()
    rx = re.compile(args.pattern, re.I if args.case else 0)
    rows = []
    for sid, path in corpus.session_paths():
        hits = 0
        first = None
        last = None
        parent = depth = label = ""
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                tt = o.get("type")
                if tt == "session":
                    parent = o.get("parentSession") or ""
                    depth = o.get("delegationDepth")
                    continue
                if tt == "subagent/descriptor":
                    label = (o.get("data") or {}).get("label") or ""
                    continue
                if rx.search(blob_of(o)):
                    hits += 1
                    t = o.get("time")
                    first = t if first is None else min(first, t)
                    last = t if last is None else max(last, t)
        if hits:
            rows.append((sid, depth, parent, label, hits, first, last))
    rows.sort(key=lambda r: r[5] or 0)
    print(f"{'session':14} {'d':2} {'parent':14} {'hits':>5} {'first':>14} {'last':>14}  label")
    for sid, d, p, lab, h, fi, la in rows:
        print(f"{sid[:12]:14} {str(d):2} {p[:12]:14} {h:5} {fi:>14} {la:>14}  {lab[:44]}")
    print(f"TOTAL sessions matched: {len(rows)}   total events: {sum(r[4] for r in rows)}", file=sys.stderr)


if __name__ == "__main__":
    main()
