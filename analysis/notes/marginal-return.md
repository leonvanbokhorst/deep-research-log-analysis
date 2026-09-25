# Marginal epistemic return in a completed multi-agent research run

**Question.** As the run proceeded, did it keep producing new knowledge, or did it
start producing more confidence? Reconstruct the temporal trajectory of substantive
findings, identify what was known early versus what arrived late, and judge whether
the marginal epistemic return rose, held or decayed.

**Corpus.** Root session `session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357` plus 152
subagent sessions (269 MB, 10,037 model steps, 1,286,531,354 total tokens). Read-only.
All timestamps below are corpus event time in **UTC**; the run took place in a UTC+2
environment, so add two hours for the local clock used in the project's other notes
(e.g. 09:21 UTC = 11:21 local; 09:57 UTC = 11:57 local).

---

## 1. Method

**Phase definition.** Four phases were cut at root-turn boundaries, not at even
wall-clock intervals, because the run contains a 32-minute idle gap (08:45–09:16 UTC)
during which no agent produced any assistant output.

| Phase | Root turns | Clock (UTC) | Steps | Output tokens | Total tokens |
|---|---|---|---|---|---|
| P1 batch-1 build | 1–6 | 08:21:34–09:17:39 | 2,699 | 2,474,653 | 309,051,457 |
| P2 batch-2 build | 7 | 09:17:39–09:32:46 | 5,733 | 5,010,743 | 642,757,582 |
| P3 batch-2 extension | 8–14 | 09:32:46–09:47:43 | 1,368 | 1,595,556 | 277,139,964 |
| P4 finalisation | 15–18 | 09:47:43–09:57:16 | 237 | 227,905 | 57,582,351 |

**Decile definition.** Model work is ordered by event time and split into ten bins of
~1,004 steps, reproducing `analysis/tables/discovery_by_work.csv`. Decile 3 is wide
in wall-clock terms (08:30:36–09:20:08) because it contains the idle gap.

**Finding timeline construction.**

1. A single streaming pass over main + subagent JSONL (`analysis/tools/timeline.py`)
   extracted every `deliverables/presented`, every `agent/inbox/spliced` inserted
   message (633), every write/edit tool call (1,402), and every `assistant/message`
   for all 153 sessions (10,037 steps, 35 MB of text).
2. Assistant text includes tool-call *arguments*, i.e. the full text of every file an
   agent wrote. Searching this stream therefore covers both what agents said and what
   they committed to the shared workspace.
3. 43 report-critical findings were defined from the final report's §1 bottom line, §5,
   §7.5, §8 and §12.1–12.3 (from a 44-probe set), each with a distinctive regex probe
   (`analysis/tools/probes.py`, probe set `analysis/work/probes2.json`). For each
   probe the earliest timestamp in the whole corpus was taken.
4. Probes whose first hit was a *root planning outline* or a *task prompt* rather than
   retrieved evidence were manually overridden to the first evidence-bearing
   appearance (`OVERRIDE` in `analysis/tools/findings_inventory.py`).
5. Novelty series were computed per phase and per decile by
   `analysis/tools/marginal.py` and `analysis/tools/deciles.py`.

**New-source definition.** A "new host" is the first appearance of a non-search-proxy
host in `analysis/data/targets.csv`. Search proxies (9 hosts, incl. `news.google.com`)
are excluded so the series measures primary-source discovery, not search-engine use.

---

## 2. Findings per phase and per decile

Counts of the 43 report-critical findings by first evidence-bearing appearance.

**Per phase** (`analysis/work/findings_by_decile.csv`, `findings_inventory.csv`):

| Phase | New primary source | New factual claim | New conceptual distinction | Negative finding | Correction | Open question | Total |
|---|---|---|---|---|---|---|---|
| P1 batch-1 build | 0 | 5 | 0 | 2 | 0 | 0 | **7** |
| P2 batch-2 build | 0 | 22 | 5 | 2 | 2 | 0 | **31** |
| P3 batch-2 extension | 2 | 0 | 0 | 2 | 1 | 0 | **5** |
| P4 finalisation | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Per decile of model work:**

