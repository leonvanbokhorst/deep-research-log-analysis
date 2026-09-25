"""Classified finding inventory -> per-phase and per-decile tables.

The inventory is the ~45 substantive findings that the final report's sections
1, 5, 7.5, 8 and 12.1-12.3 depend on. First-appearance times come from
probe_first_hits2.json (first time the finding's evidence appears in any
session's assistant text, including written file content).

Classes:
  NPS new primary source retrieved/registered
  NFC new factual claim (number, case, document)
  NCD new conceptual distinction
  NEG negative finding (absence of evidence / failed verification)
  COR correction or withdrawal of an earlier figure
  UQ  unanswered question / identified gap
"""

from __future__ import annotations

import csv
import json
import os
import sys
import datetime
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

WORK = os.path.join(C.WORKSPACE, "analysis", "work")

# id -> (class, phase, short description)
INV = {
    "gatwick_115": ("NFC", "P1", "Gatwick 2018: 115 'credible' sightings"),
    "gatwick_33h": ("NFC", "P1", "Gatwick 2018: 33-hour closure"),
    "nj_5000reports": ("NFC", "P1", "New Jersey 2024: 5,000+ tips"),
    "copenhagen_500": ("NFC", "P1", "Copenhagen 2025: 500+ reports"),
    "vilnius_38min": ("NFC", "P1", "Vilnius 2026: birds, 38-minute closure"),
    "central_negative": ("NEG", "P1", "no documented AI amplification of a drone wave"),
    "com2026_zero": ("NEG", "P1", "COM(2026) 81 has zero disinformation terms"),
    "nj_nothing_anomalous": ("NFC", "P2", "NJ: no national security / public safety risk"),
    "iran_china_agents": ("NFC", "P2", "Iran/China used hundreds of AI agents"),
    "followers_80000": ("NFC", "P2", "Iranian network ~80,000 followers H1 2026"),
    "reach_billion": ("NFC", "P2", "coordinated networks >1bn views in a month"),
    "eeas_147": ("NFC", "P2", "EEAS AI-related cases 41 (2024) -> 147 (2025)"),
    "eeas_540": ("NFC", "P2", "EEAS 540 FIMI incidents 2025, 27% AI TTPs"),
    "eeas_noname": ("NEG", "P2", "EEAS names PL/RO/LT/EE, not DK/NO"),
    "galati_116014": ("NFC", "P2", "Galati 2026: 116,014 coordinated posts in 7 days"),
    "indian_chronicles": ("NFC", "P2", "Indian Chronicles: 750+ fake outlets"),
    "synthetic_3749": ("NFC", "P2", "NewsGuard: 3,749 AI content-farm sites"),
    "liars_dividend": ("NCD", "P2", "the liar's dividend"),
    "liars_dividend_pct": ("NFC", "P2", "45-54% who accepted warning still judged guilt"),
    "schiff": ("NFC", "P2", "Schiff APSR 2024: deepfake true-evidence experiment"),
    "detect_86155": ("NFC", "P2", "pooled detection N=86,155"),
    "detect_555": ("NFC", "P2", "55.5% pooled synthetic-media detection"),
    "dawel_40_80": ("NFC", "P2", "Dawel PNAS 2026: 40% -> 80% with training"),
    "botometer_085": ("NFC", "P2", "Botometer AUC 0.85, not 0.94"),
    "botometer_76": ("NFC", "P2", "~76% of accounts labelled bots are human"),
    "gallwitz": ("NPS", "P3", "Gallwitz & Kreil 2022 (arXiv 2207.11474)"),
    "cib_starbird": ("NPS", "P3", "Starbird, Arif & Wilson 2019 CIB critique (source)"),
    "openai_150k": ("NFC", "P2", "OpenAI: 150,000 views vs 57 for one prompt"),
    "openai_quote": ("NEG", "P3", "OpenAI: no meaningful engagement increase"),
    "usc_sim": ("NEG", "P3", "USC 2510.25003: agent coordination simulation-only"),
    "cost_524": ("NFC", "P2", "524:1 generation vs distribution asymmetry"),
    "repetition_not_number": ("NFC", "P2", "2012: repetition, not number of sources"),
    "persuasion_005": ("NFC", "P2", "measured persuasion 0.05-0.06 SD"),
    "zero49": ("NEG", "P2", "zero average persuasion across 49 experiments"),
    "correction_lag": ("NFC", "P2", "62.9h note lag vs 6.25h post half-life"),
    "six_conditions": ("NCD", "P2", "six conditions for second-order risk"),
    "temporal_decoupling": ("NCD", "P2", "temporal-decoupling test"),
    "institution_amplifier": ("NCD", "P2", "the amplifier is the institution"),
    "sustained_ambiguity": ("NCD", "P2", "objective is sustained ambiguity"),
    "borris_43rounds": ("NFC", "P2", "Borris: 43 rounds fired at an aircraft"),
    "twitter25_withdrawn": ("COR", "P2", "withdraw: 25% of Twitter activity is bots"),
    "indistinguishable_withdrawn": ("COR", "P2", "withdraw: 'indistinguishable in more than half'"),
    "two_withdrawn": ("COR", "P3", "two early figures withdrawn or bounded"),

}

