"""Classify every tool call by what it does to the SHARED workspace, and measure
how much of each agent's input was material produced by OTHER agents.

This is the core test for "propagated conclusion" vs "independent discovery":
if an agent's context is dominated by files written by its siblings/parent, its
agreement is inheritance, not convergence.

Outputs:
  analysis/data/io_acts.csv        one row per tool call with an I/O class
  analysis/data/io_matrix.csv      session x class counts
  analysis/data/fileprovenance.csv file -> first writer session, readers (all sessions)
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

# A path inside the original research workspace
DS = "/Users/leonvanbokhorst/repos/deep-research/"
PATH_RE = re.compile(
    re.escape(DS) + r"([A-Za-z0-9_\-][A-Za-z0-9_\-./]*\.[A-Za-z0-9]{1,5})")
# relative mention of a shared artefact (e.g. cd into workspace then cat findings/x.md)
REL_RE = re.compile(
    r"(?:^|[\s\"'`(])((?:amplification|findings|notes|sources|research|tools)/"
    r"[A-Za-z0-9_\-./]+\.(?:md|txt|json|csv|py|sh|html|pdf))"
)

WRITE_TOOLS = {"write", "edit"}
READ_TOOLS = {"read", "grep", "glob"}
# shell verbs that consume file content
READ_VERBS = re.compile(
    r"\b(cat|head|tail|less|more|grep|rg|awk|sed|wc|sort|uniq|diff|jq|pdftotext|"
    r"python3?|node|open|Read)\b")
# shell constructs that create/modify files
WRITE_VERBS = re.compile(
    r"(>>?\s*[^|;&]*\.(?:md|txt|json|csv|py|sh|html)|"
    r"\btee\b|\bcp\b|\bmv\b|\bmkdir\b|\btouch\b|\bsed\s+-i\b|>\s*/)")


def classify(name: str, args: dict, text: str):
    """Return (io_class, paths, n_paths)."""
    paths: list[str] = []
    if name == "bash":
        cmd = args.get("command") or ""
        for m in PATH_RE.finditer(cmd):
            paths.append(m.group(1))
        if not paths:
            for m in REL_RE.finditer(cmd):
                paths.append(m.group(1))
        paths = list(dict.fromkeys(paths))
        if not paths:
            return "bash_other", [], 0
        w = bool(WRITE_VERBS.search(cmd))
        r = bool(READ_VERBS.search(cmd))
        if w and not r:
            return "shared_write", paths, len(paths)
        if w and r:
            return "shared_rw", paths, len(paths)
        return "shared_read", paths, len(paths)
    if name in WRITE_TOOLS:
        p = args.get("file_path") or ""
        if p:
            paths.append(p.replace(DS, ""))
        return "shared_write", paths, len(paths)
    if name in READ_TOOLS:
        p = args.get("file_path") or args.get("path") or ""
        if p:
            paths.append(p.replace(DS, ""))
        return "shared_read", paths, len(paths)
    if name == "web_fetch":
        return "external_fetch", [], 0
    if name == "web_search":
        return "external_search", [], 0
    if name in ("subagent", "subagent_fork"):
        return "delegation", [], 0
    if name in ("send_message", "list_agents", "interrupt_agent"):
        return "agent_coordination", [], 0
    if name == "present":
        return "deliverable", [], 0
    return "other", [], 0


def main():
    sessions = C.load_all()
    acts = []
    matrix: dict[str, Counter] = defaultdict(Counter)
    writers: dict[str, list] = defaultdict(list)   # rel path -> [(time, sid, depth)]
    readers: dict[str, list] = defaultdict(list)

    for sid, s in sessions.items():
        for c in C.all_tool_calls(s):
            name = c.get("name")
            try:
                a = json.loads(c.get("arguments") or "{}")
            except json.JSONDecodeError:
                a = {}
            cls, paths, n = classify(name, a, "")
            matrix[sid][cls] += 1
            if cls in ("shared_write", "shared_rw"):
                for p in paths:
                    writers[p].append((c.get("_time") or 0, sid, s.depth))
            if cls in ("shared_read", "shared_rw"):
                for p in paths:
                    readers[p].append((c.get("_time") or 0, sid, s.depth))
            acts.append({
                "session": sid, "depth": s.depth, "label": s.label,
                "time": c.get("_time"), "turn": c.get("turn"), "step": c.get("step"),
                "tool": name, "ioClass": cls, "nPaths": n,
                "firstPath": paths[0] if paths else "",
                "allPaths": ";".join(paths[:8]),
            })

    with open(os.path.join(OUT, "io_acts.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(acts[0].keys()))
        cw.writeheader()
        cw.writerows(acts)

    # ---- the decisive measure: did a session READ a file that another session WROTE
    #      BEFORE that read? (temporal, so we can prove inheritance of material)
    prov = []
    for p in sorted(set(list(writers) + list(readers))):
        ws = sorted(writers.get(p, []))
        rs = sorted(readers.get(p, []))
        first_w = ws[0] if ws else None
        w_sessions = {w[1] for w in ws}
        r_sessions = {r[1] for r in rs}
        # reads that happened after some *other* session wrote the file
        inherited = 0
        for (t, sid, d) in rs:
            if any(wt < t and wsid != sid for (wt, wsid, _wd) in ws):
                inherited += 1
        prov.append({
            "path": p,
            "nWriteActs": len(ws),
            "nWriteSessions": len(w_sessions),
            "nReadActs": len(rs),
            "nReadSessions": len(r_sessions),
            "firstWriterSession": first_w[1] if first_w else "",
            "firstWriteTime": first_w[0] if first_w else "",
            "firstWriteDepth": first_w[2] if first_w else "",
            "readsInheritingFromOtherSession": inherited,
            "crossSession": str(bool(w_sessions & r_sessions and
                                     (w_sessions - r_sessions or len(w_sessions) > 1))
                                or inherited > 0),
        })
    prov.sort(key=lambda r: (-r["readsInheritingFromOtherSession"], -r["nReadActs"]))
    with open(os.path.join(OUT, "fileprovenance.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(prov[0].keys()))
        cw.writeheader()
        cw.writerows(prov)

    # ---- per-session I/O matrix
    allc = sorted({c for v in matrix.values() for c in v})
    rows = []
    for sid in sorted(matrix):
        r = {"session": sid, "depth": sessions[sid].depth, "label": sessions[sid].label}
        r.update({c: matrix[sid].get(c, 0) for c in allc})
        r["sharedIOPct"] = round(
            100 * sum(matrix[sid].get(c, 0) for c in
                      ("shared_read", "shared_rw", "shared_write"))
            / max(1, sum(matrix[sid].values())), 1)
        rows.append(r)
    with open(os.path.join(OUT, "io_matrix.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        cw.writeheader()
        cw.writerows(rows)

    # ---- console
    cls_tot = Counter()
    for c in matrix.values():
        cls_tot.update(c)
    print("I/O class totals:", dict(cls_tot.most_common()))
    print(f"\nio_acts.csv {len(acts)} | fileprovenance.csv {len(prov)} rows")
    tot_inh = sum(r["readsInheritingFromOtherSession"] for r in prov)
    cross = [r for r in prov if r["readsInheritingFromOtherSession"] > 0]
    print(f"paths whose content was read by a session AFTER another session wrote it: "
          f"{len(cross)} files, {tot_inh} read acts")
    print("\ntop inherited artefacts (read after being written by another agent):")
    for r in cross[:20]:
        print(f"  {r['readsInheritingFromOtherSession']:>4} inherited reads | "
              f"{r['nWriteSessions']} writer(s) | {r['path'][:90]}")


if __name__ == "__main__":
    main()