| Decile | % work | Clock (UTC) | NPS | NFC | NCD | NEG | COR | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | 10% | 08:21:37–08:26:39 | 0 | 4 | 0 | 0 | 0 | 4 |
| 2 | 20% | 08:26:39–08:30:36 | 0 | 0 | 0 | 2 | 0 | 2 |
| 3 | 30% | 08:30:36–09:20:08 | 0 | 7 | 1 | 0 | 0 | 8 |
| 4 | 40% | 09:20:08–09:21:40 | 0 | 3 | 1 | 1 | 1 | 6 |
| 5 | 50% | 09:21:40–09:23:52 | 0 | 4 | 0 | 0 | 0 | 4 |
| 6 | 60% | 09:23:52–09:26:01 | 0 | 5 | 2 | 0 | 0 | 7 |
| 7 | 70% | 09:26:01–09:28:18 | 0 | 2 | 1 | 1 | 1 | 5 |
| 8 | 80% | 09:28:18–09:31:10 | 0 | 1 | 0 | 0 | 0 | 1 |
| 9 | 90% | 09:31:11–09:36:46 | 0 | 1 | 0 | 1 | 0 | 2 |
| 10 | 100% | 09:36:46–09:57:16 | 2 | 0 | 0 | 1 | 1 | 4 |

**OBSERVATION.** Decile 3's eight findings are concentrated at its very end: seven of
them fall in 09:17:57–09:20:06, the first ~2.5 minutes of batch 2, crammed into the tail
of a bin that is wide only because it absorbs the 32-minute idle gap. An earlier probe
pass had also matched three *root planning-outline* mentions at 09:17:57 (`havana`,
`boston_2013`, the Starbird/CIB line); these were judged to be model-prior mentions
rather than retrieved evidence and were excluded by the evidence-bearing overrides in
`findings_inventory.py`. What remains counted in decile 3 is genuine evidence.

**OBSERVATION.** No new factual claim, no new conceptual distinction and no first-read
primary source enters the report-critical inventory during P4 (turns 15–18). P4's 237
steps and 227,905 output tokens went to editing, reconciling and freezing documents.

**DERIVED RESULT.** Findings per million output tokens by decile:
6.2, 2.1, 7.1, 9.1, 5.4, 7.8, 5.3, 0.9, 1.7, 3.6. The rate is stable at 5–9 through
deciles 1 and 4–7, then collapses by roughly 5x in deciles 8–10.

---

## 3. New sources versus output over time

**Per decile** (`analysis/work/decile_series.csv`). New hosts reproduce the established
series (420, 145, 95, 244, 210, 199, 107, 106, 48, 66 vs the project's
428, 145, 95, 244, 210, 199, 107, 106, 48, 66 — decile 1 differs only by proxy
filtering).

| Decile | Output tokens | New hosts | New URLs | Output tok / new host | External URLs per 10k text chars |
|---|---|---|---|---|---|
| 1 | 645,297 | 420 | 1,221 | 1,536 | 16.7 |
| 2 | 940,069 | 145 | 1,005 | 6,483 | 13.5 |
| 3 | 1,126,393 | 95 | 367 | 11,857 | 10.8 |
| 4 | 662,032 | 244 | 1,346 | 2,713 | 15.4 |
| 5 | 745,431 | 210 | 1,242 | 3,550 | 15.3 |
| 6 | 892,133 | 199 | 1,161 | 4,483 | 13.4 |
| 7 | 941,380 | 107 | 913 | 8,798 | 11.2 |
| 8 | 1,075,144 | 106 | 748 | 10,143 | 9.5 |
| 9 | 1,180,154 | 48 | 433 | 24,587 | 8.7 |
| 10 | 1,100,824 | 66 | 331 | 16,679 | 9.9 |

**DERIVED RESULT.** The cost of one new primary source rises by roughly 16x from the
best decile (1,536 output tokens/host in decile 1) to the worst (24,587 in decile 9).
Output tokens per decile are essentially flat-to-rising (0.65M → 1.1M) while new hosts
fall 6x. This is the cleanest diminishing-returns signal in the corpus.

**DERIVED RESULT.** External-URL mention density per 10,000 assistant-text characters
falls from 16.7 (decile 1) to 8.7–9.9 (deciles 9–10) — the run progressively stopped
touching the open web and started working its own material.

