"""Stream a compact event timeline out of the immutable corpus.

Single streaming pass over main + subagent session files. Never holds the whole
corpus in memory: one session file is read line by line and discarded.

Outputs (analysis/work/):
  tl_presented.csv     every deliverables/presented event
  tl_inbox.jsonl       every agent/inbox/spliced inserted message, with source
  tl_writes.csv        every write/edit/multi_edit tool call with its paths
  tl_root_text.jsonl   root assistant text + tool call names, per step
  tl_assistant.jsonl   assistant text for ALL sessions (for finding-timing search)
"""

from __future__ import annotations

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

WORK = os.path.join(C.WORKSPACE, "analysis", "work")
os.makedirs(WORK, exist_ok=True)

WRITE_TOOLS = {"write", "edit", "multi_edit", "create_file", "str_replace_editor"}


def paths_from_args(name, args):
    """Best-effort extraction of file paths touched by a write-ish tool call."""
    out = []
    if not isinstance(args, dict):
        return out
    for k in ("file_path", "path", "filePath", "filename"):
        v = args.get(k)
        if isinstance(v, str):
            out.append(v)
    for k in ("edits", "files"):
        v = args.get(k)
        if isinstance(v, list):
            for it in v:
                if isinstance(it, dict):
                    for kk in ("file_path", "path"):
                        if isinstance(it.get(kk), str):
                            out.append(it[kk])
    return out


def main():
    sessions = C.session_paths()
    f_pres = open(os.path.join(WORK, "tl_presented.csv"), "w", newline="", encoding="utf-8")
    f_wr = open(os.path.join(WORK, "tl_writes.csv"), "w", newline="", encoding="utf-8")
    f_inbox = open(os.path.join(WORK, "tl_inbox.jsonl"), "w", encoding="utf-8")
    f_root = open(os.path.join(WORK, "tl_root_text.jsonl"), "w", encoding="utf-8")
    f_asst = open(os.path.join(WORK, "tl_assistant.jsonl"), "w", encoding="utf-8")

    cw_pres = csv.writer(f_pres)
    cw_pres.writerow(["time", "session", "depth", "label", "turn", "nFiles", "paths", "descriptions"])
    cw_wr = csv.writer(f_wr)
    cw_wr.writerow(["time", "session", "depth", "label", "turn", "step", "tool", "path", "argChars"])

    desclabels = {}
    n_pres = n_wr = n_inbox = 0

    for sid, path in sessions:
        header = {}
        descriptor = None
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = o.get("type")
                if t == "session":
                    header = o
                    continue
                if t == "subagent/descriptor":
                    descriptor = o.get("data") or {}
                    continue
                tm = int(o.get("time") or 0)
                d = o.get("data") or {}
                depth = int(header.get("delegationDepth") or 0)
                label = (descriptor or {}).get("label") or ""
                if t == "deliverables/presented":
                    files = d.get("files") or []
                    ps = [x.get("path", "") for x in files if isinstance(x, dict)]
                    ds = [x.get("description", "")[:300] for x in files if isinstance(x, dict)]
                    cw_pres.writerow([tm, sid, depth, label, d.get("turn"), len(files),
                                      "|".join(ps), " || ".join(ds)])
                    n_pres += 1
                elif t == "agent/inbox/spliced":
                    for ins in (d.get("inserted") or []):
                        src = ins.get("source") or {}
                        rec = {
                            "time": tm, "session": sid, "depth": depth, "label": label,
                            "target": d.get("target"),
                            "sourceKind": src.get("kind") or src.get("type"),
                            "sender": src.get("senderSessionId") or src.get("sessionId"),
                            "text": C.text_of(ins.get("content")),
                        }
                        f_inbox.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        n_inbox += 1
                elif t == "tool/call":
                    name = d.get("name") or ""
                    if name in WRITE_TOOLS:
                        raw = d.get("arguments") or "{}"
                        try:
                            args = json.loads(raw) if isinstance(raw, str) else (raw or {})
                        except json.JSONDecodeError:
                            args = {}
                        for p in paths_from_args(name, args):
                            cw_wr.writerow([tm, sid, depth, label, d.get("turn"), d.get("step"),
                                            name, p, len(raw)])
                            n_wr += 1
                elif t == "assistant/message":
                    txt = C.text_of((d.get("message") or {}).get("content"))
                    calls = []
                    for c in ((d.get("message") or {}).get("content") or []):
                        if isinstance(c, dict) and c.get("type") == "tool-call":
                            calls.append(c.get("name") or c.get("toolName") or "")
                    rec = {"time": tm, "session": sid, "depth": depth, "label": label,
                           "turn": d.get("turn"), "step": d.get("step"),
                           "calls": calls, "text": txt}
                    f_asst.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    if sid == C.MAIN_SESSION_ID:
                        f_root.write(json.dumps(rec, ensure_ascii=False) + "\n")

    for fh in (f_pres, f_wr, f_inbox, f_root, f_asst):
        fh.close()
    print(f"presented={n_pres} writes={n_wr} inbox={n_inbox}")


if __name__ == "__main__":
    main()
