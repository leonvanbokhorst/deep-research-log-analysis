"""Decile-of-model-work series: novelty vs output, with self-referential noise removed.

Steps are ordered by event time (matching discovery_by_work.csv, whose deciles
are monotone in time) and split into ten bins of ~1004 steps.

Measures per decile:
  work        steps, output tokens, reasoning tokens, fresh input
  retrieval   target acts, query acts, new distinct hosts, new distinct URLs
  claims      new distinct *substantive* numeric fact tokens
  artefacts   new workspace artefacts first written
  epistemics  negative / correction / open-question / confidence marker events

A numeric token counts as substantive unless its surrounding window is about
the document itself (word counts, byte sizes, line counts, URLs).

Outputs: analysis/work/decile_series.csv, analysis/work/decile_facts.csv
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

FACT_RX = re.compile(
    r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|\b\d{1,3}\.\d+\s?%|"
    r"\b\d{1,2}\.\d+\s?(?:SD|percentage points)\b")
SELF_RX = re.compile(
    r"(?i)\b(words?|word count|bytes?|lines?|kb|mb|chars?|characters?|wc -w|"
    r"budget|over the|target|aim|trim|cut|compress|rewrite|draft)\b")
NEG_RX = re.compile(
    r"(?i)\b(no evidence|no case|not found|no documented|absence of evidence|"
    r"failed to find|non-finding|no verified case|never observed|no record)\b")
CORR_RX = re.compile(
    r"(?i)\b(retract(?:ed|ion)?|withdrawn|withdraw|correction|corrected|"
    r"superseded|unverifiable|single[- ]source|debunked)\b")
OPEN_RX = re.compile(
    r"(?i)\b(unanswered|open question|remains unknown|no data|data gap|"
    r"research gap|we do not know|cannot be determined)\b")
CONF_RX = re.compile(
    r"(?i)\b(clearly established|strongly supported|high confidence|"
    r"conclusive|decisive|definitively|demonstrably|is settled|proven)\b")


def clock(t):
    return datetime.datetime.utcfromtimestamp(t / 1000).strftime("%H:%M:%S")


def main():
    # step list ordered by time
    steps = []
    with open(os.path.join(WORK, "tl_assistant.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            steps.append((r["time"], r["session"], r.get("turn"), r.get("step")))
    steps.sort()
    usage = {}
    with open(os.path.join(ANA, "data", "usage_steps.csv")) as f:
        for r in csv.DictReader(f):
            usage[(r["session"], int(r["turn"]), int(r["step"]))] = r
    n = len(steps)
    nbins = 10
    binof = {}
    for i, (t, s, tu, st) in enumerate(steps):
        b = min(nbins - 1, i * nbins // n)
        binof[(s, tu, st, i)] = b
    # ordered lookup by (session,turn,step) -> bin (first occurrence)
    key_bin = {}
    for i, (t, s, tu, st) in enumerate(steps):
        k = (s, tu, st)
        if k not in key_bin:
            key_bin[k] = min(nbins - 1, i * nbins // n)

    work = defaultdict(Counter)
    for k, r in usage.items():
        b = key_bin.get(k)
        if b is None:
            continue
        work[b]["steps"] += 1
        work[b]["outputTokens"] += int(r["outputTokens"])
        work[b]["reasoningTokens"] += int(r["reasoningTokens"])
        work[b]["freshInput"] += int(r["freshInput"])
        work[b]["totalTokens"] += int(r["totalTokens"])
    # the time extents of each decile
    ext = {}
    for i, (t, s, tu, st) in enumerate(steps):
        b = min(nbins - 1, i * nbins // n)
        if b not in ext:
            ext[b] = [t, t]
        ext[b][1] = t

    # retrieval
    prox = set()
    with open(os.path.join(ANA, "data", "hosts.csv")) as f:
        for r in csv.DictReader(f):
            if r["isSearchProxy"] == "True":
                prox.add(r["host"])

    def bin_of_time(t):
        # find decile by the step-time extents
        for b in sorted(ext):
            if ext[b][0] <= t <= ext[b][1]:
                return b
        return max(ext) if t > ext[max(ext)][1] else 0

    seen_host, seen_url = set(), set()
    nh, nu = Counter(), Counter()
    tgt, qry = Counter(), Counter()
    with open(os.path.join(ANA, "data", "targets.csv")) as f:
        rows = sorted(csv.DictReader(f), key=lambda r: int(r["time"]))
    for r in rows:
        t = int(r["time"]); b = bin_of_time(t)
        tgt[b] += 1
        if r["host"] in prox:
            continue
        if r["host"] not in seen_host:
            seen_host.add(r["host"]); nh[b] += 1
        if r["url"] not in seen_url:
            seen_url.add(r["url"]); nu[b] += 1
    with open(os.path.join(ANA, "data", "queries.csv")) as f:
        for r in csv.DictReader(f):
            qry[bin_of_time(int(r["time"]))] += 1

    # fact tokens / markers
    ft = defaultdict(list)
    neg, corr, opn, conf = Counter(), Counter(), Counter(), Counter()
    seen_fact = {}
    with open(os.path.join(WORK, "tl_assistant.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            txt = r.get("text") or ""
            if not txt:
                continue
            t = r["time"]
            b = bin_of_time(t)
            for rx, ctr in ((NEG_RX, neg), (CORR_RX, corr), (OPEN_RX, opn), (CONF_RX, conf)):
                ctr[b] += len(rx.findall(txt))
            for m in FACT_RX.finditer(txt):
                tok = m.group(0)
                win = txt[max(0, m.start() - 70):m.end() + 70]
                if SELF_RX.search(win):
                    continue
                if tok in seen_fact:
                    continue
                seen_fact[tok] = (t, b, r["session"], r.get("label"), win.replace("\n", " "))
                ft[b].append(tok)

    art = Counter()
    with open(os.path.join(ANA, "data", "fileprovenance.csv")) as f:
        for r in csv.DictReader(f):
            if not r["firstWriteTime"]:
                continue
            art[bin_of_time(int(r["firstWriteTime"]))] += 1

    with open(os.path.join(WORK, "decile_series.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["decile", "pctWork", "tStart", "tEnd", "steps", "outputTokens",
                     "reasoningTokens", "freshInput", "totalTokens", "targetActs",
                     "queryActs", "newHosts", "newUrls", "newSubstantiveFacts",
                     "newArtefacts", "negMarkers", "corrMarkers", "openMarkers",
                     "confMarkers", "outTokPerNewHost", "outTokPerNewFact"])
        for b in range(nbins):
            w = work[b]
            cw.writerow([b + 1, f"{(b+1)*10}%", clock(ext[b][0]), clock(ext[b][1]),
                         w["steps"], w["outputTokens"], w["reasoningTokens"],
                         w["freshInput"], w["totalTokens"], tgt[b], qry[b], nh[b],
                         nu[b], len(ft[b]), art[b], neg[b], corr[b], opn[b], conf[b],
                         round(w["outputTokens"] / nh[b], 1) if nh[b] else "",
                         round(w["outputTokens"] / len(ft[b]), 1) if ft[b] else ""])
    print(open(os.path.join(WORK, "decile_series.csv")).read())

    with open(os.path.join(WORK, "decile_facts.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["token", "time", "clock", "decile", "session", "label", "context"])
        for tok, (t, b, s, lab, win) in sorted(seen_fact.items(), key=lambda kv: kv[1][0]):
            cw.writerow([tok, t, clock(t), b + 1, s, lab, win])


if __name__ == "__main__":
    main()