**Per phase** (`analysis/work/marginal_by_phase.csv`): P1 593 new hosts / 2.47M output
tokens; P2 954 / 5.01M; P3 77 / 1.60M; P4 16 / 0.23M. P2 alone (15 minutes of wall
clock) produced 58% of all new hosts and 54% of all output tokens.

**Counter-series — substantive numeric facts.** A cleaned proxy for new quantitative
claims (comma-grouped numbers, decimal percentages, effect sizes, with
self-referential word/byte-count windows filtered out) does **not** decay in the same
way: 36, 63, 57, 69, 116, 128, 167, 142, 150, 159 per decile, i.e. output tokens per
new numeric fact *falls* from ~18k to ~6–8k. **INTERPRETATION:** this divergence is
real but should not be over-read. Batch 2 (agentic threat amplification) is a far more
figure-dense literature than batch 1 (autonomy economics) — meta-analyses with
N=86,155, view counts, follower counts — so more numbers enter per unit of work even
as the number of *new hosts* falls. A manual audit of deciles 9–10 shows roughly half
of the "new facts" are genuine external figures (Bavarian intelligence 30.17%/249,481
clicks; 27,227 respondents; 1,002,627 posts; 146,681 mean followers) and roughly half
are self-referential document arithmetic that escaped the filter. The source-novelty
series is the trustworthy one; the fact series is directional only.

---

## 4. Early versus late: the report-critical findings

Complete inventory in `analysis/work/findings_inventory.csv`. Selected items with the
session that first asserted them:

| Finding (report anchor) | First evidence (UTC) | Decile | Class | First asserting session |
|---|---|---|---|---|
| Gatwick 2018: 115 "credible" sightings | 08:24:16 | 1 | NFC | d2 `ac2e73e0` Airport drone disruption |
| New Jersey 2024: 5,000+ tips | 08:25:37 | 1 | NFC | d1 `99dae34e` Middle East conflict autonomy |
| Gatwick 2018: 33-hour closure | 08:25:53 | 1 | NFC | d1 `214d85c6` Criminal terrorist misuse |
| Copenhagen 2025: 500+ reports | 08:26:37 | 1 | NFC | d2 `ac2e73e0` Airport drone disruption |
| **Central negative finding** (§5.1d) | 08:27:03 | 2 | NEG | d2 `cbd79d49` Drone assassination attempts |
| COM(2026) 81: zero disinformation terms | 08:27:26 | 2 | NEG | d1 `c2e2b954` NATO/EU institutional assessments |
| Vilnius 2026: birds, 38-minute closure | 08:30:57 | 3 | NFC | d1 `214d85c6` Criminal terrorist misuse |
| Iran/China used hundreds of AI agents (§5.2) | 09:19:58 | 3 | NFC | root turn 7 (relaying NYT reporting) |
| Iranian network ~80,000 followers H1 2026 | 09:19:58 | 3 | NFC | root turn 7 |
| EEAS AI-related cases 41→147 | 09:20:06 | 3 | NFC | d1 `b61859d5` Computational propaganda |
| **"The amplifier is not the agent"** (§9) | 09:20:15 | 4 | NCD | root turn 7 outline, written up 09:25:12 |
| 45–54% who accepted a warning still judged guilt | 09:24:57 | 6 | NFC | d3 `53ed1b24` AI deepfakes |
| EEAS 540 FIMI incidents, 27% AI TTPs | 09:23:00 | 5 | NFC | d1 `b61859d5` Computational propaganda |
| **Galați 116,014 coordinated posts** (§5.1d) | 09:24:01 | 6 | NFC | d3 `f38af81e` Influence-op drone amplification |
| 524:1 cost asymmetry (§12.2) | 09:23:59 | 6 | NFC | d1 `f54b15a3` Agentic AI capability |
| Six conditions for second-order risk (§12.3) | 09:27:32 | 7 | NCD | root turn 7 |
| EEAS names PL/RO/LT/EE, not DK/NO | 09:28:15 | 7 | NEG | d3 `f38af81e` Influence-op drone amplification |
| ~76% of accounts labelled "bots" are human | 09:28:18 | 7 | NFC | d3 `da686808` cross-platform coordination |
| OpenAI: 150,000 views vs 57 for one prompt | 09:30:29 | 8 | NFC | d3 `1ece4a27` LLM-driven IO 2024–26 |
| **55.5% pooled synthetic-media detection** | 09:31:11 | 9 | NFC | d3 `fc1be9de` Detection and belief studies |
| **OpenAI: no meaningful engagement increase** | 09:34:04 | 9 | NEG | d2 `f73d55cf` AI lab and platform threat reports |
| Two figures withdrawn or bounded (correction) | 09:37:26 | 10 | COR | root turn 12 |
| **Gallwitz & Kreil 2022 (arXiv 2207.11474)** | 09:38:08 | 10 | NPS | d3 `d07fdde4` CIB and bot-detection critiques |
| **USC arXiv:2510.25003, simulation-only** | 09:42:24 | 10 | NEG | d3 `1ece4a27` LLM-driven IO 2024–26 |
| **Starbird, Arif & Wilson 2019 CIB critique** | 09:45:54 | 10 | NPS | d3 `d07fdde4` CIB and bot-detection critiques |

