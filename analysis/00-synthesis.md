# What the scale actually bought

### A synthesis of the DSH recursive research run of 25 September 2026

---

## 0. What was analysed, and how to read this

This is an analysis of a **completed** research run, treated as an empirical
object. The research itself is not continued here. The primary dataset is the
exported session logs — 153 sessions, 281 MB, 67,072 records — together with the
research workspace the run produced. The corpus was not modified.

**Evidentiary labels.** Every substantive claim below is tagged **OBSERVATION**
(directly in the logs or artefacts, quoted or cited), **DERIVED RESULT** (from
systematic computation, with the number), or **INTERPRETATION** (what it may mean).
Derivations are reproducible from `analysis/tools/`; tables are in `analysis/data/`
and `analysis/tables/`; three delegated sub-analyses are in `analysis/notes/` and
were independently spot-checked in `analysis/notes/validation.md`.

**Scope of the claims.** Nothing here judges whether the research *conclusions were
true*. It judges what the process did, what it produced, and what that implies for
recursive agent research. Where the logs cannot settle a question, that is stated.

---

## 1. The run in numbers

**DERIVED RESULT.**

| | |
|---|---|
| Wall clock span | **96.1 minutes**, of which **≈33 minutes idle** |
| Active work | **≈63 minutes** in two bursts (batch 1, then batch 2) |
| Sessions | **153** (1 root + 152 subagents) |
| Delegation depth reached | **3** (of a permitted 3) |
| Sessions that themselves delegated | **79** (52%) |
| Spawn attempts | 251 — 152 succeeded, **99 refused by the depth cap** |
| Model steps | **10,037** |
| Tool calls | **16,195** |
| Total tokens | **1,286,531,354** |
| — cache reads | 1,258,387,840 (**97.81%**) |
| — uncached input | 18,834,657 (1.46%) |
| — output | 9,308,857 (0.72%) |
| Logical input processed | 1,277,222,497 |
| Reasoning share of output | 30.9% |
| Files in the research workspace | **2,161** (~945 MB of captures) |
| Distinct evidence hosts reached | **1,609** |
| Agent-to-agent messages | 374, carrying 1,645,470 characters |

**OBSERVATION — the run is two bursts, not one continuous effort.** There is a
**33.0-minute gap** (08:44:38 → 09:17:39 UTC) in which the entire system produced
**exactly one** assistant step. The pause ends when the user commissions the second
research question. Merged across all 153 sessions, gaps longer than a minute total
**36.7 minutes**. So the run's *span* is 96 minutes but its *work* is roughly 63 —
a distinction that matters for any per-hour productivity claim.

**DERIVED RESULT — the distribution is extreme.** One context — the root — holds
10.1% of all tokens, 391 tool calls and 112 edits to the report, and reached
**598,254 logical tokens** against a declared 1,000,000-token window (60% occupancy).
The other 152 sessions share 89.9%.

**OBSERVATION.** Both topics were researched in one session with one synthesiser:
topic 1 ("AI/autonomy and the economics of harmful capability") in root turns 1–6,
topic 2 ("agentic threat amplification") in turns 7–18, the latter commissioned by
the *user* mid-run.

---

## 2. What the scale bought

### 2.1 Genuine, broad, non-overlapping evidence gathering

**DERIVED RESULT.** Across the 16 depth-1 branches, median pairwise **domain**
Jaccard is **0.031** (n=120 pairs). The union of evidence hosts is 1,609 against a
per-branch sum of 2,400 — an overlap factor of only **1.49×**. At URL level, maximum
pairwise Jaccard across the eight amplification strands is **0.076**, with 6.2% of
URLs shared. Every domain fetched by three or more strands is search or
bibliographic infrastructure.

**DERIVED RESULT — and the fan-out found things that repeated search would not.**
Three of the report's most important negative findings were independently reached
from different queries by different strands hitting the same primary document
(Botometer's AUC correction; OpenAI's own "no sustained audience" statement; the
USC simulation-only paper). On the USC paper the report actually *understates* the
independence, crediting one strand when two reached it.

