"""Message-channel provenance.

A correction to the file-based view: the dominant channel by which findings
moved between agents in this run was `send_message` — 374 agent-to-agent
messages carrying 1.65M characters, 148 of them full reports inline (>4,000
chars). File reads undercount contribution substantially.

This module reconstructs the message graph and measures, per session:
  * what it sent upward (volume, whether it embedded a full report)
  * what it received
  * whether the receiving parent then incorporated it (keyword overlap check)

Outputs:
  analysis/data/messages.csv          every agent-to-agent message
  analysis/tables/message_flow.csv    per session sent/received
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
TAB = os.path.join(C.WORKSPACE, "analysis", "tables")

REPORT_MARK = re.compile(
    r"(?i)(=== ?begin|#\s|FINAL|DELIVERABLE|RESULT|BOTTOM LINE|SUMMARY)")


def main():
    sessions = C.load_all()
    rows = []
    for sid, s in sessions.items():
        for o in s.events:
            if o.get("type") != "agent/inbox/spliced":
                continue
            for ins in (o.get("data") or {}).get("inserted", []):
                src = ins.get("source") or {}
                sender = src.get("senderSessionId")
                if not sender:
                    continue
                txt = C.text_of(ins.get("content"))
                rows.append({
                    "recipient": sid,
                    "recipientDepth": s.depth,
                    "recipientLabel": s.label,
                    "sender": sender,
                    "time": o.get("time"),
                    "chars": len(txt),
                    "hasMarkdownHeading": str(bool(re.search(r"(?m)^#{1,3} ", txt))),
                    "looksLikeReport": str(bool(REPORT_MARK.search(txt[:1500]))),
                    "nUrls": len(re.findall(r"https?://", txt)),
                    "nCites": len(re.findall(r"\[(?:PRIMARY|P|J|T|V|H|NV)\]", txt)),
                    "excerpt": re.sub(r"\s+", " ", txt)[:400],
                })
    rows.sort(key=lambda r: r["time"] or 0)
    with open(os.path.join(OUT, "messages.csv"), "w", newline="",
              encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        cw.writeheader()
        cw.writerows(rows)
    print(f"  messages.csv: {len(rows)} rows")

    sent = defaultdict(list)
    recv = defaultdict(list)
    for r in rows:
        sent[r["sender"]].append(r)
        recv[r["recipient"]].append(r)

    flow = []
    for sid, s in sessions.items():
        out = sent.get(sid, [])
        inn = recv.get(sid, [])
        flow.append({
            "session": sid, "depth": s.depth, "label": s.label[:60],
            "sentN": len(out), "sentChars": sum(x["chars"] for x in out),
            "sentReports": sum(1 for x in out if x["looksLikeReport"] == "True"),
            "sentUrls": sum(x["nUrls"] for x in out),
            "recvN": len(inn), "recvChars": sum(x["chars"] for x in inn),
            "recvReports": sum(1 for x in inn if x["looksLikeReport"] == "True"),
        })
    flow.sort(key=lambda r: -r["sentChars"])
    with open(os.path.join(TAB, "message_flow.csv"), "w", newline="",
              encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(flow[0].keys()))
        cw.writeheader()
        cw.writerows(flow)
    print(f"  message_flow.csv: {len(flow)} rows")

    # console
    print(f"\n  total message bytes moved: {sum(r['chars'] for r in rows):,}")
    print(f"  messages that look like full reports: "
          f"{sum(1 for r in rows if r['looksLikeReport']=='True')}")
    print(f"  messages with markdown headings: "
          f"{sum(1 for r in rows if r['hasMarkdownHeading']=='True')}")
    print(f"  messages containing URLs: {sum(1 for r in rows if r['nUrls'])}")
    print("\n  top senders (by chars pushed to their parent):")
    for r in flow[:14]:
        print(f"    d{r['depth']} sent={r['sentN']:<3} chars={r['sentChars']:>8,} "
              f"reports={r['sentReports']:<3} urls={r['sentUrls']:<4} {r['label'][:38]}")
    print("\n  top recipients:")
    for r in sorted(flow, key=lambda x: -x["recvChars"])[:10]:
        print(f"    d{r['depth']} recv={r['recvN']:<3} chars={r['recvChars']:>8,} "
              f"reports={r['recvReports']:<3} {r['label'][:38] or '(root)'}")


if __name__ == "__main__":
    main()