### Which important conclusions were already available in the first 10% of model work?

**DERIVED RESULT.** Four report-critical findings (Gatwick 115 and 33-hour closure,
New Jersey 5,000+ tips, Copenhagen 500+ reports) had evidence in the corpus by
08:26:39, the end of decile 1. All four are *case facts* — incidents, numbers, closures.

**OBSERVATION.** Their *interpretation* was not available then. The New Jersey
conclusion the report actually leads with — the joint DoD/DHS/FAA/FBI statement of
16 December 2024, "5,000+ reports, **nothing anomalous**", and the later framing that
the input was "essentially nothing anomalous — no adversary action was established" —
first appears at **09:19:55** (d1 `f5d926fb`, Drone sighting ambiguity cases) and
**09:20:52** (root), i.e. in batch 2, ~2.3 hours of run time and roughly 35% of model
work later.

**OBSERVATION.** The central negative finding — the *absence* of a documented
AI-enabled amplification of a drone wave — was reached at **08:27:03** by d2
`cbd79d49` (Drone assassination attempts), whose report ends with
*"India/Pakistan/Somalia/Ethiopia: no credible documented case found → gap"*.
The report's version of it is a *convergence* claim — "reached independently twice, from
different directions" — and the EU-level material it uses to strengthen that claim
(EEAS 540 incidents / 27% AI TTPs / 41→147 cases, and the EEAS geography finding) did
not enter the corpus until 09:23:00–09:28:15 (deciles 5–7), with the Galați exception at
09:24:01.

### Which important findings arrived surprisingly late (last 25%)?

**DERIVED RESULT.** Seven of 43 report-critical findings (16%) first appear in deciles
8–10 (09:28:18–09:57:16): OpenAI 150k-vs-57 miss, 55.5% detection, OpenAI engagement
null, the two-figure withdrawal, Gallwitz & Kreil, USC simulation-only, and the
Starbird CIB critique.

**OBSERVATION.** Three of these are load-bearing for the final report:

- **USC / arXiv:2510.25003.** First fetched at **09:42:24** by d3 `1ece4a27`
  (LLM-driven IO 2024–26): *"USC paper: arXiv 2510.25003, ACM DL
  10.1145/3774904.3792580."* The phrase "demonstrated only in simulation / never
  observed in the wild" first appears anywhere in the corpus at **09:49:32**
  (d2 `edb0f8d3`). The root writes it into the report at **09:57:04** as
  *"THE SINGLE MOST IMPORTANT CONSTRAINT FINDING (new section 7.5)"*. The report's
  decisive constraint therefore had a working life of **15 minutes**.
- **Starbird, Arif & Wilson (2019)**, the canonical CIB critique, was first read at
  **09:45:54** by d3 `d07fdde4`: *"JACKPOT. Section 5.2 of Starbird, Arif & Wilson
  (2019) is titled 'The Trouble with Coordinated Inauthentic Behavior'."* This is
  §7.5's governance argument and §12.2's closing move.
- **55.5% pooled detection (56 papers, 86,155 participants)** first appears at
  **09:31:11** (d3 `fc1be9de`) and is used to replace a figure the report had itself
  flagged as unverifiable at 09:27:15.

