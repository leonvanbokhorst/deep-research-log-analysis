#!/usr/bin/env python3
"""Timeline statistics: how many agent steps / sessions occur in a time window."""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import corpus  # noqa: E402
from grepcorpus import blob_of  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--t0", type=int, required=True)
    ap.add_argument("--t1", type=int, required=True)
    ap.add_argument("--pattern", default=None)
    args = ap.parse_args()

    steps = 0
    sessions_with_steps = set()
    sessions_matching = set()
    matches_in_window = 0
    for sid, path in corpus.session_paths():
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = o.get("time")
                if t is None or not (args.t0 <= t <= args.t1):
                    continue
                if o.get("type") == "step/start":
                    steps += 1
                    sessions_with_steps.add(sid)
                if args.pattern and __import__("re").search(args.pattern, blob_of(o)):
                    matches_in_window += 1
                    sessions_matching.add(sid)
    print(f"window [{args.t0},{args.t1}] span={(args.t1-args.t0)/1000:.1f}s")
    print(f"step/start events: {steps}  in {len(sessions_with_steps)} sessions")
    if args.pattern:
        print(f"matching events: {matches_in_window} in {len(sessions_matching)} sessions")


if __name__ == "__main__":
    main()
