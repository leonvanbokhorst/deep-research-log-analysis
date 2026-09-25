"""Marginal epistemic return: novelty per phase of model work.

Joins the precomputed per-step usage table to event timestamps, defines four
phases by root-turn boundaries, and measures, per phase:

  work            steps, output tokens, reasoning tokens, fresh input tokens
  retrieval       target acts, query acts, new distinct hosts, new distinct URLs
  claims          new distinct "fact tokens" (comma numbers, decimal %, SD)
  artefacts       new workspace artefacts first written in that phase
  epistemics      negative-finding / correction / open-question marker events
  confidence      assertoric-language marker events

Search-proxy hosts (news.google.com etc.) are excluded from new-host counts so
the series measures *primary source* discovery, not search-engine use.

Outputs: analysis/work/marginal_by_phase.csv, marginal_tokens.csv and
         analysis/work/fact_token_firsts.csv
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import datetime
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

ANA = os.path.join(C.WORKSPACE, "analysis")
WORK = os.path.join(ANA, "work")

# Phase boundaries: root turn start times (corpus UTC, ms).
P1, P2, P3, P4, P5 = 1790324474000, 1790327859000, 1790328766000, 1790329663000, 1790330236601
PHASES = [
    ("P1 batch-1 build (turns 1-6)", P1, P2),
    ("P2 batch-2 build (turn 7)", P2, P3),
    ("P3 batch-2 extension (turns 8-14)", P3, P4),
    ("P4 finalisation (turns 15-18)", P4, P5),
]


def phase_of(t):
    for name, a, b in PHASES:
        if a <= t < b:
            return name
    return "outside"


def clock(t):
    return datetime.datetime.utcfromtimestamp(t / 1000).strftime("%H:%M:%S")


FACT_RX = [
    re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b"),          # 5,000 / 116,014
    re.compile(r"\b\d{1,3}\.\d+\s?%"),                        # 55.5%
    re.compile(r"\b\d{1,2}\.\d+\s?(?:SD|percentage points)\b"),
]
NEG_RX = re.compile(
    r"(?i)\b(no evidence|no case|not found|no documented|absence of evidence|"
    r"failed to find|non-finding|no verified case|never observed|no record)\b")
CORR_RX = re.compile(
    r"(?i)\b(retract(?:ed|ion)?|withdrawn|withdraw|correction|corrected|"
    r"superseded|unverifiable|single[- ]source|debunked|initially claimed|"
    r"report initially)\b")
OPEN_RX = re.compile(
    r"(?i)\b(unanswered|open question|remains unknown|no data|data gap|"
    r"research gap|not been systematically|would count as convincing|"
    r"we do not know|cannot be determined)\b")
CONF_RX = re.compile(
    r"(?i)\b(clearly|clearly established|strongly supported|high confidence|"
    r"conclusive|decisive|definitively|demonstrably|without doubt|"
    r"is settled|proven)\b")


def main():
    # ---- step -> time ------------------------------------------------
    step_time = {}
    with open(os.path.join(WORK, "tl_assistant.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            k = (r["session"], r.get("turn"), r.get("step"))
            t = r["time"]
            if k not in step_time or t < step_time[k]:
                step_time[k] = t
    print("step_time entries", len(step_time))

    # ---- work per phase ----------------------------------------------
    work = defaultdict(lambda: Counter())
    unmatched = 0
    with open(os.path.join(ANA, "data", "usage_steps.csv")) as f:
        for r in csv.DictReader(f):
            k = (r["session"], int(r["turn"]) if r["turn"] else None,
                 int(r["step"]) if r["step"] else None)
            t = step_time.get(k)
            if t is None:
                unmatched += 1
                continue
            p = phase_of(t)
            w = work[p]
            w["steps"] += 1
            w["outputTokens"] += int(r["outputTokens"])
            w["reasoningTokens"] += int(r["reasoningTokens"])
            w["freshInput"] += int(r["freshInput"])
            w["totalTokens"] += int(r["totalTokens"])
    print("unmatched usage steps", unmatched)

    # ---- retrieval: targets & queries --------------------------------
    prox = set()
    with open(os.path.join(ANA, "data", "hosts.csv")) as f:
        for r in csv.DictReader(f):
            if r["isSearchProxy"] == "True":
                prox.add(r["host"])
    print("search-proxy hosts", len(prox))

    seen_host = {}
    seen_url = {}
    new_hosts = Counter()
    new_urls = Counter()
    host_first = {}
    with open(os.path.join(ANA, "data", "targets.csv")) as f:
        rows = sorted(csv.DictReader(f), key=lambda r: int(r["time"]))
    for r in rows:
        t = int(r["time"])
        h = r["host"]
        if h in prox:
            continue
        p = phase_of(t)
        if h not in seen_host:
            seen_host[h] = t
            new_hosts[p] += 1
            host_first[h] = (t, r["url"])
        u = r["url"]
        if u not in seen_url:
            seen_url[u] = t
            new_urls[p] += 1
    q = Counter()
    with open(os.path.join(ANA, "data", "queries.csv")) as f:
        for r in csv.DictReader(f):
            q[phase_of(int(r["time"]))] += 1

    # ---- fact tokens --------------------------------------------------
    fact_first = {}
    with open(os.path.join(WORK, "tl_assistant.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            txt = r.get("text") or ""
            if not txt:
                continue
            t = r["time"]
            p = phase_of(t)
            for rx in FACT_RX:
                for m in rx.finditer(txt):
                    tok = m.group(0)
                    if tok not in fact_first:
                        fact_first[tok] = (t, p, r["session"], r.get("label"),
                                           txt[max(0, m.start() - 80):m.end() + 80]
                                           .replace("\n", " ")[:200])
    fact_by_phase = Counter(v[1] for v in fact_first.values())

    # ---- artefacts ----------------------------------------------------
    art = Counter()
    art_rows = []
    with open(os.path.join(ANA, "data", "fileprovenance.csv")) as f:
        for r in csv.DictReader(f):
            if not r["firstWriteTime"]:
                continue
            t = int(r["firstWriteTime"])
            p = phase_of(t)
            art[p] += 1
            art_rows.append((t, p, r["path"], r["firstWriteDepth"],
                             r["firstWriterSession"]))

    # ---- epistemic markers -------------------------------------------
    neg = Counter(); corr = Counter(); opn = Counter(); conf = Counter()
    marker_first = {"neg": {}, "corr": {}, "open": {}, "conf": {}}
    with open(os.path.join(WORK, "tl_assistant.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            txt = r.get("text") or ""
            if not txt:
                continue
            t = r["time"]; p = phase_of(t)
            for rx, ctr, key in ((NEG_RX, neg, "neg"), (CORR_RX, corr, "corr"),
                                 (OPEN_RX, opn, "open"), (CONF_RX, conf, "conf")):
                for m in rx.finditer(txt):
                    ctr[p] += 1
                    tok = m.group(0).lower()
                    if tok not in marker_first[key]:
                        marker_first[key][tok] = (t, p, r["session"], r.get("label"))

    # ---- write tables -------------------------------------------------
    names = [n for n, _, _ in PHASES]
    with open(os.path.join(WORK, "marginal_by_phase.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["phase", "steps", "outputTokens", "reasoningTokens", "freshInput",
                     "totalTokens", "targetActs", "queryActs", "newHosts", "newUrls",
                     "newFactTokens", "newArtefacts",
                     "negMarkers", "corrMarkers", "openMarkers", "confMarkers"])
        tgt = Counter()
        with open(os.path.join(ANA, "data", "targets.csv")) as fh:
            for r in csv.DictReader(fh):
                tgt[phase_of(int(r["time"]))] += 1
        for n in names:
            w = work[n]
            cw.writerow([n, w["steps"], w["outputTokens"], w["reasoningTokens"],
                         w["freshInput"], w["totalTokens"], tgt[n], q[n],
                         new_hosts[n], new_urls[n], fact_by_phase[n], art[n],
                         neg[n], corr[n], opn[n], conf[n]])
    print(open(os.path.join(WORK, "marginal_by_phase.csv")).read())

    # fact-token timing detail
    with open(os.path.join(WORK, "fact_token_firsts.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["token", "time", "clock", "phase", "session", "label", "context"])
        for tok, (t, p, s, lab, ctx) in sorted(fact_first.items(), key=lambda kv: kv[1][0]):
            cw.writerow([tok, t, clock(t), p, s, lab, ctx])

    # host firsts
    with open(os.path.join(WORK, "host_firsts.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["host", "time", "clock", "phase", "url"])
        for h, (t, u) in sorted(host_first.items(), key=lambda kv: kv[1][0]):
            cw.writerow([h, t, clock(t), phase_of(t), u])

    # artefacts
    with open(os.path.join(WORK, "artefact_firsts.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["time", "clock", "phase", "path", "firstWriteDepth", "session"])
        for t, p, path, dep, s in sorted(art_rows):
            cw.writerow([t, clock(t), p, path, dep, s])

    # marker firsts
    with open(os.path.join(WORK, "marker_firsts.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["kind", "marker", "time", "clock", "phase", "session", "label"])
        for key in ("neg", "corr", "open", "conf"):
            for tok, (t, p, s, lab) in sorted(marker_first[key].items(), key=lambda kv: kv[1][0]):
                cw.writerow([key, tok, t, clock(t), p, s, lab])
    print("wrote fact_token_firsts / host_firsts / artefact_firsts / marker_firsts")


if __name__ == "__main__":
    main()
