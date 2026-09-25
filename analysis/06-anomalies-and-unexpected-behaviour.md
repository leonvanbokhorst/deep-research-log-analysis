# Anomalies and unexpected structure

Findings that were not anticipated by the analysis brief, or that contradict the
expectations of the run's own final report. Ordered by how much they change the
interpretation. Every item is labelled **OBSERVATION** / **DERIVED RESULT** /
**INTERPRETATION**.

---

## A1 — Recursion was terminated by a hard depth cap, not by diminishing returns

**OBSERVATION.** 40 of the 91 depth-3 sessions attempted to spawn children. All 99
attempts returned the identical error:

```
Error: subagent depth 4 exceeds maxDepth 3
```

Every attempt included a fully written prompt (median ≈3,600 characters). Examples
of delegations that were written and rejected: "ASN nuclear drone overflights",
"Platform IRA disclosures", "Google TAG influence op counts", "LLM API token
pricing 2026", "Vulnerability of tip yield and false-positive research",
"Cyber amplification analogies".

**DERIVED RESULT.** The tree's shape is therefore **censored**, not natural:
`depth 0 = 1, depth 1 = 16, depth 2 = 45, depth 3 = 91`. The 91 leaves are not
sessions that concluded; 44% of them (`40/91`) were still actively trying to
delegate when they hit the wall.

**INTERPRETATION.** Any statement of the form "the process stopped when it stopped
producing" is false for this run. The stopping condition was **infrastructural**.
This also means the observed depth-3 productivity figures (§A2) describe agents
that were *cut off*, not agents that had run to completion — an important
qualification for any argument about optimal depth.

---

## A2 — Productivity collapses with depth, but the deepest agents produced the decisive corrections

**DERIVED RESULT.** Tokens spent in sessions whose artefacts were subsequently read
by another session (`tables/agent_productivity.csv`):

| depth | sessions | tokens | sessions with consumed output | tokens in those | share |
|---|---|---|---|---|---|
| 0 | 1 | 130,220,004 | 1 | 130,220,004 | 100.0% |
| 1 | 16 | 249,647,052 | 14 | 238,604,968 | 95.6% |
| 2 | 45 | 474,060,261 | 22 | 268,294,695 | 56.6% |
| 3 | 91 | 432,604,037 | 36 | 194,441,320 | 44.9% |

Measured by **file** inheritance, depth 3 looks wasteful: 55% of its tokens went
to sessions whose files nobody read.

**OBSERVATION — that measure is wrong for this architecture.** The dominant
transfer channel was not files but `send_message`. 374 agent-to-agent messages
carried 1,645,470 characters; **251** of them look like full reports and **148**
exceed 4,000 characters. Against that channel, **152 of 153 sessions produced
output that reached another session** (only one session — 1.7M tokens, 0.1% of the
run — left no observable trace).

**DERIVED RESULT — and the deepest agents were disproportionately decisive.**

- Three of the four largest corrections in the run were detected at **depth 3**,
  by leaves that went to primary literature after the root *and* the depth-1/2
  leads had asserted the opposite (Foster 2012 null on source-count; the Salvi
  author correction; an Internet Archive full-text check that falsified a
  "Liddell Hart" quotation the depth-1 agent had written into its own brief).
- A depth-3 agent ("FRONTEX Eurojust Europol research", 2.4M tokens) pushed
  28,611 characters containing **103 URLs** to its parent — more URLs than any
  depth-1 branch sent.
- A depth-2 agent ("European retractions and influence ops", 17.6M tokens) wrote
  the report's single most valuable evidence file
  (`amplification/findings/drone-cases-amplification-retractions.md`, 30KB,
  `[P]/[J]/[T]/[NV]`-graded, with explicit "could not retrieve" flags).

**INTERPRETATION.** Raw token-to-artefact accounting understates deep agents
because their output is a *message*, not a file. Any cost-benefit judgement of
deep recursion that counts only artefacts will misprice it. But this cuts both
ways: the same architecture that let a leaf falsify the root's claim also let 40
leaves spend 190M tokens re-querying sources the run had already mined (§A6).

---

## A3 — The "six independent evidence streams" were six siblings of one branch

Full trace in [`notes/validation.md`](validation.md) §2. In brief:

**OBSERVATION.** The phrase enters the report at root `seq 2017`, 13 seconds after
a subagent message (`seq 2004`) from depth-1 session `6f182957` ("Concept
genealogy and fit"). That session had exactly six children, all spawned by it,
all briefed by it, writing on rumour theory, active measures, reflexive control,
perception management, self-amplifying attack concepts and computational
propaganda. The subagent's own wording to the root was "all six **agents**
converged independently"; the report's wording is "six independent evidence
streams converged".

**DERIVED RESULT.** Pairwise prompt similarity across those six is low (median
`difflib` ratio 0.216) — the work was genuinely differentiated. But they are one
branch's sub-agents, not the study's "eight parallel research strands", and the
logs contain no test of their independence.

**INTERPRETATION.** A subordinate's hedged claim about its own six helpers was
promoted, in one step and without check, into the report's headline epistemics.
This is the clearest instance in the run of **confidence amplification through
compression**: nothing false was said at any stage, and the resulting claim is
materially stronger than what the evidence supports.

---

## A4 — The decisive constraint was found in the last 20 minutes, and the conclusion was adopted before it was reported

**DERIVED RESULT — first appearance of each decisive marker** (t = start of run):

| marker | first session | depth | t+min | sessions touching it |
|---|---|---|---|---|
| Starbird 44:1 correction ratio | Drone recon over bases | 3 | 0.0 | 26 |
| Diel 55.5% detection pooled | Drone assassination attempts | 2 | 0.4 | 12 |
| "no case found" (central negative) | Drone assassination attempts | 2 | 2.0 | 14 |
| Breakout Scale | Computational propaganda evidence | 1 | 53.9 | 26 |
| Botometer AUC caution | Concept genealogy and fit | 1 | 54.5 | 6 |
| Salvi +81.2% (the erroneous figure) | Agentic AI capability evidence | 1 | 54.6 | 10 |
| Foster 2012 "repetition not sources" | Detection and belief studies | 3 | 59.2 | 4 |
| Salvi +48.7% (the correction) | Research stream C AI persuasion | 3 | 62.1 | 4 |
| **USC arXiv:2510.25003 (simulation-only)** | RAND IO and counter-propaganda | 3 | **76.8** | **5** |
| "plausible, novel, and currently unobserved" | Research computational propaganda CIB | 2 | 84.8 | 3 |

**OBSERVATION.** The report's "single most important constraint finding" —
that autonomous agent-to-agent propaganda coordination has been demonstrated only
in simulation — rests on a paper first touched at **t+76.8 minutes**, by a depth-3
agent, and reached only **5 sessions** in a run of 153. The formulation it
supports ("plausible, novel, and currently unobserved") first appears at
**t+84.8 minutes**, and the report was finalised at ≈t+96.

**INTERPRETATION.** The study's most important negative result was a
**late, thin, single-paper finding** — which is exactly the profile of evidence
that a process optimised for convergence would be expected to under-weight. The
report handles this honestly (it names the paper and its limits), but the phrase
"six independent evidence streams converged" implies a robustness the late,
five-session footprint does not show.

---

## A5 — The primary search tool failed for 86% of the run, and the workaround became shared infrastructure

**OBSERVATION.** `web_search` was invoked 135 times; **116** returned
"unprocessable response body" (85.9%). Agents reported the failure explicitly and
repeatedly to one another ("web_search stayed broken all session"; "web_search is
dead for me too").

**OBSERVATION — the response was to build tools.** Agents wrote ~30 shell scripts
into the shared workspace (`tools/news.sh`, `get.sh`, `ddg.sh`, `web.sh`, `s.sh`,
`bn.sh`, `j.sh`, `wsearch.sh`, `news-nl.sh`, `a3fetch.sh`, `pget.py`, …) and told
each other about them. Retrieval consequently ran through **6,458 shell
invocations** (`curl` 4,381; `tools/news.sh` 1,405; `tools/get.sh` 991;
`pdftotext` 272) and 1,361 `web_fetch` calls. For the six sessions that sent the
most content upward, shell retrieval was the whole method.

**DERIVED RESULT — the workaround created a shared dependency.** In
`data/fileprovenance.csv`, the most "inherited" files in the entire run are not
evidence at all:

| file | sessions that wrote it | read-acts inheriting it from another session |
|---|---|---|
| `tools/news.sh` | 52 | 160 |
| `tools/get.sh` | 51 | 111 |
| `tools/ddg.sh` | 34 | 73 |
| `tools/web.sh` | 31 | 52 |

**INTERPRETATION.** A degraded first-class tool did not reduce the run's
capability so much as **relocate** it into shared, unversioned shell scripts that
every branch then coupled to. Two consequences follow. First, source *discovery*
was channelled through a handful of proxy hosts (`lite.duckduckgo.com` appears in
72 sessions, `web.archive.org` in 65, `en.wikipedia.org` in 60), so the run's
apparent breadth partly reflects one workaround's reach. Second, a single bug in
`news.sh` would have silently biased every branch simultaneously — the coupling
is invisible in the delegation tree, which shows independent agents.

---

## A6 — Source mining exhausted while artefact production stayed flat

**DERIVED RESULT** (`tables/discovery_by_work.csv`, equal counts of model steps,
plus `tables/stopping_signals.csv` for artefacts):

| decile of model work | new hosts | new queries | new artefacts |
|---|---|---|---|
| 10% | 428 | 249 | 51 |
| 20% | 145 | 138 | 69 |
| 30% | 95 | 233 | 28 |
| 40% | 244 | 577 | 23 |
| 50% | 210 | 400 | 17 |
| 60% | 199 | 298 | 45 |
| 70% | 107 | 179 | 32 |
| 80% | 106 | 152 | 44 |
| 90% | 48 | 105 | 43 |
| 100% | 66 | 90 | 38 |

**OBSERVATION.** New-host discovery falls by roughly an order of magnitude and is
at its lowest in the final two deciles. New *artefact* creation, by contrast,
stays roughly flat at 38–45 per decile right to the end.

**DERIVED RESULT — the total corpus is large but the productive core is not.**
The research workspace holds 2,161 files and ≈946 MB of captures. But only
**1,609 distinct evidence hosts** were ever reached, 6,458 shell retrievals
produced a **median result of 941 characters**, and 584 of 1,622 evidence hosts
were targeted by more than one session.

**INTERPRETATION.** The last ~20% of model work was spent writing summaries and
syntheses from a source pool that had stopped growing. That is not automatically
waste — synthesis is where corrections were caught (§A7) — but it is *not*
additional empirical discovery, and a stopping rule keyed on new-host rate would
have fired well before the run ended.

---

## A7 — Correction was concentrated in the root, and its detection depended on relays that nearly did not happen

**OBSERVATION (from the correction forensics).** Of ~20 reconstructed
corrections, the evidence was found at depth 3 in the largest cases and relayed
up over two to three hops. Relay latency dominated: **2m44s** for the Foster null,
**16m02s** for the Salvi correction. Two mechanisms failed:

- A partial warning — "an author correction was issued 3 Sep 2026 whose content I
  could not retrieve; treat the headline figures as provisional" — was sent to the
  root at `09:34:05` and sat **unactioned for 9m19s**; ~3,000 model steps ran in
  the interval.
- The refuting Starbird PDF (correction:claim ratio 44:1) was read at depth 2 at
  `09:23:52` and reached the root at `09:40:22` — **16m44s latent**, while its
  wrong version was already in the report.

**DERIVED RESULT.** Correction throughput was limited not by finding evidence but
by **message travel time and the parent's attention**. In one case a depth-2 agent
read the parent's own in-progress report and reproduced its framing (root
document read at `11:21:29` and `11:22:42` by two non-root sessions), i.e. the
report briefly became a source for the research that was meant to test it. The
exposure was small — **4 read-acts by 2 sessions** out of 132 acts touching that
file — but the direction of the loop is the one that manufactures false
consensus.

**OBSERVATION — and correction was asymmetric.** The report's own tally moves
**six → seven → eight** withdrawn assertions across its final three turns
(`turn 16 step 7`, `turn 17 step 7`, `turn 18 step 9`). The corrections were not
all distinct: the count includes a *source's* correction (Salvi) and a
withholding (the 25% Twitter figure) alongside the study's own withdrawn claims.

**INTERPRETATION.** Recursive delegation did provide a genuine error-detection
mechanism that the root alone would likely have missed — the Foster and Salvi
catches both went to primary literature that no depth-0 or depth-1 agent read.
But it was **slow and lossy**, and it worked only when a parent happened to read
its inbox at the right moment. The run's own closing verification pass was
string-based (`grep` for named banned entities) and therefore could not detect
a withdrawn claim that survived under its own original wording — which is how
at least two corrected claims remained asserted in the final report body.

---

## A8 — Errors ran in one direction, and the briefs, not the branches, caused most of them

**OBSERVATION.** In the correction forensics, 13 of ~20 corrections removed an
*overstatement* of threat, capability or source authority; 2 removed an
*understatement*; the rest were terminological or indeterminate. The four largest
amplification-strand errors were all **borrowings of authority** — a published
effect size used after its own authors had corrected it, a famous author's
supposed verbatim, a named government doctrine that had been retired in 2010, and
a journal named through a secondary paraphrase that was never retrieved.

**DERIVED RESULT — the errors were mostly systemic, not branch-specific.** The
self-correcting-rumour claim, the doctrine errors, the "Liddell Hart" quotation
and the persona names were all written into **child briefs by the parent** (or, in
the "perception management" case, named in the *user* prompt). Detection succeeded
where a brief said "verify this / get the exact quote" and failed where the brief
asserted.

**INTERPRETATION.** Recursive delegation propagated the parent's errors as
efficiently as it propagated its corrections. The architecture provides no
mechanism that distinguishes an inherited assumption from a discovered fact —
both arrive as context. The practical implication is that **brief hygiene
determines error rate more than branch count does**: a delegation tree cannot
verify what it was told to assume.

---

## A9 — Near-universal output, no orphans, and a single bottleneck

**DERIVED RESULT.** 152 of 153 sessions produced output that reached another
session. The one exception was a 1.7M-token session (0.1% of the run). There was
no significant body of "orphaned high-value findings" in the sense the brief
anticipated.

**OBSERVATION.** But the traffic is extremely concentrated. The root received
**49 messages, 233,673 characters** — more than any other session, and about 14%
of all message volume. Its own context reached **598,254 logical tokens** on the
final step, against a declared 1,000,000-token window (60% occupancy), and it
spent **130.2M tokens** — 10.1% of the entire run in one session.

**INTERPRETATION.** The architecture concentrates all adjudication in one context
that ends within 60% of its window. This is the structural reason corrections were
late and why the closing verification was reduced to string matching: the root had
no room to re-read its own output. Had the tree been one level deeper, the root's
synthesis problem would have been strictly harder, not easier.

---

## A10 — One session spends 39M tokens with 11 artefacts, another spends 22M with one

**DERIVED RESULT — the top two depth-1 branches by token spend behave nothing alike:**

| branch | tokens | artefacts written | artefacts consumed by others | messages sent upward |
|---|---|---|---|---|
| Health and military scare cases | 39,337,578 | 11 | 36 inherited reads | 5 |
| Agentic AI capability evidence | 22,056,925 | 1 | 54 inherited reads | — |

**OBSERVATION.** "Agentic AI capability evidence" produced exactly one artefact —
`amplification/findings/04-agentic-capability.md` — and it became the single
most-read evidence file in the run after the report itself. "Health and military
scare cases" produced eleven, only some of which anyone read.

**INTERPRETATION.** There is no relation in this run between token spend and
influence, and none between number of artefacts and influence. The unit that
mattered was a *single well-targeted synthesis of a decisive question*. Any
budgeting heuristic based on branch size would have misallocated here.

---

## A11 — Timeline artefacts in the data

**OBSERVATION.** Within a session file, `session.createdAt` is offset from the
`time` field of that session's first events by ≈2 hours (root: `createdAt` decodes
to 08:21:09Z; its first `turn/start` is 10:21:34). All *event* timestamps are
mutually consistent and monotone. One delegated analysis produced a different
absolute reading by treating `createdAt` as the t=0 anchor.