**INTERPRETATION.** The parallel breadth is real and is the run's clearest
achievement. The 153 agents did not mostly re-read each other; they read different
things. Duplication was far lower than the brief anticipated — only **1.9%** of 2,416
unique normalised queries were run by more than one session.

### 2.2 Error detection that a shallow process would have missed

**OBSERVATION.** Three of the four largest corrections in the run came from
**depth-3 leaves** that went to primary literature after the root *and* the
depth-1/2 leads had asserted the opposite:

- a depth-3 agent retrieved the **Foster et al. 2012** *Acta Psychologica* abstract —
  "Repetition, not number of sources" — the null that contradicted the root's own
  designated "genuinely new capability";
- another found the **30-day-old author correction** to Salvi et al. that retired
  the most-cited positive effect size in AI-persuasion research;
- a third used an Internet Archive full-text search to return **zero hits** for a
  "Liddell Hart" quotation that a depth-1 agent had written into its own brief.

**DERIVED RESULT — the run reconstructed ~20 corrections** (a delegated forensic
pass; 7 advertised by the report, 13 recovered that it does not advertise). **13 of
~20 removed an overstatement** of threat, capability or source authority; **2**
removed an understatement. The four largest amplification-strand errors were all
**borrowings of authority** — a real effect size used after its authors had corrected
it, a famous author's supposed verbatim, a doctrine retired in 2010, a journal named
through a secondary paraphrase never retrieved.

**INTERPRETATION.** This is the strongest positive finding in the analysis:
**recursive delegation produced a genuine peer-review-like mechanism**. Not because
many agents agreed, but because a leaf with a narrow mandate read a primary source
that its ancestors had not. The mechanism is real and it is the thing scale bought
that a single long context plausibly could not.

### 2.3 Cache-served feasibility

**OBSERVATION.** All 153 sessions received **byte-identical** system prompts and
tool schemas. The first model step of **152 of 153** sessions read **exactly 7,936**
cached tokens; the root, which ran first and cold, read 1,280.

**DERIVED RESULT.** 97.81% of all input was served from cache. The root re-read its
own accumulated context 369 times over (129.6M cache reads against 351K fresh input);
the most context-heavy branch 84×. Under an illustrative 1/10 cache-read price, the
run's 1.28B logical input tokens cost the equivalent of ~145M — an **88.7%**
reduction.

**INTERPRETATION.** Cache reuse is very likely the condition that made a 153-agent,
96-minute run affordable at all. Critically, **fan-out is what benefits**: every new
agent inherits a prefix that is large and already hot, a benefit unavailable to a
single cold session and one that *scales with agent count*.

But cache efficiency is **not** an argument for scale, and this run demonstrates
why. The same mechanism makes **re-synthesis** cheap — which is exactly why the last
20% of the run could produce 81 new artefacts from a source pool that had stopped
growing without the volume registering as new knowledge.

---

## 3. What the scale did not buy

### 3.1 Convergence that was actually convergence

The final report's central epistemic claim is that **"six independent evidence
streams converged"** on the verdict *plausible, novel, and currently unobserved*
(§7.5, repeated at §1 and §12). **The logs do not support it.**

