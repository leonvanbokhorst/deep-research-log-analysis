#!/usr/bin/env python3
"""Print events from a specific session by seq range or type filter."""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import corpus  # noqa: E402


def text_of_event(o: dict) -> str:
    t = o.get("type")
    d = o.get("data") or {}
    if t == "assistant/message":
        return corpus.text_of((d.get("message") or {}).get("content"))
    if t == "tool/call":
        return f"[{d.get('name')}] {d.get('arguments')}"
    if t == "tool/result":
        try:
            return d["message"]["content"][0]["content"][0]["text"]
        except Exception:
            return json.dumps(d)
    if t == "agent/inbox/spliced":
        out = []
        for ins in d.get("inserted", []):
            for c in ins.get("content", []):
                if isinstance(c, dict):
                    out.append(c.get("text") or json.dumps(c))
        return "\n".join(out)
    if t == "user/message":
        return corpus.text_of((d.get("message") or {}).get("content"))
    if t == "subagent/descriptor":
        return json.dumps(d)
    return json.dumps(d)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sid")
    ap.add_argument("--lo", type=int, default=-1)
    ap.add_argument("--hi", type=int, default=10**9)
    ap.add_argument("--types", default=None)
    ap.add_argument("--maxchars", type=int, default=4000)
    args = ap.parse_args()
    types = set(args.types.split(",")) if args.types else None
    paths = dict(corpus.session_paths())
    key = None
    for sid in paths:
        if args.sid in sid:
            key = sid
            break
    if key is None:
        print("no session", file=sys.stderr)
        return
    s = corpus.load_session(key, paths[key])
    print(f"### session {key} parent={s.parent} depth={s.depth} label={s.label!r}")
    for o in s.events:
        if types and o.get("type") not in types:
            continue
        seq = o.get("seq") or 0
        if not (args.lo <= seq <= args.hi):
            continue
        t = text_of_event(o)
        print(f"\n=== [{o.get('time')}] seq={seq} {o.get('type')} ===")
        print(t[: args.maxchars])


if __name__ == "__main__":
    main()