### Which findings were available early but only became salient/structurally important later?

**OBSERVATION — New Jersey.** The 5,000+ figure is decile-1 evidence (08:25:37); the
adversary-free conclusion is 09:19:55; it becomes the report's opening exemplar only
when the root writes *"the input was essentially nothing anomalous … and the output was
5,000+ reports, an interagency response, and counter-UAS legislation"* at 09:20:52.

**OBSERVATION — COM(2026) 81.** Retrieved 08:27:26 by a batch-1 branch
(`c2e2b954`, NATO/EU institutional threat assessments) for an autonomy-economics
report. It becomes §5.1d's third sharper finding — "the institution closest to the
problem does not assess it as an information operation" — only after being carried into
the amplification report in batch 2.

**OBSERVATION — the institutional/reflexive insight.** The root's turn-1 brainstorm at
08:22:08 already lists "Second-order consequences"; but the structural claim itself,
*"The amplifier is not the agent: institutions as the true amplification stage"*, is
first written at **09:20:15** (root turn 7 outline) and drafted at 09:25:12 — after,
not before, the batch-2 evidence arrived. It is a *late synthesis of early material*.

**OBSERVATION — Galați.** The town appears in batch 1 (08:25:53) as a *real* drone
strike that injured a child. The coordinated amplification campaign around it —
"7 consecutive days, 28–105 accounts/day, 3,400–6,800 posts/day, **116,014 posts**" —
first appears at **09:24:01** (d3 `f38af81e`, Influence-op drone amplification) and is
folded into §5.1d at 09:40:06–09:41:27. Same event, genuinely new fact, 59 minutes
later.

---

## 5. Did late work produce anything decisive? (Testing the diminishing-returns story)

**OBSERVATION — decisive late arrivals exist.** The report says of the USC result:
*"This matters more than any other negative finding in this report, because it removes
the one element that would make the hypothesis genuinely novel."* That finding, plus
the Starbird CIB critique and the peer-reviewed 55.5% replacement, entered in the last
25% of model work. **The claim "late branches restated earlier material" is false as a
blanket statement.**

**OBSERVATION — the Galați exception was late and is explicitly the strongest case in
the record.** §5.1d calls it *"the strongest documented case in the entire record"*.
It was found by a depth-3 branch at 09:24:01 (decile 6, ~60% of model work) — late
middle, not first wave.

**DERIVED RESULT — but the late findings are constrained in kind.** In P3 (turns 8–14)
the inventory records 2 new primary sources, 2 negative findings and 1 correction — and
**zero** new factual claims and **zero** new conceptual distinctions. Every new factual
claim in the report-critical inventory is in P1 or P2. Late work *narrowed and corrected*
the hypothesis rather than expanding it.

**DERIVED RESULT — the late decisive findings were new sources, not restatements.**
Each of the four last-decile items has a distinct new retrieval behind it:
arXiv `2207.11474` first fetched 09:38:08 (`targets.csv`); `2510.25003` fetched by
`curl` at 09:42:24 (invisible to `targets.csv`); the Starbird full text first read at
09:45:54; and the pooled-detection preprint (`osf.io/cxv4r`, Diel et al.) first fetched
at 09:27:07 with the 55.5% figure extracted at 09:31:11. They were not synthesis citing
synthesis.

**OBSERVATION — the reverse is also true for at least one late finding.** The *two
non-root sessions that read the root's in-progress report* did so at 09:21:29
(d1 `46b82e74`, Health and military scare cases, via `bash`) and 09:22:42–43
(d2 `31ca772b`, Personas and influence-for-hire, via `bash` and `read`). Both sessions
subsequently produced material that entered the same report. This is a genuine
synthesis-cites-synthesis pathway inside the run, and it operates exactly where the
late-tail findings cluster (deciles 4–6).

---

## 6. "Confidence without knowledge" signatures

**DERIVED RESULT — output per new source rises.** Output tokens per new host:
1,536 → 6,483 → 11,857 → 2,713 → 3,550 → 4,483 → 8,798 → 10,143 → 24,587 → 16,679.
After the batch-2 refill (decile 4) the ratio rises monotonically. The run increasingly
spent output on material it already had.