**DERIVED RESULT.** All timings in this analysis are therefore reported as
intervals and orderings; absolute UTC is omitted. Any cross-check against a
delegated note that quotes absolute times should expect this two-hour offset.

**INTERPRETATION.** Minor, but recorded because it is exactly the class of
unexamined provenance assumption that produced several of the errors in §A8.

---

## A12 — What was *not* found (negative findings preserved)

Deliberately recording the anticipated anomaly types that did **not** appear, so
that absence is not mistaken for a search:

- **No repeated rediscovery storm.** Unique normalised queries were 2,416; only
  46 (1.9%) were run by more than one session. Duplication was much lower than
  the brief anticipated. (The apparent repeats — "drone", "query" — are shell
  variable artefacts, not real duplicate searches.)
- **No pathological recursion.** Branching factor never exceeded 9 children for
  any node (median 2). No session spawned runaway children.
- **No detectable lock-step convergence on a single source.** Depth-1 branch
  domain overlap is low: median pairwise Jaccard **0.031** across 120 branch
  pairs; the union of evidence hosts is 1,609 against a per-branch sum of 2,400
  (overlap factor 1.49×). Shared hosts are the high-traffic outlets any broad
  search would find (theguardian.com in 36 sessions, nature.com in 31, gov.uk in
  30) — which is a shared *web*, not necessarily shared *reasoning*.
- **No evidence of a branch deliberately gaming or flattering the parent.** The
  disagreements found are substantive and were acted on.
- **No machine-readable cost data.** Prices, cache writes and billing are absent
  from the export, so no true cost figure can be produced (see
  `01-corpus-manifest-and-schema.md` §3).