**OBSERVATION — the trace.** The phrase enters the report at root `seq 2017`, **13
seconds** after a message from depth-1 session `6f182957` ("Concept genealogy and
fit"), which reported: *"resting on six independent evidence streams … which all six
**agents** converged on independently."* That session has **exactly six children** —
six sibling sub-agents it spawned, briefed and adjudicated itself.

**OBSERVATION — the verdict sentence has one author.** The formulation *"plausible,
novel, and currently unobserved"* first appears in **one depth-2 agent**
(`edb0f8d3`, inside that same branch). It appears in exactly **two** places in the
entire workspace: that agent's own file, and the final report. **None of the 21
`findings/*.md` briefs contains it** — including the brief of the strand that
reported the six-way convergence.

**DERIVED RESULT — the verdict preceded the evidence.**

| event | t+ min |
|---|---|
| root's own prompt names the expected finding: *"most likely … neither new nor attributable to AI"* | +57.7 |
| root writes a **28,375-character draft** already containing "neither new nor", "that narrower case remains unevidenced", "The amplifier is not the botnet. It is the institution." | **+59.7** |
| Foster 2012 null on source-count | +63.1 |
| Diel 55.5% pooled detection | +65.8 |
| Salvi author correction | +66.0 |
| USC arXiv:2510.25003 — the report's "single most important constraint finding" | **+80.7** |
| OpenAI "not observed any cases … sustained audiences" | +86.1 |
| Botometer AUC caution | +95.3 |

**OBSERVATION.** The core verdict was in the draft **21 minutes before** the paper
the report calls its most important constraint finding arrived. Three branches read
that in-progress draft shortly after it was written.

**INTERPRETATION — stated at the strength the evidence supports.** This is not proof
that the strands merely ratified a pre-written answer. They assembled a real,
largely non-overlapping evidence base (§2.1), and they contradicted the parent on
numerous checkable facts. What did **not** happen is production of the conclusion by
convergence. What happened is: **a prior was stated early, independently gathered
evidence was consistent with it, and one late nested finding was cast as its
confirmation.** "Convergence" is the wrong word, and "six independent streams" is
wrong for its provenance.

**What *is* independent — the steelman, which largely succeeds.** The streams were
substantially independent in *gathering evidence* and demonstrably willing to
contradict each other (13 documented cases, including a date error caught
cross-strand and three circulating figures retracted). The failure is narrower and
more specific than "the process was an echo chamber": it is a **conflation of
independent evidence gathering with independent conclusion production**.

### 3.2 Verification of interpretation

**DERIVED RESULT — a sharp asymmetry.** Every disagreement resolved *against* the
emerging consensus concerns a **checkable factual error** — a date, a citation ID, a
dollar figure, a quotation, a mis-dated statistic. The **one** disagreement that
touched the **interpretive** core was resolved **in favour of the lead's prior**:

> a specialist sub-agent rated reflexive control only **PARTIAL** fit — *"RC is
> human-decision-centric, deliberate, state-centric, with no AI and no
> emergent/self-amplifying claim"* — and the strand lead recorded: *"**I have kept
> RC as High**"*, matching the rating already in the pre-written draft.

**INTERPRETATION.** Recursive delegation gave this run an effective immune system
against **wrong facts** and essentially none against **fixed framing**. That is the
sharpest behavioural generalisation available in the data, and it is a design
lesson, not a scaling lesson.

### 3.3 Completeness of correction

**OBSERVATION — two advertised corrections were never applied to the report body.**
"Synthetic corroboration = the genuinely new capability" is still asserted at report
lines 276, 278 and in the §5.3 heading (line 487), while lines 507 and 764 declare
it withdrawn; §12.2's *derived* bullet was correctly replaced. "Indistinguishable
from human journalism in more than half of evaluated instances" is still asserted at
line 495 while Appendix C records it as withdrawn.

**OBSERVATION — the cause is visible.** The root's closing verification pass
(`seq 1980–1996`) grepped for **named banned strings** (Krepinevich, ADA152240,
"Gerasimov Doctrine", "firehose"). A string check cannot detect a withdrawn claim
that survives **under its own original wording**.

**DERIVED RESULT — corrections were slow, and latency dominated.** The Foster null
took 2m44s to relay from depth 3 to the root; the Salvi correction **16m02s**. The
refuting Starbird PDF sat at depth 2 for **16m44s** while its wrong version was in
the report. A partial warning — *"an author correction was issued 3 Sep 2026 whose
content I could not retrieve; treat the headline figures as provisional"* — sat
unactioned for **9m19s**, during which ~3,000 model steps ran.

**INTERPRETATION.** The run could find its errors; it could not reliably **apply**
them. With 104 concurrent sessions live, correction throughput was bounded by
message travel time and the parent's attention, not by detection. And because the
one context that had to apply every correction had no reviewer, its own
incompleteness went uncaught.

**OBSERVATION — the correction count itself inflated during the run.** The agent's
own narration of how many assertions it had withdrawn reads **"Six of my own
claims"** (turn 16, step 7), then **"Seven of my own claims"** (turn 17, step 7),
then **"Eight of my own assertions"** (turn 18, step 9) — inside its final three
turns.

**DERIVED RESULT — and the count does not reconcile with the report's text.** A
direct search of the final report for explicit withdrawal language yields **four**
claims recorded as withdrawn: the self-correcting-rumour claim (line 168), the
"genuinely new capability" framing (line 764), the "more than half indistinguishable"
figure (lines 670 and 1277), and the "indistinguishable" claim again in Appendix C
(line 1374). The other items counted toward "eight" are **not the study's own
withdrawn assertions**: the Salvi figure was corrected *by its own authors*, the
"25% of Twitter activity" figure was **never used** rather than withdrawn, and the
doctrine errors were corrections to *briefs* that never reached the report.

**INTERPRETATION.** This is a small, self-contained instance of the same failure as
§3.1: an accuracy claim about the study's own process, made in the final turns,
rising without a supporting count behind it. It is worth recording because the
report is otherwise scrupulous about its errors — which is precisely why the
process-level numbers are the ones to treat with caution.

### 3.4 Marginal epistemic return

**DERIVED RESULT — discovery decays, output does not.**

| decile of model work | new hosts | new artefacts |
|---|---|---|
| 10% | 428 | 51 |
| 40% | 244 | 23 |
| 70% | 107 | 32 |
| 90% | 48 | 43 |
| 100% | 66 | 38 |

New-source yield falls an order of magnitude; artefact production stays flat at
38–45 per decile through the end. Output per newly discovered host rises **2.7×**
between the first and second half of the run.

**DERIVED RESULT — but the late phase held the best corrections.** Foster arrived at
~63%, Diel at ~66%, the Salvi correction at ~66%, and the USC paper at ~77%.

**INTERPRETATION — the two curves genuinely conflict, and there is no single optimal
stopping point in this data.** A rule keyed on new-host rate would have fired around
70–80% and would have removed most of the report's negative case and most of its
corrections. The only signal in the corpus that separated valuable late work from
churn was **whether retrieval was reaching new *primary* sources** — a rule that is
computable during a run and is the most useful practical recommendation this
analysis can offer.

**The signal a process is most likely to reach for — conclusion stability — is
actively dangerous here.** The conclusion never moved after +59.7 min while evidence
kept arriving. A stability-based stopping rule would have ratified the pre-written
verdict before the evidence justifying it existed.

### 3.5 Cost transparency

**DERIVED RESULT.** The export contains **no** cache-write counts, prices, latency
or billing data — one cache field only. No monetary cost can be computed. A session
that writes 300K tokens of context and reads it back 8 times may be **net negative**
on caching, and this export cannot distinguish that case.

**INTERPRETATION.** Claims that this run "cost X" would be unsupported. What can be
said is the shape: 1.28B logical input tokens, 97.8% cache-served, 9.3M output
tokens.

---

## 4. Anomalies that changed the interpretation

Four findings were not anticipated and each alters the analysis.

**A1 — Recursion was terminated by a hard cap, not by diminishing returns.**
**OBSERVATION.** 40 of 91 depth-3 sessions attempted to spawn; all **99** attempts
returned `Error: subagent depth 4 exceeds maxDepth 3`, each with a fully written
prompt. The 91 leaves are therefore **censored**, not concluded — 44% were still
trying to widen the tree. Any claim that "the process stopped when it stopped
producing" is false for this run; the stopping condition was infrastructural.

**A2 — The dominant transfer channel was messages, not files.** **DERIVED RESULT.**
A file-based contribution measure declared 86 of 168 presented deliverables
"orphaned". Against the message channel (374 messages, 1.65M characters), **152 of
153 sessions produced output that reached another session.** Measuring recursive
research by artefact reads systematically **understates** architectures that report
by message.

**A3 — Token spend did not predict influence.** **OBSERVATION.** "Agentic AI
capability evidence" spent 22.1M tokens and produced **one** artefact, which became
the most-read evidence file in the run after the report itself. "Health and military
scare cases" spent 39.3M (1.8×) and produced **eleven**, only some of which anyone
read. A depth-3 session spending 2.4M tokens pushed **103 URLs** upward.

**A4 — A degraded first-class tool relocated the run's capability into shared
infrastructure.** **OBSERVATION.** `web_search` failed **116 of 135** calls
(85.9%). Agents responded by writing ~30 shell scripts into the workspace and
telling each other about them; retrieval ran through **6,458 shell invocations**
instead. **DERIVED RESULT.** The most "inherited" files in the entire run are not
evidence but tooling: `tools/news.sh` (read by 52 sessions, 160 cross-session
inheriting read-acts), `tools/get.sh` (51 sessions, 111). **INTERPRETATION.** The
delegation tree shows independent agents; the `tools/` directory shows them all
coupled to the same unversioned scripts. A single bug in `news.sh` would have
silently biased every branch at once. This coupling is invisible in the genealogy.

---

## 5. When does more research become more knowledge, and when more confidence?

The run's own trajectory gives a usable answer, and it is more specific than the
question implies.

**It did not drift into general overconfidence. The opposite.** **DERIVED RESULT.**
13 of ~20 corrections removed overstatements; the report's stated confidence is
*high* only for the pre-agentic mechanism and the production/reach distinction, and
*low* on material effects and attribution. The correction tally the agent kept for
itself rose across its final three turns (six → seven → eight withdrawn assertions).
**OBSERVATION.** And the errors were overwhelmingly *borrowings of authority* —
real artefacts used at a strength the underlying evidence did not support — which is
the failure mode of a process that reads widely and summarises quickly, not of one
that is ideologically committed.

**The confidence inflation was localised, and it was about the process itself.**
**OBSERVATION.** The run produced exactly one materially overstated epistemic claim:
"six independent evidence streams converged". It was:
- written **13 seconds** after the message that prompted it, with **no intervening
  tool call**;
- a **compression** of a subordinate's hedged claim about its own six helpers;
- about **its own method**, which no branch was tasked with checking and which the
  synthesizer had no budget left to check.

**INTERPRETATION.** The generalisable finding is this:

> **In a recursive research system, the least-verified output is the system's
> description of its own process.** Every branch is scoped to a subject. No branch
> is scoped to the provenance of the synthesis. The synthesizer, working at 60% of
> its context window on its final turn, compresses what its children told it — and
> compression is where strength gets added and never checked.

So: more research became more knowledge when agents were reading **new primary
sources** — which happened to the end, and produced the run's best corrections. It
became more confidence when agents were **writing from context they already held**,
which was ~99.6% of their late input, and when the **synthesis described itself**.

---

## 6. What this teaches about recursive agent systems for serious research

**1. Independence of gathering and independence of conclusion are different
properties, and scale delivers only the first.** 153 agents and 1,609 sources
produced a genuinely broad evidence base and one author for its verdict. Counting
agents, sources or agreement measures the first and says nothing about the second.

**2. Fan-out's real product is adversarial coverage, not throughput.** The run's
best moments were leaves with narrow mandates reading primaries their ancestors had
not. The value is in the *coverage of the evidence graph*, and it is destroyed by
homogeneous briefs. Detection worked where a brief said "verify this"; it failed
where a brief asserted.

**3. Depth needs a budget line for relaying, not just for searching.** Correction
latency here was 2m44s to 16m02s of pure message travel, and one actionable warning
sat 9m19s. Discovery was never the bottleneck; the path back up was.

**4. Never let a synthesizer verify by string matching.** The two corrections that
survived into the final report body did so because a `grep` for banned strings
cannot find a claim stated in its own original words. Verification must re-read
claims, and it needs context budget reserved for it.

**5. Reserve a reviewer for the process's own self-description.** The single
unsupported claim about the whole evidence base was the one about the whole evidence
base. It needs an owner.

**6. A hard depth cap is a stopping rule, and it is not a good one.** It stopped
this run at a point where 40 agents were still actively trying to delegate, while
refusing 99 written prompts. If a cap is used, log what it refused — the refused
prompts are the cheapest available map of unmet evidence demand, and here they
included "Google TAG influence op counts", "tip yield and false-positive research"
and "cyber amplification analogies".

**7. Prefer a primary-source-rate stopping signal to a new-source-rate one.** New
hosts decayed to ~50/decile at 90% while the most valuable corrections arrived at
63–77%. New *primary* sources is the signal that tracked value.

**8. Cache economics favour fan-out, but do not confuse that with epistemic value.**
97.8% cache-served input is what made 153 agents feasible in 96 minutes. It also
made re-summarising cheap enough that the last 20% of work produced 81 artefacts
from an exhausted source pool. Cheap generation is not cheap knowledge.

---

## 7. Negative results, preserved

Recorded so that absence is not read as a search result.

- **The report's conclusions were not re-verified.** This analysis judges provenance
  and process, not truth. The report may be right.
- **Diminishing returns is not a clean story here.** Discovery decayed; corrections
  arrived late. Any single-curve stopping claim would be wrong.
- **The anticipated redundancy storm did not occur.** Only 1.9% of 2,416 unique
  queries were repeated across sessions. Duplication was low.
- **No pathological recursion.** Maximum branching factor 9; median 2.
- **No lock-step convergence on a single source.** Depth-1 domain Jaccard median
  0.031.
- **No significant orphaned high-value findings.** The "orphans" were a measurement
  artefact (§3.2), not a real loss.
- **The "assertion without retrieval" worry is not supported.** Only 7 sessions
  assert the decisive null; all 7 performed retrieval; none asserted it with none.
- **No sycophancy or flattery toward the parent.** Disagreement was frequent and
  substantive.
- **No cost figure can be produced** — cache writes, prices and billing are absent.

---

## 8. The single most interesting thing that was not asked about

The brief asked how recursive delegation affects research quality, and this analysis
answers that. But the least-sought and most consequential finding is structural:

> **The run's most important epistemic failure and its most important epistemic
> success have the same cause.** The 28 KB draft written at +59.7 min — before the
> evidence arrived — is why "convergence" is the wrong description of the verdict
> *and* is the reason a single coherent 26,000-word report exists at all. The same
> early commitment that let the synthesizer integrate 152 agents' output into one
> argument is what made the argument's provenance unverifiable.

A recursive system optimised to *produce a coherent answer* will commit early,
because commitment is what coherence requires. A system optimised to *know whether
it knows* must delay commitment, which is exactly what destroys coherence. **This
run did not choose between those; it did both, in the same context, and did not
notice.** The report's corrections are the honest record of that tension — and the
two corrections that never reached the body are where it won.

---

## 9. Outputs of this analysis

| file | contents |
|---|---|
| `01-corpus-manifest-and-schema.md` | corpus manifest, hashes, event schema, token-field semantics, what can and cannot be reconstructed |
| `02-agent-genealogy.md` | reconstructed delegation tree, branch table, influence measured two ways, termination states |
| `03-token-and-cache-tables.md` | token classes, cache architecture, cache by depth and over time, economics under assumed discounts |
| `04-contribution-mapping.md` | report sections mapped to branches; falsification counted as contribution |
| `05-independence-and-convergence.md` | the empirical test of the "six independent streams" claim |
| `06-anomalies-and-unexpected-behaviour.md` | 12 anomalies, including the depth cap, the message channel, and the tooling coupling |
| `07-marginal-return-and-stopping.md` | diminishing returns, the two conflicting curves, candidate stopping rules scored |
| `notes/corrections.md` | forensic reconstruction of ~20 corrections (delegated, spot-checked) |
| `notes/independence.md` | full independence analysis (delegated, spot-checked) |
| `notes/marginal-return.md` | 43-finding temporal inventory, phase and decile analysis (delegated) |
| `notes/validation.md` | independent verification of the delegated analyses, including one corrected error |
| `data/` | 19 machine-readable derived datasets |
| `tables/` | 14 rollup tables |
| `tools/` | 21 reproducible extraction and analysis scripts |