**DERIVED RESULT — the marginal output becomes document management.** Share of
assistant messages containing explicit word-count language ("N words", "word count",
"wc -w") and their share of assistant-text characters:

| Decile | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| % messages | 7.8 | 21.2 | 34.1 | 3.6 | 4.3 | 11.2 | 17.3 | 20.9 | 25.1 | **39.5** |
| % characters | 28.1 | 44.4 | 60.2 | 16.7 | 14.2 | 34.7 | 33.1 | 37.5 | 46.7 | **50.5** |

**OBSERVATION.** In the final decile more than half of all assistant-text characters
are about the length of documents. Representative example (d1 `dc0b75f5`, Defensive
practice and non-amplification): *"3,023. Let me trim ~30 words to land ~2,993.
Cuts: - S4 OSINT clause I just added is 34 words."* — repeated across dozens of steps.
This is output that cannot, by construction, add knowledge.

**DERIVED RESULT — external-URL density halves** from 16.7 to 8.7–9.9 per 10k chars
while distinct internal-artefact references per 10k chars rise again late (1.64 in
decile 5 → 2.52 in decile 10). Relative internal cross-citation therefore grows.

**OBSERVATION — concepts arrived before their evidence.** The root's turn-7 brief
(09:19:30) names *"the 'liar's dividend' effect (real evidence dismissed as fake)"*
before any source for it had been retrieved; the supporting figure (45–54% still
judging guilt) arrives at 09:24:57. Likewise the turn-7 outline names Havana, Boston
2013 and the Starbird/CBI line at 09:17:57; their sources arrive at 09:45:54 and later.
The parent pre-specified several conclusions and delegated confirmation of them.

**OBSERVATION — confidence language per output token rises late.** Negative-finding
markers per million output tokens: 105 (P1), 127 (P2), 219 (P3), 364 (P4); correction
markers: 171, 228, 422, 447; confidence markers: 93, 99, 211, 189. Late text is more
assertoric *and* more hedging at the same time, which is what a synthesis-and-adjudication
phase looks like.

**OBSERVATION — but the evidence base did grow where it mattered.** The two withdrawn
figures were replaced by a peer-reviewed pooled figure (55.5%, 56 papers, 86,155
participants) newly retrieved from the OSF preprint at 09:27:07 and extracted at
09:31:11, not re-asserted; the OpenAI null was first asserted at 09:34:04 by session
`f73d55cf` (AI lab and platform threat reports), whose stated source is OpenAI's own
threat reporting. The confidence escalation in the final report is anchored to *new*
primary sources in the cases the report flags as decisive.

**What cannot be determined.** Whether any individual agent's confidence exceeded its
evidence; whether the root's private reasoning discounted a source it publicly cited;
whether a claim asserted without a corpus retrieval came from model prior knowledge or
from a retrieval whose text the extractor missed (bash-`curl` fetches are not in
`targets.csv` — the USC paper is a confirmed instance). All marker series above are
vocabulary proxies, not calibrated belief measurements.

---

## 7. Verdict

**DERIVED RESULT.** The trajectory is neither monotone decay nor flat. It is a
two-burst structure with a thin, high-value tail:

- **Front-loaded for case facts.** 4 of 43 findings in the first 10% of model work; the
  first 20% contains the central negative finding and the COM(2026) 81 absence.
- **Peak in the middle.** Deciles 4–7 (40–70% of work, 09:20–09:28) carry 22 of 43
  findings — 51% of the report's evidence base — after batch 2's eight branches opened
  a new literature.
- **Sharply decayed after 70%.** Deciles 8–10 carry 7 of 43 (16%) while consuming 33%
  of output tokens; new hosts fall from 199 to 66.
- **But the tail is disproportionately decisive.** The report's self-declared single
  most important constraint finding (USC, simulation-only), its canonical governance
  critique (Starbird et al.), its peer-reviewed replacement for a withdrawn figure
  (55.5%), and the OpenAI null quote all arrive in the last 25%.

