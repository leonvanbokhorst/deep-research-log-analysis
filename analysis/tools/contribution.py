"""Map final-report claims back to the research process.

Method: for each section of the final amplification report, find the shared
workspace artefacts whose vocabulary best matches that section, then map those
artefacts to their first-writer session and delegation depth. This gives an
evidence-based (if imperfect) attribution of which branches actually supplied
material to which part of the report.

Vocabulary matching is a proxy for contribution, NOT a substitute for reading.
It is used only to rank candidates; the notes files and the correction analysis
carry the interpretive weight.

Outputs:
  analysis/tables/contribution.csv      report section -> artefacts -> branch
  analysis/tables/branch_outputs.csv    per session: artefacts written + inherited reads
"""

from __future__ import annotations

import csv
import math
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

WS_RESEARCH = "/Users/leonvanbokhorst/repos/deep-research"
REPORT = os.path.join(WS_RESEARCH, "amplification",
                      "Agentic-Threat-Amplification-2026.md")
OUT = os.path.join(C.WORKSPACE, "analysis", "data")
TAB = os.path.join(C.WORKSPACE, "analysis", "tables")

STOP = set("""the a an and or of to in for on with by is are was were be been being
that this these those it its as at from into than then so such not no nor but if
which who whom whose what when where how all any both each few more most other
some only own same too very can will just should now we you they he she i their
there here about above after again against because before below between during
during out off over under while would could may might must have has had do does
did doing also however therefore thus would's it's""".split())


def tokens(t: str) -> Counter:
    w = re.findall(r"[a-zA-Z][a-zA-Z\-]{3,}", t.lower())
    return Counter(x for x in w if x not in STOP)


def read(p):
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def main():
    rep = read(REPORT)
    if not rep:
        print("report not found")
        return

    # split into sections on level-2/3 headings
    parts = re.split(r"\n(?=#{2,3} )", rep)
    sections = []
    for p in parts:
        m = re.match(r"(#{2,3}) (.+)", p)
        if m:
            sections.append((m.group(2).strip(), p))

    # candidate artefacts: the shared workspace, excluding raw captures >400KB
    cands = []
    for root, dirs, files in os.walk(WS_RESEARCH):
        dirs[:] = [d for d in dirs if d not in (".git", "tools", "node_modules")]
        for fn in files:
            if not fn.endswith((".md", ".txt")):
                continue
            p = os.path.join(root, fn)
            sz = os.path.getsize(p)
            if sz > 400_000 or sz < 400:
                continue
            rel = os.path.relpath(p, WS_RESEARCH)
            cands.append((rel, p, sz))

    # provenance: first writer session per path
    prov = {}
    fp = os.path.join(OUT, "fileprovenance.csv")
    if os.path.exists(fp):
        for r in csv.DictReader(open(fp)):
            prov[r["path"]] = r

    # session labels/depth
    sess = {}
    for r in csv.DictReader(open(os.path.join(OUT, "sessions.csv"))):
        sess[r["session"]] = {"depth": r["depth"], "label": r["label"],
                              "tokens": int(r["totalTokens"])}

    rows = []
    for title, body in sections:
        if len(body) < 600:
            continue
        bt = tokens(body)
        scored = []
        for rel, p, sz in cands:
            ct = tokens(read(p))
            if not ct:
                continue
            # cosine-ish similarity over shared vocabulary
            common = set(bt) & set(ct)
            if len(common) < 12:
                continue
            dot = sum(bt[k] * ct[k] for k in common)
            na = math.sqrt(sum(v * v for v in bt.values()))
            nb = math.sqrt(sum(v * v for v in ct.values()))
            sim = dot / (na * nb) if na and nb else 0
            scored.append((sim, rel, len(common)))
        scored.sort(reverse=True)
        top = scored[:6]
        for sim, rel, nc in top:
            pr = prov.get(rel, {})
            sid = pr.get("firstWriterSession", "")
            rows.append({
                "reportSection": title[:90],
                "artefact": rel[:110],
                "similarity": round(sim, 4),
                "sharedTerms": nc,
                "firstWriterSession": sid,
                "firstWriterDepth": pr.get("firstWriteDepth", ""),
                "firstWriterLabel": (sess.get(sid, {}) or {}).get("label", "")[:60],
                "inheritedReads": pr.get("readsInheritingFromOtherSession", ""),
            })
    with open(os.path.join(TAB, "contribution.csv"), "w", newline="",
              encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        cw.writeheader()
        cw.writerows(rows)
    print(f"  contribution.csv: {len(rows)} rows, {len(sections)} sections")

    # per-session output/consumption profile
    bp = os.path.join(OUT, "fileprovenance.csv")
    written = defaultdict(list)
    consumed = Counter()
    if os.path.exists(bp):
        for r in csv.DictReader(open(bp)):
            if r["path"].endswith((".sh", ".py")):
                continue
            if r["firstWriterSession"]:
                written[r["firstWriterSession"]].append(
                    (r["path"], int(r["readsInheritingFromOtherSession"] or 0)))
            for s in (r.get("sessions") or "").split(";"):
                pass
    brows = []
    for sid, info in sess.items():
        arts = written.get(sid, [])
        brows.append({
            "session": sid, "depth": info["depth"], "label": info["label"][:60],
            "totalTokens": info["tokens"],
            "artefactsWritten": len(arts),
            "artefactsInheritedByOthers": sum(1 for _, n in arts if n > 0),
            "totalInheritedReads": sum(n for _, n in arts),
            "topArtefact": (max(arts, key=lambda x: x[1])[0][:70] if arts else ""),
        })
    brows.sort(key=lambda r: -r["totalInheritedReads"])
    with open(os.path.join(TAB, "branch_outputs.csv"), "w", newline="",
              encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(brows[0].keys()))
        cw.writeheader()
        cw.writerows(brows)
    print(f"  branch_outputs.csv: {len(brows)} rows")

    # console
    by_branch = Counter()
    for r in rows:
        if r["similarity"] > 0.30 and r["firstWriterLabel"]:
            by_branch[r["firstWriterLabel"]] += 1
    print("\n  branches contributing most to report sections (sim>0.30):")
    for k, v in by_branch.most_common(18):
        print(f"    {v:>4}  {k}")
    print("\n  sessions whose artefacts others inherited most:")
    for r in brows[:14]:
        print(f"    d{r['depth']} inh={r['totalInheritedReads']:<5} "
              f"arts={r['artefactsWritten']:<3} tok={r['totalTokens']:>11,}  "
              f"{r['label'][:40]}")


if __name__ == "__main__":
    main()
