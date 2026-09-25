"""Build analysis/data/manifest.json — the immutable-corpus manifest.

Hashes every source file in the export, records sizes, line counts, and the
schema inventory of every event type observed. This is the audit anchor for the
whole analysis: nothing downstream is trustworthy unless it points here.
"""

from __future__ import annotations

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

OUT = os.path.join(C.WORKSPACE, "analysis", "data")


def schema_of(obj, prefix=""):
    """Return set of dotted key paths for a nested JSON object."""
    out = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            out.add(p)
            out |= schema_of(v, p)
    elif isinstance(obj, list):
        for v in obj[:2]:
            out |= schema_of(v, prefix + "[]")
    return out


def main():
    files = []
    total = 0
    type_counter = collections.Counter()
    key_paths: dict[str, set] = collections.defaultdict(set)
    seq_gaps = []

    for sid, path in C.session_paths():
        size = os.path.getsize(path)
        total += size
        nlines = 0
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                nlines += 1
        files.append({
            "sessionId": sid,
            "relPath": os.path.relpath(path, C.CORPUS_ROOT),
            "bytes": size,
            "lines": nlines,
            "sha256": C.sha256_file(path),
        })
        # schema inventory (cheap second pass, streaming)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    type_counter["__MALFORMED__"] += 1
                    continue
                t = o.get("type", "__NO_TYPE__")
                type_counter[t] += 1
                key_paths[t] |= schema_of(o)
                if t == "session":
                    key_paths["session"] |= schema_of(o)

    files.sort(key=lambda r: r["relPath"])
    manifest = {
        "corpusRoot": os.path.relpath(C.CORPUS_ROOT, C.WORKSPACE),
        "mainSessionId": C.MAIN_SESSION_ID,
        "nSessionFiles": len(files),
        "totalBytes": total,
        "totalLines": sum(f["lines"] for f in files),
        "hashAlgorithm": "sha256",
        "files": files,
        "eventTypeCounts": dict(type_counter.most_common()),
        "eventSchemas": {k: sorted(v) for k, v in sorted(key_paths.items())},
        "note": (
            "This export is the immutable primary dataset. Session-level rollups "
            "for the root session use MAIN_SESSION_ID. No file listed here was "
            "modified by the analysis process."
        ),
    }
    p = os.path.join(OUT, "manifest.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    print(f"wrote {p}")
    print(f"  files={len(files)} bytes={total:,} lines={manifest['totalLines']:,}")
    print(f"  event types: {len(type_counter)}")
    for k, v in type_counter.most_common(30):
        print(f"    {v:>8,}  {k}")
    print("\n  distinct key paths per notable type:")
    for t in ("assistant/message", "tool/call", "tool/result", "agent/inbox/spliced",
              "subagent/catalog", "subagent/descriptor", "deliverables/presented",
              "web/deepseek-search-llm-request", "todo/write", "session"):
        ks = sorted(key_paths.get(t, []))
        print(f"    {t} ({len(ks)}): {ks}")


if __name__ == "__main__":
    main()
