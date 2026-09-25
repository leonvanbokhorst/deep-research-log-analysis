"""Derived quantitative tables for the genealogy, timing, cache and scaling analyses.

Outputs (analysis/data/ and analysis/tables/):
  genealogy.json          tree with per-node metrics
  branch_table.csv        per-branch (depth-1 subtree) rollup
  cache_by_depth.csv      token/cache composition by delegation depth
  cache_timeline.csv      cache behaviour over the life of the run
  marginal_return.csv     novelty/redundancy proxies in 10% deciles of model work
  stops.csv               per-session start/end/queue behaviour
"""

from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

OUT = os.path.join(C.WORKSPACE, "analysis", "data")
TAB = os.path.join(C.WORKSPACE, "analysis", "tables")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TAB, exist_ok=True)


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
    main_id = C.MAIN_SESSION_ID

    # ---------- per-session metrics -----------------------------------------
    meta = {}
    for sid, s in sessions.items():
        times = [o["time"] for o in s.events if o.get("time")]
        calls = list(C.all_tool_calls(s))
        name_calls = Counter(c.get("name") for c in calls)
        usage = []
        for turn, step, d, cs, rs in C.iter_steps(s):
            u = d.get("usage") or {}
            usage.append((u.get("inputTokens") or 0, u.get("cacheReadTokens") or 0,
                          u.get("outputTokens") or 0, u.get("reasoningTokens") or 0,
                          u.get("totalTokens") or 0))
        # prompts it received that were written by agents (inbox) vs user
        inbox_agent = 0
        inbox_user = 0
        for o in s.events:
            if o.get("type") != "agent/inbox/spliced":
                continue
            for ins in (o.get("data") or {}).get("inserted", []):
                src = (ins.get("source") or {})
                if src.get("kind") == "agent" or src.get("senderSessionId"):
                    inbox_agent += 1
                else:
                    inbox_user += 1
        meta[sid] = {
            "session": sid,
            "parent": s.parent,
            "depth": s.depth,
            "label": s.label,
            "origin": s.header.get("origin", "root"),
            "preset": s.header.get("agentPreset", ""),
            "createdAt": s.created_at,
            "t0": min(times) if times else None,
            "t1": max(times) if times else None,
            "nEvents": len(s.events),
            "nSteps": len(usage),
            "nToolCalls": len(calls),
            "nTurns": len([o for o in s.events if o.get("type") == "turn/start"]),
            "nSpawns": name_calls.get("subagent", 0) + name_calls.get("subagent_fork", 0),
            "nSendMessage": name_calls.get("send_message", 0),
            "nPresent": name_calls.get("present", 0),
            "nWebFetch": name_calls.get("web_fetch", 0),
            "nWebSearch": name_calls.get("web_search", 0),
            "nBash": name_calls.get("bash", 0),
            "nInboxAgent": inbox_agent,
            "nInboxUser": inbox_user,
            "inTokens": sum(u[0] for u in usage),
            "crTokens": sum(u[1] for u in usage),
            "outTokens": sum(u[2] for u in usage),
            "reaTokens": sum(u[3] for u in usage),
            "totalTokens": sum(u[4] for u in usage),
            "maxCtx": max([u[0] + u[1] for u in usage] or [0]),
            "malformed": s.malformed,
            "model": (s.descriptor or {}).get("agentModel", ""),
            "mode": (s.descriptor or {}).get("mode", ""),
            "endSeed": any(o.get("type") == "session/end-seed" for o in s.events),
        }
        meta[sid]["wallclockMs"] = (meta[sid]["t1"] - meta[sid]["t0"]) if times else 0
        meta[sid]["firstStepCtx"] = usage[0][0] + usage[0][1] if usage else 0

    # ---------- tree ---------------------------------------------------------
    children = defaultdict(list)
    for sid, m in meta.items():
        if m["parent"]:
            children[m["parent"]].append(sid)

    def descendants(sid):
        out = []
        stack = list(children[sid])
        while stack:
            x = stack.pop()
            out.append(x)
            stack.extend(children[x])
        return out

    for sid in meta:
        d = descendants(sid)
        meta[sid]["nDescendants"] = len(d)
        meta[sid]["descendantTokens"] = sum(meta[x]["totalTokens"] for x in d)
        meta[sid]["subtreeTokens"] = meta[sid]["totalTokens"] + meta[sid]["descendantTokens"]
        meta[sid]["nChildren"] = len(children[sid])
        meta[sid]["nLeaves"] = sum(1 for x in d if not children[x]) if d else (1 if not children[sid] else 0)

    # ---------- branch table (subtree rooted at each depth-1 node) -----------
    branches = []
    for sid, m in meta.items():
        if m["depth"] != 1:
            continue
        sub = [sid] + descendants(sid)
        # branch start = earliest created, end = latest event
        sub_meta = [meta[x] for x in sub]
        branches.append({
            "branchSession": sid,
            "label": m["label"],
            "createdAt": m["createdAt"],
            "branchStart": min(x["t0"] for x in sub_meta if x["t0"]),
            "branchEnd": max(x["t1"] for x in sub_meta if x["t1"]),
            "wallclockMin": round((max(x["t1"] for x in sub_meta if x["t1"])
                                   - min(x["t0"] for x in sub_meta if x["t0"])) / 60000, 2),
            "nSessions": len(sub),
            "nSessionsDepth1": 1,
            "nDescendants": len(sub) - 1,
            "maxSubDepth": max(meta[x]["depth"] for x in sub),
            "nSteps": sum(meta[x]["nSteps"] for x in sub),
            "nToolCalls": sum(meta[x]["nToolCalls"] for x in sub),
            "nWebFetch": sum(meta[x]["nWebFetch"] for x in sub),
            "nBash": sum(meta[x]["nBash"] for x in sub),
            "totalTokens": sum(meta[x]["totalTokens"] for x in sub),
            "cacheReadTokens": sum(meta[x]["crTokens"] for x in sub),
            "inputTokens": sum(meta[x]["inTokens"] for x in sub),
            "outputTokens": sum(meta[x]["outTokens"] for x in sub),
            "maxCtx": max(meta[x]["maxCtx"] for x in sub),
            "nPresents": sum(meta[x]["nPresent"] for x in sub),
            "maxBranchFactor": max(meta[x]["nChildren"] for x in sub),
        })
    branches.sort(key=lambda r: -r["totalTokens"])
    write_csv(os.path.join(TAB, "branch_table.csv"), branches)

    # ---------- cache by depth ----------------------------------------------
    dagg = defaultdict(lambda: Counter())
    for sid, m in meta.items():
        d = dagg[m["depth"]]
        for k in ("inTokens", "crTokens", "outTokens", "reaTokens", "totalTokens",
                  "nSteps", "nToolCalls", "nSessions", "nSpawns", "nWebFetch", "nBash"):
            d[k] += m[k] if k != "nSessions" else 1
    rows = []
    for dep in sorted(dagg):
        d = dagg[dep]
        latch = d["inTokens"] + d["crTokens"]
        rows.append({
            "depth": dep, "nSessions": d["nSessions"], "nSteps": d["nSteps"],
            "nToolCalls": d["nToolCalls"], "nSpawns": d["nSpawns"],
            "nWebFetch": d["nWebFetch"], "nBash": d["nBash"],
            "inputTokens": d["inTokens"], "cacheReadTokens": d["crTokens"],
            "outputTokens": d["outTokens"], "reasoningTokens": d["reaTokens"],
            "totalTokens": d["totalTokens"],
            "logicalInput": latch,
            "cacheHitPct": round(100 * d["crTokens"] / max(1, latch), 2),
            "tokensPerStep": round(d["totalTokens"] / max(1, d["nSteps"])),
            "tokensPerSession": round(d["totalTokens"] / max(1, d["nSessions"])),
            "outputSharePct": round(100 * d["outTokens"] / max(1, d["totalTokens"]), 3),
        })
    write_csv(os.path.join(TAB, "cache_by_depth.csv"), rows)

    # ---------- cache timeline (equal-count bins over model work) -----------
    all_steps = []
    for sid, s in sessions.items():
        step_time = {}
        for o in s.events:
            if o.get("type") == "assistant/message":
                d0 = o.get("data") or {}
                step_time[(d0.get("turn"), d0.get("step"))] = o.get("time") or 0
        for turn, step, d, cs, rs in C.iter_steps(s):
            u = d.get("usage") or {}
            all_steps.append((step_time.get((turn, step), 0), sid, meta[sid]["depth"],
                              u.get("inputTokens") or 0, u.get("cacheReadTokens") or 0,
                              u.get("outputTokens") or 0, u.get("totalTokens") or 0))
    all_steps.sort(key=lambda x: x[0])
    N = len(all_steps)
    NB = 20
    rows = []
    for b in range(NB):
        lo, hi = b * N // NB, (b + 1) * N // NB
        chunk = all_steps[lo:hi]
        if not chunk:
            continue
        tin = sum(c[3] for c in chunk)
        tcr = sum(c[4] for c in chunk)
        tout = sum(c[5] for c in chunk)
        tot = sum(c[6] for c in chunk)
        rows.append({
            "bin": b + 1, "pctOfSteps": f"{(b+1)*100//NB}%",
            "stepFrom": lo, "stepTo": hi, "nSteps": len(chunk),
            "tStart": chunk[0][0], "tEnd": chunk[-1][0],
            "inputTokens": tin, "cacheReadTokens": tcr, "outputTokens": tout,
            "totalTokens": tot,
            "logicalInput": tin + tcr,
            "cacheHitPct": round(100 * tcr / max(1, tin + tcr), 2),
            "meanDepth": round(sum(c[2] for c in chunk) / len(chunk), 2),
            "meanCtxPerStep": round((tin + tcr) / len(chunk)),
            "distinctSessions": len({c[1] for c in chunk}),
        })
    write_csv(os.path.join(OUT, "cache_timeline.csv"), rows)

    # ---------- novelty / redundancy proxy by decile ------------------------
    # proxy: distinct new external URLs fetched, new shared artefacts written,
    # new sessions started, new corrections-ish markers, per decile of work.
    rd = os.path.join(OUT, "retrieval.csv")
    retr = list(csv.DictReader(open(rd))) if os.path.exists(rd) else []
    for r in retr:
        r["time"] = int(r["time"] or 0)
    retr.sort(key=lambda r: r["time"])
    win = os.path.join(OUT, "fileprovenance.csv")
    prov = list(csv.DictReader(open(win))) if os.path.exists(win) else []
    sess_by_time = sorted(meta.values(), key=lambda m: m["t0"] or 0)

    # rank every "act" by time, then bin by decile of the act sequence
    acts = []
    for r in retr:
        acts.append((r["time"], "retrieval", r))
    for sid, m in meta.items():
        if m["t0"]:
            acts.append((m["t0"], "session_start", m))
        if m["t1"]:
            acts.append((m["t1"], "session_end", m))
    acts.sort(key=lambda x: x[0])

    total_tokens = sum(m["totalTokens"] for m in meta.values())
    # cumulative token proxy: assign each act a token weight = its session's
    # tokens / that session's number of acts (so deciles are work-weighted)
    acts_per_session = Counter(a[2]["session"] for a in acts if a[1] == "retrieval")
    rows = []
    seen_urls = set()
    seen_hosts = set()
    for dec in range(10):
        lo, hi = dec * len(acts) // 10, (dec + 1) * len(acts) // 10
        chunk = acts[lo:hi]
        new_urls, new_hosts = [], []
        for t, kind, r in chunk:
            if kind != "retrieval":
                continue
            for u in (r.get("structuredSources") or "").split(";"):
                u = u.strip()
                if not u or u in seen_urls:
                    continue
                seen_urls.add(u)
                new_urls.append(u)
                h = u.split("/")[2] if "//" in u else u
                if h not in seen_hosts:
                    seen_hosts.add(h)
                    new_hosts.append(h)
        rows.append({
            "decile": dec + 1,
            "pctOfWork": f"{(dec+1)*10}%",
            "nActs": len(chunk),
            "nRetrievals": sum(1 for _, k, _ in chunk if k == "retrieval"),
            "nSessionsStarted": sum(1 for _, k, _ in chunk if k == "session_start"),
            "nSessionsEnded": sum(1 for _, k, _ in chunk if k == "session_end"),
            "distinctSessionsActive": len({r["session"] for _, k, r in chunk
                                           if k == "retrieval"}),
            "newStructuredUrls": len(new_urls),
            "newHosts": len(new_hosts),
            "cumStructuredUrls": len(seen_urls),
            "tStart": chunk[0][0] if chunk else "",
            "tEnd": chunk[-1][0] if chunk else "",
        })
    write_csv(os.path.join(TAB, "marginal_return.csv"), rows)

    # ---------- save genealogy json -----------------------------------------
    with open(os.path.join(OUT, "genealogy.json"), "w", encoding="utf-8") as f:
        json.dump({
            "root": main_id,
            "nodes": meta,
            "children": {k: v for k, v in children.items()},
            "totals": {
                "nSessions": len(meta),
                "nEdges": sum(len(v) for v in children.values()),
                "nSteps": sum(m["nSteps"] for m in meta.values()),
                "nToolCalls": sum(m["nToolCalls"] for m in meta.values()),
                "totalTokens": total_tokens,
                "inputTokens": sum(m["inTokens"] for m in meta.values()),
                "cacheReadTokens": sum(m["crTokens"] for m in meta.values()),
                "outputTokens": sum(m["outTokens"] for m in meta.values()),
                "reasoningTokens": sum(m["reaTokens"] for m in meta.values()),
                "wallclockMs": max(m["t1"] for m in meta.values())
                              - min(m["t0"] for m in meta.values() if m["t0"]),
                "maxDepth": max(m["depth"] for m in meta.values()),
                "nLeaves": sum(1 for m in meta.values() if m["nChildren"] == 0),
                "nRecursivelyDelegating": sum(1 for m in meta.values() if m["nSpawns"] > 0),
            },
        }, f, indent=1, default=str)
    print(f"  genealogy.json written")

    # ---------- console ------------------------------------------------------
    t = sum(m["totalTokens"] for m in meta.values())
    print("\n=== TREE ===")
    print(f"  sessions {len(meta)}  leaves {sum(1 for m in meta.values() if m['nChildren']==0)}"
          f"  max depth {max(m['depth'] for m in meta.values())}")
    print(f"  sessions that themselves delegated: "
          f"{sum(1 for m in meta.values() if m['nSpawns']>0)}"
          f"  (total spawn calls {sum(m['nSpawns'] for m in meta.values())})")
    print(f"  wallclock {(max(m['t1'] for m in meta.values())-min(m['t0'] for m in meta.values() if m['t0']))/60000:.1f} min")
    print(f"  total tokens {t:,}")
    print("\n  depth  sessions  tokens          cacheHit%  tok/session")
    for r in read_cache_by_depth():
        print(f"  {r['depth']:>5}  {r['nSessions']:>8}  {int(r["totalTokens"]):>14,}  "
              f"{r['cacheHitPct']:>9}  {int(r["tokensPerSession"]):>11,}")


def read_cache_by_depth():
    p = os.path.join(TAB, "cache_by_depth.csv")
    return list(csv.DictReader(open(p)))


if __name__ == "__main__":
    main()