# First *evidence-bearing* appearance overrides (probe hit was a task prompt,
# a root planning outline, or model-prior mention rather than retrieved evidence).
OVERRIDE = {
    "cib_starbird": ("09:45:54", "d3 d07fdde4 'CIB and bot-detection critiques' reads Starbird et al. full text"),
    "vilnius_38min": ("08:30:57", "d3 e289f909 'Spain, EU airports, drone wall' confirms birds"),
    "liars_dividend": ("09:19:30", "term injected in the root's turn-7 brief; evidence = Schiff 09:21:14"),
}

DEC_BOUNDS = [(0, 1003), (1003, 2007), (2007, 3011), (3011, 4014), (4014, 5018),
              (5018, 6022), (6022, 7025), (7025, 8029), (8029, 9033), (9033, 10038)]


def main():
    hits = json.load(open(os.path.join(WORK, "probe_first_hits2.json")))["first"]
    rows = []
    for k, (klass, ph, desc) in INV.items():
        h = hits.get(k)
        if not h:
            print("MISSING PROBE HIT:", k)
            continue
        if k in OVERRIDE:
            h = dict(h)
            hh, mm, ss = OVERRIDE[k][0].split(":")
            # rebuild epoch from the same UTC day
            import datetime as _dt
            base = _dt.datetime(2026, 9, 25, int(hh), int(mm), int(ss),
                                tzinfo=_dt.timezone.utc)
            h["time"] = int(base.timestamp() * 1000)
            h["clock"] = OVERRIDE[k][0]
            if k == "cib_starbird":
                h["session"] = "d07fdde4-91a3-4617-9341-d7100c77ab33"
                h["depth"] = 3
                h["label"] = "CIB and bot-detection critiques"
        rows.append({"id": k, "class": klass, "phase": ph, "desc": desc,
                     "time": h["time"], "clock": h["clock"],
                     "depth": h["depth"], "session": h["session"],
                     "label": h.get("label") or ""})
    rows.sort(key=lambda r: r["time"])
    with open(os.path.join(WORK, "findings_inventory.csv"), "w", newline="") as f:
        cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        cw.writeheader(); cw.writerows(rows)

    phases = ["P1", "P2", "P3", "P4"]
    classes = ["NPS", "NFC", "NCD", "NEG", "COR", "UQ"]
    print("\nfindings by phase x class")
    print(f"{'phase':<6}" + "".join(f"{c:>6}" for c in classes) + f"{'total':>7}")
    tab = defaultdict(Counter)
    for r in rows:
        tab[r["phase"]][r["class"]] += 1
    for p in phases:
        print(f"{p:<6}" + "".join(f"{tab[p][c]:>6}" for c in classes) + f"{sum(tab[p].values()):>7}")

    # decile of each finding (by time against decile extents from deciles.py)
    ext = [("08:21:37", "08:26:39"), ("08:26:39", "08:30:36"), ("08:30:36", "09:20:08"),
           ("09:20:08", "09:21:40"), ("09:21:40", "09:23:52"), ("09:23:52", "09:26:01"),
           ("09:26:01", "09:28:18"), ("09:28:18", "09:31:10"), ("09:31:11", "09:36:46"),
           ("09:36:46", "09:57:16")]

    def sec(s):
        h, m, ss = map(int, s.split(":")); return h * 3600 + m * 60 + ss
    bounds = [(sec(a), sec(b)) for a, b in ext]

    def decile(t):
        d = datetime.datetime.utcfromtimestamp(t / 1000)
        x = d.hour * 3600 + d.minute * 60 + d.second
        for i, (a, b) in enumerate(bounds):
            if a <= x <= b:
                return i + 1
        return 10 if x > bounds[-1][0] else 1

    dt = Counter(); dcl = defaultdict(Counter)
    for r in rows:
        d = decile(r["time"]); r["decile"] = d
        dt[d] += 1; dcl[d][r["class"]] += 1
    print("\nfindings first appearing, by decile of model work")
    print(f"{'dec':>4}" + "".join(f"{c:>6}" for c in classes) + f"{'total':>7}")
    for d in range(1, 11):
        print(f"{d:>4}" + "".join(f"{dcl[d][c]:>6}" for c in classes) + f"{dt[d]:>7}")

    with open(os.path.join(WORK, "findings_by_decile.csv"), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(["decile"] + classes + ["total"])
        for d in range(1, 11):
            cw.writerow([d] + [dcl[d][c] for c in classes] + [dt[d]])

    print("\nINVENTORY (sorted by time)")
    for r in rows:
        print(f"  d{r['decile']:<2} [{r['clock']}] {r['class']} {r['phase']} {r['desc']}"
              f"   <{r['label'][:30]}>")


if __name__ == "__main__":
    main()
