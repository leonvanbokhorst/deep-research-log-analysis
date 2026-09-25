"""Source-discovery, redundancy and marginal-return analysis.

Because the built-in web_search failed for most of the run (119/135 calls
errored), discovery actually happened through ~6,458 shell retrieval acts and
1,361 web_fetch calls. This module reconstructs discovery from those acts:

  * normalised search queries and their repetition across sessions
  * hosts actually targeted (bash curl/wget URLs + web_fetch URLs + structured
    meta sources) -> source diversity over time
  * re-fetch of the same host/URL by different sessions (redundancy)
  * equal-work deciles of novelty

Outputs:
  analysis/tables/discovery.csv        per decile of work
  analysis/data/queries.csv            every search query + who ran it
  analysis/data/targets.csv            every retrieval target URL/host
  analysis/tables/redundancy.csv       repeated queries and repeated hosts
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

OUT = os.path.join(C.WORKSPACE, "analysis", "data")
TAB = os.path.join(C.WORKSPACE, "analysis", "tables")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TAB, exist_ok=True)

URL_RE = re.compile(r"https?://[^\s\"'<>\)\],}\\]+")
Q_RE = re.compile(r"""(?:news\.sh|gn\.sh|news-nl\.sh|ddg\.sh|ddgs\.sh|web\.sh|s\.sh|"""
                  r"""jddg\.sh|wsearch\.sh|nc\.sh|bn\.sh|bs\.sh)\s+["']([^"']{5,200})["']""")


def host_of(u: str) -> str:
    try:
        h = urlparse(u).netloc.lower()
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def norm_q(q: str) -> str:
    q = q.lower()
    q = re.sub(r"[^a-z0-9 ]+", " ", q)
    return " ".join(q.split())


def write_csv(path, rows):
    if not rows:
        print(f"  (no rows) {path}")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        cw.writeheader()
        cw.writerows(rows)
    print(f"  {os.path.relpath(path, C.WORKSPACE)}: {len(rows)} rows")


def main():
    sessions = C.load_all()
    meta = {}
    for sid, s in sessions.items():
        times = [o["time"] for o in s.events if o.get("time")]
        meta[sid] = {"depth": s.depth, "label": s.label,
                     "t0": min(times) if times else 0}

    queries = []
    targets = []
    meta_sources = []

    for sid, s in sessions.items():
        calls = list(C.all_tool_calls(s))
        # structured sources from web tool meta
        for o in s.events:
            if o.get("type") != "tool/result":
                continue
            d = o.get("data") or {}
            src = (d.get("message", {}) or {}).get("source", {}) or {}
            for sc in ((d.get("meta") or {}).get("sources") or []):
                if isinstance(sc, dict) and sc.get("url"):
                    meta_sources.append({"session": sid, "depth": s.depth,
                                         "time": o.get("time") or 0,
                                         "url": sc["url"],
                                         "host": host_of(sc["url"]),
                                         "title": (sc.get("title") or "")[:200]})
        for c in calls:
            name = c.get("name")
            try:
                a = json.loads(c.get("arguments") or "{}")
            except json.JSONDecodeError:
                a = {}
            t = c.get("_time") or 0
            if name == "web_search":
                q = a.get("query") or ""
                queries.append({"session": sid, "depth": s.depth, "time": t,
                                "tool": "web_search", "query": q,
                                "normQuery": norm_q(q), "source": "tool"})
            elif name == "bash":
                cmd = a.get("command") or ""
                for m in Q_RE.finditer(cmd):
                    queries.append({"session": sid, "depth": s.depth, "time": t,
                                    "tool": "bash", "query": m.group(1),
                                    "normQuery": norm_q(m.group(1)), "source": "shell"})
                # an RSS/API search where the query is in a URL
                for m in re.finditer(r"[\?&](?:q|query|search)=([^&\"'\s]+)", cmd):
                    raw = m.group(1).replace("+", " ").replace("%20", " ")
                    if len(raw) > 4:
                        queries.append({"session": sid, "depth": s.depth, "time": t,
                                        "tool": "bash", "query": raw,
                                        "normQuery": norm_q(raw), "source": "url"})
                for u in URL_RE.findall(cmd):
                    u = u.rstrip(".,;:)]}\"'")
                    targets.append({"session": sid, "depth": s.depth, "time": t,
                                    "url": u, "host": host_of(u),
                                    "via": "bash"})
            elif name == "web_fetch":
                u = (a.get("url") or "").rstrip(".,;:)]}\"'")
                if u:
                    targets.append({"session": sid, "depth": s.depth, "time": t,
                                    "url": u, "host": host_of(u), "via": "web_fetch"})

    for m in meta_sources:
        targets.append({"session": m["session"], "depth": m["depth"], "time": m["time"],
                        "url": m["url"], "host": m["host"], "via": "meta"})

    # ---- dedupe targets excluding search-engine plumbing -------------------
    SEARCHY = {"news.google.com", "duckduckgo.com", "html.duckduckgo.com",
               "bing.com", "search.brave.com", "mojeek.com", "google.com",
               "r.jina.ai", "api.deepseek.com", "sitemaps.org", "w3.org",
               "search.yahoo.com", "youtube.com", "buttondown.email",
               "openalex.org", "export.arxiv.org", "api.semanticscholar.org",
               "api.crossref.org", "www.ebi.ac.uk", "eutils.ncbi.nlm.nih.gov"}
    real = [t for t in targets if t["host"] and t["host"] not in SEARCHY]

    write_csv(os.path.join(OUT, "queries.csv"), queries)
    write_csv(os.path.join(OUT, "targets.csv"), targets)
    write_csv(os.path.join(OUT, "meta_sources.csv"), meta_sources)

    # ---- query redundancy ---------------------------------------------------
    qc = defaultdict(set)
    qmeta = {}
    for q in queries:
        if len(q["normQuery"]) < 5:
            continue
        qc[q["normQuery"]].add(q["session"])
        qmeta.setdefault(q["normQuery"], q)
    rep = [{"normQuery": k, "nSessions": len(v), "nQueryEvents": sum(
        1 for q in queries if q["normQuery"] == k),
        "example": qmeta[k]["query"][:160],
        "firstTime": min(q["time"] for q in queries if q["normQuery"] == k)}
        for k, v in qc.items()]
    rep.sort(key=lambda r: (-r["nSessions"], -r["nQueryEvents"]))
    write_csv(os.path.join(TAB, "redundancy.csv"), rep)

    # ---- host reuse ---------------------------------------------------------
    hc = defaultdict(set)
    hcount = Counter()
    for t in real:
        hc[t["host"]].add(t["session"])
        hcount[t["host"]] += 1
    hrows = [{"host": h, "nSessions": len(v), "nTargetActs": hcount[h]}
             for h, v in hc.items()]
    hrows.sort(key=lambda r: (-r["nSessions"], -r["nTargetActs"]))
    write_csv(os.path.join(TAB, "host_reuse.csv"), hrows)

    acts = sorted([(q["time"], "query", q) for q in queries]
                  + [(t["time"], "target", t) for t in targets], key=lambda x: x[0])

    # ---- discovery over deciles of MODEL WORK ------------------------------
    # Binning by act sequence is wrong here: 16 depth-1 agents run in parallel,
    # so the first acts of the run already include every branch's opening move.
    # Bin instead by global assistant-step order (each bin = equal number of
    # model steps = equal model work), and attribute each retrieval act to the
    # bin containing the latest step of its own session that precedes it.
    steps = []
    for sid, s in sessions.items():
        for o in s.events:
            if o.get("type") == "assistant/message":
                steps.append((o.get("time") or 0, sid))
    steps.sort()
    step_time_of = defaultdict(list)
    for i, (t, sid) in enumerate(steps):
        step_time_of[sid].append(t)

    def step_index_for(sid, t):
        arr = step_time_of.get(sid)
        if not arr:
            return 0
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= t:
                lo = mid + 1
            else:
                hi = mid
        return lo  # number of steps in this session up to and including t

    # cumulative step counts per session, then a global ordering key
    # (sid, count) doesn't sort globally, so approximate global position by
    # interleaving: use the count of steps across ALL sessions whose time <= t.
    all_times = [t for t, _ in steps]

    def global_pos(t):
        import bisect
        return bisect.bisect_right(all_times, t)

    NSTEP = len(steps)
    NB = 10
    seen_hosts2, seen_urls2, seen_q2 = set(), set(), set()
    rows2 = []
    for b in range(NB):
        lo = b * NSTEP // NB
        hi = (b + 1) * NSTEP // NB
        t_lo = all_times[lo] if lo < NSTEP else 0
        t_hi = all_times[hi - 1] if hi - 1 < NSTEP else all_times[-1]
        # acts assigned by global step position of their timestamp
        chunk = [a for a in acts if t_lo <= a[0] <= t_hi]
        nh, nu, nq = [], [], []
        for t, k, o in chunk:
            if k == "target":
                if o["url"] not in seen_urls2:
                    seen_urls2.add(o["url"])
                    nu.append(o["url"])
                if o["host"] and o["host"] not in seen_hosts2:
                    seen_hosts2.add(o["host"])
                    nh.append(o["host"])
            else:
                if o["normQuery"] and o["normQuery"] not in seen_q2:
                    seen_q2.add(o["normQuery"])
                    nq.append(o["normQuery"])
        rows2.append({
            "decile": b + 1, "pctOfWork": f"{(b+1)*100//NB}%",
            "stepFrom": lo, "stepTo": hi,
            "nSteps": hi - lo,
            "nTargetActs": sum(1 for _, k, _ in chunk if k == "target"),
            "nQueryActs": sum(1 for _, k, _ in chunk if k == "query"),
            "newUrls": len(nu), "newHosts": len(nh), "newQueries": len(nq),
            "cumUrls": len(seen_urls2), "cumHosts": len(seen_hosts2),
            "cumQueries": len(seen_q2),
            "sessionsActive": len({o["session"] for _, _, o in chunk}),
            "meanDepth": round(sum(o["depth"] for _, _, o in chunk) / max(1, len(chunk)), 2),
            "tStart": t_lo, "tEnd": t_hi,
        })
    write_csv(os.path.join(TAB, "discovery_by_work.csv"), rows2)
    rows_console = rows2

    # ---- console ------------------------------------------------------------
    print(f"\n  unique normalised queries: {len(qc)}")
    print(f"  queries run by >1 session: "
          f"{sum(1 for v in qc.values() if len(v) > 1)} "
          f"({100*sum(1 for v in qc.values() if len(v)>1)/max(1,len(qc)):.1f}%)")
    print(f"  unique real hosts targeted: {len(hc)}")
    multh = [h for h, v in hc.items() if len(v) > 1]
    print(f"  hosts targeted by >1 session: {len(multh)} "
          f"({100*len(multh)/max(1,len(hc)):.1f}%)")
    print("\n  top repeated queries:")
    for r in rep[:12]:
        print(f"    x{r['nSessions']:<3} sessions  {r['example'][:95]}")
    print("\n  top reused hosts:")
    for r in hrows[:15]:
        print(f"    x{r['nSessions']:<3} sessions  {r['host'][:70]}")
    print("\n  discovery by decile:")
    print("    %6s %8s %8s %8s %10s %10s %10s" % ("dec", "steps", "newURLs",
                                              "newHosts", "cumURLs", "cumHosts", "cumQueries"))
    for r in rows_console:
        print("    %6s %8s %8s %8s %10s %10s %10s" % (r["pctOfWork"], r["nSteps"],
                                                     r["newUrls"], r["newHosts"],
                                                     r["cumUrls"], r["cumHosts"],
                                                     r["cumQueries"]))


if __name__ == "__main__":
    main()
