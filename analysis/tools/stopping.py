"""Scaling and stopping analysis.

Question: does the log contain observable signals that would support a practical
stopping rule? Three candidate signals are tested:

  S1  marginal new-artefact rate per unit of model work
  S2  marginal new-source (host) rate per unit of model work
  S3  correction/adjudication activity, by phase

Plus a phase decomposition of where the run's model work actually went:
research-by-children vs synthesis-by-the-root.

Outputs:
  analysis/tables/phases.csv
  analysis/tables/stopping_signals.csv
  analysis/tables/agent_productivity.csv
"""

from __future__ import annotations

import csv
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

OUT = os.path.join(C.WORKSPACE, "analysis", "data")
TAB = os.path.join(C.WORKSPACE, "analysis", "tables")
MAIN = C.MAIN_SESSION_ID


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        cw.writeheader()
        cw.writerows(rows)
    print(f"  {os.path.relpath(path, C.WORKSPACE)}: {len(rows)} rows")


def main():
    sessions = C.load_all()
    sess = {r["session"]: r for r in csv.DictReader(open(os.path.join(OUT, "sessions.csv")))}
    prov = list(csv.DictReader(open(os.path.join(OUT, "fileprovenance.csv"))))
    disc = list(csv.DictReader(open(os.path.join(TAB, "discovery_by_work.csv"))))

    meta = {}
    for sid, s in sessions.items():
        times = [o["time"] for o in s.events if o.get("time")]
        meta[sid] = {"depth": s.depth, "label": s.label,
                     "t0": min(times) if times else 0,
                     "t1": max(times) if times else 0}

    # ---------- agent productivity: artefact produced AND consumed ----------
    produced = defaultdict(list)
    for r in prov:
        if r["path"].endswith((".sh", ".py")):
            continue
        if r["firstWriterSession"]:
            produced[r["firstWriterSession"]].append(r)

    rows = []
    for sid, sessobj in sessions.items():
        arts = produced.get(sid, [])
        consumed = sum(int(a["readsInheritingFromOtherSession"] or 0) for a in arts)
        tok = int(sess[sid]["totalTokens"])
        rows.append({
            "session": sid, "depth": sessobj.depth, "label": sessobj.label[:60],
            "totalTokens": tok,
            "nSteps": sess[sid]["nSteps"],
            "artefacts": len(arts),
            "inheritedReadsReceived": consumed,
            "productive": str(consumed > 0),
            "tokensPerInheritedRead": (round(tok / consumed) if consumed else ""),
            "presented": sess[sid]["nPresent"],
        })
    rows.sort(key=lambda r: -int(r["totalTokens"]))
    write_csv(os.path.join(TAB, "agent_productivity.csv"), rows)

    # ---------- phase decomposition -----------------------------------------
    # Define phases by the ROOT session's turn structure (observed turning points)
    root = sessions[MAIN]
    turn_t = {}
    for o in root.events:
        if o.get("type") == "turn/start":
            turn_t[o["data"]["turn"]] = o["time"]
    ordered = sorted(turn_t.items())
    bounds = [(1, 6, "P1 topic-1 build (turns 1-6)"),
              (7, 7, "P2 topic-2 build (turn 7)"),
              (8, 14, "P3 topic-2 extension (turns 8-14)"),
              (15, 18, "P4 finalisation (turns 15-18)")]

    def tok_in(sid, lo, hi):
        tot = 0
        for turn, step, d, cs, rs in C.iter_steps(sessions[sid]):
            if lo <= (turn or 0) <= hi:
                tot += (d.get("usage") or {}).get("totalTokens") or 0
        return tot

    # root tokens per phase
    rows = []
    t_first = min(m["t0"] for m in meta.values() if m["t0"])
    t_last = max(m["t1"] for m in meta.values() if m["t1"])
    for lo, hi, name in bounds:
        rt = tok_in(MAIN, lo, hi)
        # children alive in this window
        tlo = turn_t.get(lo, t_first)
        thi = turn_t.get(hi + 1, t_last + 1)
        alive = [sid for sid, m in meta.items()
                 if sid != MAIN and m["t0"] < thi and m["t1"] >= tlo]
        ct = sum(int(sess[sid]["totalTokens"]) for sid in alive)
        rows.append({
            "phase": name,
            "rootTurns": f"{lo}-{hi}",
            "rootTokens": rt,
            "childTokens": ct,
            "totalTokens": rt + ct,
            "childSessionsAlive": len(alive),
            "rootSharePct": round(100 * rt / max(1, rt + ct), 1),
        })
    write_csv(os.path.join(TAB, "phases.csv"), rows)

    # ---------- stopping signals --------------------------------------------
    # S1: new artefacts written per step-bin (from io_acts + provenance)
    acts = list(csv.DictReader(open(os.path.join(OUT, "io_acts.csv"))))
    steps_all = []
    for sid, s in sessions.items():
        for o in s.events:
            if o.get("type") == "assistant/message":
                steps_all.append(o.get("time") or 0)
    steps_all.sort()
    N = len(steps_all)
    NB = 10
    first_written = {}
    for r in prov:
        if r["firstWriteTime"] and r["firstWriterSession"]:
            first_written[r["path"]] = int(r["firstWriteTime"])
    seen_art = set()
    rows = []
    for b in range(NB):
        lo, hi = b * N // NB, (b + 1) * N // NB
        t_lo = steps_all[lo]
        t_hi = steps_all[min(hi, N - 1)]
        new_art = [p for p, t in first_written.items() if t_lo <= t <= t_hi]
        for p in new_art:
            seen_art.add(p)
        d = disc[b]
        rows.append({
            "bin": b + 1, "pctOfWork": f"{(b+1)*100//NB}%",
            "nSteps": hi - lo,
            "newArtefacts": len(new_art),
            "newHosts": int(d["newHosts"]),
            "newQueries": int(d["newQueries"]),
            "cumArtefacts": len(seen_art),
            "sessionsActive": int(d["sessionsActive"]),
            "meanDepth": d["meanDepth"],
        })
    write_csv(os.path.join(TAB, "stopping_signals.csv"), rows)

    # ---------- console ------------------------------------------------------
    allp = list(csv.DictReader(open(os.path.join(TAB, "agent_productivity.csv"))))
    tot_tok = sum(int(r["totalTokens"]) for r in allp)
    ptok = sum(int(r["totalTokens"]) for r in allp if r["productive"] == "True")
    print(f"\n  sessions whose artefacts were inherited by others: "
          f"{sum(1 for r in allp if r['productive']=='True')} / {len(allp)}")
    print(f"  tokens spent in those sessions: {ptok:,} / {tot_tok:,} "
          f"({100*ptok/tot_tok:.1f}%)")
    print("\n  phases:")
    print("    %-34s %12s %12s %8s %8s" % ("phase", "rootTok", "childTok", "child#", "root%"))
    for r in list(csv.DictReader(open(os.path.join(TAB, "phases.csv")))):
        print("    %-34s %12s %12s %8s %8s" % (r["phase"], f"{int(r['rootTokens']):,}",
                                               f"{int(r['childTokens']):,}",
                                               r["childSessionsAlive"], r["rootSharePct"]))
    print("\n  stopping signals:")
    print("    %6s %10s %10s %10s %10s" % ("bin", "newArts", "newHosts", "newQueries", "active"))
    for r in list(csv.DictReader(open(os.path.join(TAB, "stopping_signals.csv")))):
        print("    %6s %10s %10s %10s %10s" % (r["pctOfWork"], r["newArtefacts"],
                                               r["newHosts"], r["newQueries"],
                                               r["sessionsActive"]))


if __name__ == "__main__":
    main()