**INTERPRETATION.** The marginal epistemic return **rose, then decayed, but did not
reach zero before the run stopped.** Judged by volume and by source-novelty per unit of
work, the run was well past its productive peak by decile 8: after ~70% of model work
it was mostly re-arranging, hedging and correcting what it already had, and by the last
decile half of its output was word-count bookkeeping. Judged by *decisiveness*, the
final 25% still paid for itself — the report explicitly says it could not have been
written without the USC constraint. The honest summary is that the run's marginal
return decayed in **rate** but retained a **small, sparse, high-variance tail**; a
stopping rule based on new-source rate alone would have halted the run roughly 15
minutes before the finding the report calls decisive.

The "more confidence rather than more knowledge" framing is half right. Late output was
overwhelmingly confidence-shaped (restatement, hedging, document arithmetic) — but the
late *findings* that did arrive were almost all **negative or corrective** (2 NEG + 1
COR + 2 NPS in P3; no NFC, no NCD). The run did not keep discovering new facts; it kept
discovering reasons to constrain the hypothesis, and it did that well until the end.

---

## 8. Limitations

1. **The logs cannot show what an agent believed**, only what it wrote. "First
   appearance in assistant text" is a proxy for "first known"; the turn-1 brainstorm at
   08:22:08 shows agents naming New Jersey, Gatwick and Copenhagen from model priors
   before any retrieval.
2. **Retrieval coverage is incomplete.** `targets.csv` is built from `web_fetch`
   targets; sources pulled with `bash` + `curl`/`wget` or read from `tools/news.sh`
   are invisible to it. The USC paper (arXiv:2510.25003) is a confirmed case: it is
   absent from `targets.csv` although the run demonstrably fetched it at 09:42:24.
   New-host counts are therefore lower bounds.
3. **The finding inventory is a curated sample of 43 items**, chosen because the final
   report depends on them. Findings the report discarded, or that never made it past a
   strand brief, are not counted, so the counts measure *report-relevant* novelty, not
   total novelty.
4. **Regex probes have both false positives and false negatives.** Four confirmed false
   positives were caught and overridden; others may remain. A finding phrased without a
   distinctive number, name or document code will be missed entirely.
5. **The numeric-fact proxy is contaminated** by self-referential word/byte counts.
   Roughly half of decile 9–10 "new facts" survive auditing; the series is directional,
   not a measurement.
6. **Decile 3 is wide** (08:30:36–09:20:08) because it absorbs the 32-minute idle gap;
   per-decile rates for deciles 2–4 are correspondingly distorted, which is why phase
   tables are reported alongside them.
7. **Importance weighting is the analyst's**, derived from the report's own emphases
   (§1, §5, §7.5, §8, §12.1–12.3). A different reading of what mattered would move
   individual cells in the early/late tables, though not the two-burst shape.
8. **The logs cannot say whether the run should have stopped earlier.** They contain no
   counterfactual: the late findings arrived, so the marginal value of continuing is
   observed; the marginal value of an earlier stop is not.
9. **The two batches ask different questions** and are reported separately above; the
   phase table is the only place they are aggregated, and P1/P2 are never averaged into
   a single "batch" number.

---

## 9. Artefacts produced by this analysis

| Path | Contents |
|---|---|
| `analysis/tools/timeline.py` | streaming extraction of presented/inbox/write/assistant events |
| `analysis/tools/probes.py` | regex first-hit search over all assistant text |
| `analysis/tools/show_hits.py` | exact-context occurrence viewer |
| `analysis/tools/marginal.py` | per-phase novelty vs output |
| `analysis/tools/deciles.py` | per-decile novelty vs output |
| `analysis/tools/findings_inventory.py` | classified finding inventory and tables |
| `analysis/work/marginal_by_phase.csv` | phase metrics |
| `analysis/work/decile_series.csv` | decile metrics |
| `analysis/work/findings_inventory.csv` | 43 report-critical findings with first evidence times |
| `analysis/work/findings_by_decile.csv` | findings per decile by class |
| `analysis/work/fact_token_firsts.csv`, `decile_facts.csv` | numeric-fact first appearances |
| `analysis/work/host_firsts.csv`, `artefact_firsts.csv`, `marker_firsts.csv` | supporting first-appearance series |
| `analysis/work/probe_first_hits2.json`, `probes2.json` | probe definitions and results |
