"""Build the reconstructed session/agent genealogy and token/cache ledger.

Outputs (analysis/data/):
  sessions.csv            one row per session (node)
  edges.csv               parent -> child delegation edges
  usage_steps.csv         one row per assistant step (usage + context metrics)
  usage_session.csv       per-session usage rollup
  toolcalls.csv           one row per tool call
  corrections_candidates  (handled elsewhere)

All logic is deterministic; re-running reproduces identical output.
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
os.makedirs(OUT, exist_ok=True)

UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")


def w(name, rows, cols):
    p = os.path.join(OUT, name)
    with open(p, "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        cw.writeheader()
        for r in rows:
            cw.writerow(r)
    print(f"  {name}: {len(rows)} rows")
    return p


def main():
    sessions = C.load_all()
    print(f"loaded {len(sessions)} sessions")

    # ---- per session metadata -------------------------------------------------
    rows = []
    usage_rows = []
    tool_rows = []
    edges = []

    # map child session id -> (spawn label, descriptor, prompt text, spawn provenance)
    spawn_info: dict[str, dict] = {}

    for sid, s in sessions.items():
        calls = list(C.all_tool_calls(s))
        results = list(C.all_tool_results(s))
        name_calls = Counter(c.get("name") for c in calls)

        # collect subagent spawns from this session
        for c in calls:
            if c.get("name") == "subagent":
                try:
                    a = json.loads(c.get("arguments") or "{}")
                except json.JSONDecodeError:
                    a = {}
                spawn_info.setdefault("_pending", {})
                spawn_info.setdefault("_by_call", {})[c.get("callId")] = {
                    "parent": sid,
                    "description": a.get("description"),
                    "prompt": a.get("prompt") or "",
                    "run_in_background": a.get("run_in_background"),
                    "callTime": c.get("_time"),
                }
            elif c.get("name") == "subagent_fork":
                try:
                    a = json.loads(c.get("arguments") or "{}")
                except json.JSONDecodeError:
                    a = {}
                spawn_info.setdefault("_by_call", {})[c.get("callId")] = {
                    "parent": sid,
                    "description": a.get("description"),
                    "prompt": a.get("prompt") or "",
                    "run_in_background": a.get("run_in_background"),
                    "fork": True,
                    "callTime": c.get("_time"),
                }

        # catalog events: authoritative childId + label + createdAt
        for o in s.events:
            if o.get("type") == "subagent/catalog":
                d = o.get("data") or {}
                spawn_info.setdefault(d.get("childId"), {})
                spawn_info[d["childId"]].update(
                    {"parent": sid, "label": d.get("label"),
                     "childCreatedAt": d.get("childCreatedAt"),
                     "mode": d.get("mode"), "catalogTime": o.get("time")}
                )

        # message serialisation: find child ids named in tool results
        result_text_by_call = {}
        for r in results:
            src = (r.get("message", {}) or {}).get("source", {}) or {}
            cid = src.get("callId")
            if cid:
                result_text_by_call[cid] = C.text_of(
                    (r.get("message", {}) or {}).get("content")
                )
        for cid, txt in result_text_by_call.items():
            if cid in spawn_info.get("_by_call", {}):
                info = spawn_info["_by_call"][cid]
                info["result_text"] = (txt or "")[:2000]
                # child id appears in text like "started subagent <uuid>"
                m = UUID_RE.search(txt or "")
                if m:
                    cid2 = m.group(0)
                    spawn_info.setdefault(cid2, {}).update(info)
                    spawn_info[cid2]["childId"] = cid2
                else:
                    spawn_info.setdefault("_unlinked", []).append(
                        {"callId": cid, "parent": sid, "text": (txt or "")[:200]}
                    )

        # steps + usage
        n_steps = 0
        turn_times = {}
        for turn, step, d, cs, rs in C.iter_steps(s):
            u = d.get("usage") or {}
            msg = d.get("message") or {}
            content = msg.get("content") or []
            rtext = "\n".join(
                c.get("text") or "" for c in content if isinstance(c, dict) and c.get("type") == "reasoning"
            )
            otext = "\n".join(
                c.get("text") or "" for c in content if isinstance(c, dict) and c.get("type") == "text"
            )
            tin = int(u.get("inputTokens") or 0)
            tcr = int(u.get("cacheReadTokens") or 0)
            tout = int(u.get("outputTokens") or 0)
            trea = int(u.get("reasoningTokens") or 0)
            ttot = int(u.get("totalTokens") or 0)
            usage_rows.append({
                "session": sid, "depth": s.depth, "turn": turn, "step": step,
                "inputTokens": tin, "cacheReadTokens": tcr, "outputTokens": tout,
                "reasoningTokens": trea, "totalTokens": ttot,
                "logicalContext": tin + tcr,
                "freshInput": tin,
                "reasoningChars": len(rtext), "outputChars": len(otext),
                "nToolCalls": len(cs),
            })
            n_steps += 1

        # session rollup
        tot_in = sum(r["inputTokens"] for r in usage_rows if r["session"] == sid)
        tot_cr = sum(r["cacheReadTokens"] for r in usage_rows if r["session"] == sid)
        tot_out = sum(r["outputTokens"] for r in usage_rows if r["session"] == sid)
        tot_rea = sum(r["reasoningTokens"] for r in usage_rows if r["session"] == sid)
        tot_all = sum(r["totalTokens"] for r in usage_rows if r["session"] == sid)
        max_ctx = max([r["logicalContext"] for r in usage_rows if r["session"] == sid] or [0])
        times = [C.ev_time(o) for o in s.events if o.get("time")]
        rows.append({
            "session": sid, "parent": s.parent or "", "depth": s.depth,
            "origin": s.header.get("origin", "root"),
            "label": s.label,
            "createdAt": s.created_at,
            "firstEvent": min(times) if times else 0,
            "lastEvent": max(times) if times else 0,
            "nEvents": len(s.events),
            "nSteps": n_steps,
            "nToolCalls": sum(name_calls.values()),
            "nSubagentSpawns": name_calls.get("subagent", 0) + name_calls.get("subagent_fork", 0),
            "nSendMessage": name_calls.get("send_message", 0),
            "nPresent": name_calls.get("present", 0),
            "nWebSearch": name_calls.get("web_search", 0),
            "nWebFetch": name_calls.get("web_fetch", 0),
            "nBash": name_calls.get("bash", 0),
            "nRead": name_calls.get("read", 0),
            "nWrite": name_calls.get("write", 0),
            "nEdit": name_calls.get("edit", 0),
            "nGrep": name_calls.get("grep", 0),
            "nGlob": name_calls.get("glob", 0),
            "inputTokens": tot_in, "cacheReadTokens": tot_cr,
            "outputTokens": tot_out, "reasoningTokens": tot_rea,
            "totalTokens": tot_all,
            "logicalContext": tot_in + tot_cr,
            "maxStepContext": max_ctx,
            "malformed": s.malformed,
            "provider": (s.descriptor or {}).get("agentProvider", ""),
            "model": (s.descriptor or {}).get("agentModel", ""),
            "reasoningEffort": (s.descriptor or {}).get("agentReasoningEffort", ""),
            "mode": (s.descriptor or {}).get("mode", ""),
        })

        # tool calls
        for c in calls:
            try:
                a = json.loads(c.get("arguments") or "{}")
            except json.JSONDecodeError:
                a = {}
            tool_rows.append({
                "session": sid, "depth": s.depth, "turn": c.get("turn"), "step": c.get("step"),
                "name": c.get("name"),
                "argKeys": "|".join(sorted(a.keys())),
                "argChars": len(c.get("arguments") or ""),
                "description": (a.get("description") or "")[:200],
                "query": (a.get("query") or a.get("url") or a.get("command") or "")[:300],
                "callId": c.get("callId"),
            })

    # ---- edges ---------------------------------------------------------------
    catalog_seen = set()
    for child, info in spawn_info.items():
        if child in ("_pending", "_by_call") or not isinstance(info, dict):
            continue
        if "parent" not in info:
            continue
        cat = sessions.get(child)
        edges.append({
            "parent": info.get("parent"),
            "child": child,
            "label": info.get("label") or (cat.label if cat else ""),
            "description": info.get("description") or "",
            "promptChars": len(info.get("prompt") or ""),
            "prompt": (info.get("prompt") or "").replace("\n", " ")[:4000],
            "childCreatedAt": info.get("childCreatedAt") or (cat.created_at if cat else ""),
            "parentCatalogTime": info.get("catalogTime") or "",
            "inCorpus": str(child in sessions),
            "fork": str(bool(info.get("fork"))),
        })
        catalog_seen.add(child)

    # sessions present in corpus but not referenced by any catalog (orphan edges)
    referenced = {e["child"] for e in edges}
    for sid, s in sessions.items():
        if sid == C.MAIN_SESSION_ID or sid in referenced or not s.parent:
            continue
        # fall back to the session header's own parentSession pointer
        edges.append({"parent": s.parent, "child": sid, "label": s.label,
                      "description": "", "promptChars": "", "prompt": "",
                      "childCreatedAt": s.created_at, "parentCatalogTime": "",
                      "inCorpus": "True", "fork": "False", "link": "header"})
    for e in edges:
        e.setdefault("link", "catalog")
    # only keep edges whose child really is in the corpus
    edges = [e for e in edges if e["child"] in sessions]

    edges.sort(key=lambda e: (e["parent"], e["child"]))
    w("sessions.csv", rows, list(rows[0].keys()))
    w("edges.csv", edges, list(edges[0].keys()))
    w("usage_steps.csv", usage_rows, list(usage_rows[0].keys()))
    w("toolcalls.csv", tool_rows, list(tool_rows[0].keys()))

    # ---- console summary -----------------------------------------------------
    print("\n=== TOTALS ===")
    for k in ("inputTokens", "cacheReadTokens", "outputTokens", "logicalContext"):
        print(f"  {k}: {sum(r[k] for r in rows):,}")
    print("  nSessions:", len(rows))
    print("  nSteps:", len(usage_rows))
    print("  nToolCalls:", len(tool_rows))
    print("  nEdges:", len(edges))
    print("  spawns without corpus child:",
          sum(1 for e in edges if e["inCorpus"] != "True"))


if __name__ == "__main__":
    main()
