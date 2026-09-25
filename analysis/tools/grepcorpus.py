#!/usr/bin/env python3
"""Stream the DSH corpus and grep for a regex, printing provenance.

Usage:
  python3 grepcorpus.py '<regex>' [--max N] [--ctx CHARS] [--sid SUBSTR]
                        [--types t1,t2] [--case] [--width W]

Prints one record per matching event:
  time  sid12  L<label>  type  seq  ::snippet::
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import corpus  # noqa: E402


def blob_of(o: dict) -> str:
    t = o.get("type")
    d = o.get("data") or {}
    if t == "assistant/message":
        return corpus.text_of((d.get("message") or {}).get("content"))
    if t == "tool/call":
        return f"{d.get('name')} {d.get('arguments')}"
    if t == "tool/result":
        try:
            return d["message"]["content"][0]["content"][0]["text"]
        except Exception:
            return json.dumps(d)[:200000]
    if t == "agent/inbox/spliced":
        return json.dumps(d)
    if t == "user/message":
        return corpus.text_of(d.get("message", {}).get("content")) or json.dumps(d)[:20000]
    if t == "web/deepseek-search-llm-request":
        return json.dumps(d)
    if t == "deliverables/presented":
        return json.dumps(d)
    if t == "subagent/descriptor":
        return json.dumps(d)
    return json.dumps(d)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern")
    ap.add_argument("--max", type=int, default=60)
    ap.add_argument("--ctx", type=int, default=160)
    ap.add_argument("--sid", default=None)
    ap.add_argument("--types", default=None)
    ap.add_argument("--case", action="store_true")
    ap.add_argument("--width", type=int, default=0, help="0=use ctx")
    args = ap.parse_args()

    flags = re.I if args.case else 0
    rx = re.compile(args.pattern, flags)
    width = args.width or args.ctx
    types = set(args.types.split(",")) if args.types else None
    n = 0
    total = 0
    for sid, path in corpus.session_paths():
        if args.sid and args.sid not in sid:
            continue
        # read header/descriptor cheaply
        label = ""
        parent = ""
        depth = ""
        evs = []
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
                if types and tt not in types:
                    continue
                evs.append(o)
        for o in evs:
            b = blob_of(o)
            for m in rx.finditer(b):
                total += 1
                if n >= args.max:
                    continue
                n += 1
                s = max(0, m.start() - width // 3)
                e = min(len(b), m.end() + width)
                snip = b[s:e].replace("\n", " \\n ")
                print(f"{o.get('time')} {sid[:12]} L[{label[:38]}] d{depth} {o.get('type')} seq={o.get('seq')} ::{snip}::")
                break
    print(f"--- {n} shown of {total} matching events ---", file=sys.stderr)


if __name__ == "__main__":
    main()
