# Marginal return, scaling and stopping

**Question.** Does the log contain observable signals that would support a
practical stopping rule for a recursive research run? And separately: did more
research buy more knowledge, or more confidence?

**Answer in one line.** Source discovery decayed steeply and predictably while
artefact production stayed flat, so a stopping rule keyed on new-source rate would
have fired at roughly 60–70% of the run; but the run's most important *negative*
findings arrived at 63–86% and one decisive correction at 76%, so firing there
would have cost real knowledge. There is no single optimal stopping point in this
data — the two curves that would justify stopping and continuing point in opposite
directions.

---

## 1. Where the model work actually went

**DERIVED RESULT.** The run is two research batches plus a finalisation phase, all
driven from one root session:

- **Batch 1** ("AI/autonomy and the economics of harmful capability"), 8 depth-1
  branches, ~08:22–10:40 local → root turns 1–6.
- **Batch 2** ("agentic threat amplification"), 8 depth-1 branches, ~11:18 local
  onward → root turns 7–18.
- **Finalisation**, root turns 15–18.

**OBSERVATION — a 33-minute idle gap separates them.** From 08:44:38 to 09:17:39 UTC
the entire 153-session system produced **exactly one** assistant step; the pause ends
when the user commissions the second question. Merged across all sessions, gaps over
a minute total **36.7 minutes**. The 96-minute span therefore contains about
**63 minutes of actual work**, in two bursts.

**DERIVED RESULT — division of labour** (`tables/phases.csv`). Note these
"childTokens" figures count every child session alive in the phase window, so a
long-lived session is counted in more than one phase and the column **does not sum
to the run total**; the shares are the meaningful quantity.

| phase | root tokens | child tokens in window | child sessions alive | root share |
|---|---|---|---|---|
| P1 topic-1 build (turns 1–6) | 26,251,407 | 282,800,050 | 47 | 8.5% |
| P2 topic-2 build (turn 7) | 33,902,574 | 866,428,406 | 103 | **3.8%** |
| P3 topic-2 extension (turns 8–14) | 47,212,080 | 583,613,338 | 55 | 7.5% |
| P4 finalisation (turns 15–18) | 22,853,943 | 77,466,051 | 9 | 22.8% |

**DERIVED RESULT.** Root total: 26.2M tokens for topic 1, 104.0M for topic 2.
Against 1.286B total, the root is **10.1%** of all tokens. The entire distributed
tree is ~90%, and children outnumber the root's own work by roughly **9:1**.

**INTERPRETATION.** The architecture is a single synthesizer with a very large
distributed evidence-gathering organ. That is the opposite of a peer network: there
is no second adjudicator anywhere in the 153 sessions.

---

## 2. Diminishing returns: the source curve

**DERIVED RESULT — new-source discovery per decile of model work**
(`tables/discovery_by_work.csv`; bins contain equal numbers of assistant steps, so
each bin is equal model work):

| decile | new hosts | new queries | cumulative hosts |
|---|---|---|---|
| 10% | 428 | 249 | 428 |
| 20% | 145 | 138 | 573 |
| 30% | 95 | 233 | 668 |
| 40% | 244 | 577 | 912 |
| 50% | 210 | 400 | 1,122 |
| 60% | 199 | 298 | 1,321 |
| 70% | 107 | 179 | 1,428 |
| 80% | 106 | 152 | 1,534 |
| 90% | 48 | 105 | 1,582 |
| 100% | 66 | 90 | 1,648 |

**DERIVED RESULT.** New-host yield falls from **428** in the first decile to
**48–66** in the last two — an order of magnitude. The 40% bump is batch 2's fresh
8-branch launch, not renewed discovery in batch 1.

**OBSERVATION — but query volume does not decay at the same rate**, and stays
high through the middle (577 new queries in the 40% decile). Agents kept *asking*
new questions long after the *source pool* stopped yielding new answers.

**INTERPRETATION.** New-host rate is the cleanest observable stopping signal in
the corpus. It is cheap to compute during a run, it is monotone in expectation, and
it is not confounded by agent count. In this run it would have suggested stopping
around 70–80% of model work.

---

## 3. Diminishing returns: the artefact curve says the opposite

**DERIVED RESULT — new shared artefacts first written per decile of model work**
(`tables/stopping_signals.csv`):

| decile | new artefacts | new hosts | new queries |
|---|---|---|---|
| 10% | 51 | 428 | 249 |
| 20% | 69 | 145 | 138 |
| 30% | 28 | 95 | 233 |
| 40% | 23 | 244 | 577 |
| 50% | 17 | 210 | 400 |
| 60% | 45 | 199 | 298 |
| 70% | 32 | 107 | 179 |
| 80% | 44 | 106 | 152 |
| 90% | 43 | 48 | 105 |
| 100% | 38 | 66 | 90 |

**DERIVED RESULT.** Artefact production **does not decay**: it is 38–45 per decile
in the final three deciles, against 17–28 in the middle. The final 20% of model
work produced **81 new research artefacts**.

**OBSERVATION.** Those late artefacts were largely made from an exhausted source
pool. Across the run, 6,458 shell retrievals produced a **median result of 941
characters**; only 1,622 evidence hosts were ever reached; 36% of them were hit by
more than one session.

**INTERPRETATION.** Late output was **synthesis**, not discovery — and here the
two curves genuinely conflict. Judged by *finding new things in the world*, the run
was done by ~70%. Judged by *turning what had been found into usable, corrected
structure*, it was still working at 100%, and the correction forensics show that
work was not wasted (§4).

### 3.1 What the late output actually consisted of

A delegated analysis (`notes/marginal-return.md`) built a 43-item inventory of the
report's report-critical findings and classified each by decile. Its results refine
the picture in a way that a pure source-count cannot:

**DERIVED RESULT — findings per phase:**

| phase | root turns | findings | composition |
|---|---|---|---|
| P1 batch-1 build | 1–6 | 7 | 5 factual claims, 2 negative findings |
| P2 batch-2 build | 7 | **31** | 22 factual, 5 conceptual, 2 negative, 2 corrections |
| P3 batch-2 extension | 8–14 | 5 | **2 new primary sources, 2 negative, 1 correction — zero new factual claims, zero new concepts** |
| P4 finalisation | 15–18 | 0 | — |

**DERIVED RESULT — output tokens per newly discovered host rise ~16×**, from 1,536
in the first decile to 24,587 at the ninth, while external-URL density in the text
falls from 16.7 to 8.7 per 10,000 characters.

**DERIVED RESULT — and the final decile's output is largely document arithmetic.**
The share of assistant messages containing word-count bookkeeping rises to **39.5%
of messages and 50.5% of text characters in the final decile**, from 3.6% / 16.7% at
the fourth. In the last tenth of the run, **half of all generated text was the agent
counting its own words against a target.**

**INTERPRETATION.** Late work did not merely continue at lower yield — it **changed
kind**. It stopped producing new facts and concepts and produced *negative findings,
corrections and presentation work* instead. That is genuinely valuable (§4) and it is
also the signature of a process that had exhausted its empirical returns and was
spending its remaining budget on form.

---

## 4. What the late phase actually bought

This is where a naive stopping rule would have failed, so it is worth stating
precisely.

**DERIVED RESULT — first appearance of the decisive findings, by fraction of run
elapsed:**

| finding | first touched at | depth | sessions that ever touched it |
|---|---|---|---|
| Starbird 44:1 (single decisive item available early) | ~4% | 3 | 26 |
| Foster 2012 null on source-count | **~63%** | 3 | 4 |
| Diel 55.5% pooled detection | ~66% | 3 | 12 |
| Salvi author correction | ~66% | 3 | 4 |
| USC arXiv:2510.25003 (report's "single most important constraint finding") | **~77%** | 3 | 5 |
| OpenAI "not observed any cases … sustained audiences" | ~86% | 3 | — |
| Botometer AUC caution | ~95% | 1 | 6 |

**OBSERVATION.** Three of the four largest corrections in the run were found by
**depth-3 leaves after ~63% of the work**, and the report's own designated most
important negative finding arrived at **~77%**.

**OBSERVATION — the late phase also produced the report's "strongest documented
case".** The Galați coordinated-amplification finding (116,014 posts over seven
consecutive days, 28–105 accounts/day, described in §5.1d as "the strongest
documented case in the entire record") came from a **depth-3** branch at ~64% of the
run.

**OBSERVATION — and every late decisive item sits on a *new* retrieval**, not on
synthesis citing synthesis: an arXiv fetch, the arXiv/ACM paper for the USC study,
the Starbird full text, and an OSF preprint. This directly falsifies the hypothesis
that late branches were merely restating earlier material.

**INTERPRETATION.** A stopping rule firing at 70% on new-host rate would have
removed the Foster null, the Diel figure, the Salvi correction, the Galați case and
the USC paper — that is, most of the report's negative case, its strongest positive
case, and most of its corrections. **The source-discovery curve and the
epistemic-value curve are not the same curve**, and in this run they diverge
precisely late. This is the strongest argument in the data against a single cheap
stopping heuristic.

**But the same late phase also produced low-value output.** The counter-evidence,
stated fairly:

- The final decile produced **66 new hosts** — and those hosts fed 38 new
  artefacts.
- 40 depth-3 sessions spent 190M tokens producing delegations that were refused
  (see `06-anomalies-and-unexpected-behaviour.md` §A1). This work is not
  recoverable as knowledge.
- Depth 3's *file-level* productivity was 44.9% (§A2), though the message channel
  raises that to near-universal.

**Honest reading.** The late phase contained both the run's best corrections and a
large volume of refused or redundant work. It was not decaying; it was
**high-variance**.

---

## 5. The signal that actually distinguishes late value

**DERIVED RESULT.** Comparing the late findings that mattered against the late work
that did not, the discriminator is not volume or depth but **what the agent did**:

- The three decisive corrections all came from agents that went to **primary
  literature or primary documents** (an *Acta Psychologica* abstract, a publisher
  author-correction notice, an Internet Archive full-text search, an arXiv/ACM
  paper).
- The refused and redundant late work was overwhelmingly **re-querying a known
  source space** — 40 leaves writing fresh delegations into topics their parents
  had already covered, mid-way through answering their own prompts.

**INTERPRETATION.** A stopping rule that only watched *new-host rate* would have
been wrong. A rule that watched **the rate at which retrieval acts landed on
primary sources new to the run** would have tracked the valuable late work much
better. That quantity is computable during a run (`targets.csv` distinguishes
`doi.org`, publisher domains, `arxiv.org`, government domains from news and
aggregators) and is the most useful candidate this analysis can offer.

---

## 6. Confidence without knowledge — what can and cannot be shown

The brief asked whether the run started producing more confidence than knowledge.
Some signatures are testable here; others are not.

**DERIVED RESULT — output-to-novelty ratio.** Output tokens per newly-discovered
host:

| phase of work | output tokens | new hosts | output per new host |
|---|---|---|---|
| first 50% | 4,118,213 | 1,122 | 3,670 |
| last 50% | 5,190,644 | 526 | 9,868 |

Output volume rose 26% while new-source discovery more than halved, so **each new
source late in the run came with roughly 2.7× more generated text than early**.
This is the signature the brief hypothesised, and it is present.

**OBSERVATION — confidence language did not measurably strengthen.** The report's
stated confidence is *high* only for the pre-agentic mechanism and the production/
reach distinction, and *low* on material effects and attribution — the opposite of
escalation. Correction direction was also overwhelmingly deflationary:
13 of ~20 corrections removed an overstatement, only 2 removed an understatement.
So on the artefact, the run ended **less** confident than it began.

**DERIVED RESULT — the one place confidence measurably exceeded its base.** The
report's "six independent evidence streams converged" (§7.5) is a claim about the
strength of the evidence base that (a) has a single point of origin in a depth-2
agent, (b) is absent from seven of eight strand briefs, and (c) was written into
the draft 21 minutes before the decisive paper arrived. Full trace in
`05-independence-and-convergence.md`.

**INTERPRETATION.** The run did **not** drift into general overconfidence — it
spent most of its late effort *reducing* claims. But it produced exactly one
overstated epistemic claim, and it was the claim about its own process. That is a
specific and generalisable failure: **a recursive system's self-description is the
least-verified thing it produces**, because no branch is tasked with checking it
and the synthesizer has no budget left to.

**NOT DETERMINABLE from the logs.** Whether individual agents' internal confidence
rose over the run cannot be measured: there is no calibrated confidence field, no
per-claim probability, and reasoning text is unevenly retained. Any claim that
agents "became more confident" would be an inference from rhetoric, not data, and
is not made here.

**OBSERVATION — but one related signature *is* present, and it is the clearest
instance of framing preceding evidence.** The delegated finding inventory shows that
the root's turn-7 brief named the report's key concepts **before their supporting
evidence was retrieved**:

| concept named in the brief | first named | supporting evidence first retrieved |
|---|---|---|
| "liar's dividend" (and the 45–54% figure) | 09:19:30 | **09:24:57** — 5.5 min later |
| Havana syndrome, Boston 2013, Starbird | 09:17:57 | Starbird full text **09:45:54** — 28 min later |

**INTERPRETATION.** This is the same pattern as the conclusion-before-evidence
finding in `05-independence-and-convergence.md`, observed at the level of individual
concepts rather than the overall verdict. **Naming a concept first is not
illegitimate** — it is how research briefs direct attention — but it means the
evidence retrieved afterwards was sought to *populate* a named idea rather than to
test whether the idea existed. Both are visible in this run; only the second
generates an error signal.

---

## 6.1 Limitations of the stopping analysis

1. **`data/targets.csv` undercounts retrieval.** It is built from explicit tool
   arguments, and misses URLs that appear only inside shell pipelines. Verified
   case: the USC arXiv paper is demonstrably fetched but is absent from the target
   list. **All "new host" counts in this document are therefore lower bounds**, and
   the decay they show is if anything understated.
2. **The numeric-fact proxy in the delegated inventory is contaminated** by
   self-referential word and byte counts; roughly half the "factual findings" in the
   last two deciles are the agent's own document arithmetic.
3. **Phase boundaries are cut at root-turn boundaries, not even time**, because the
   run contains a 33-minute idle gap (§1).
4. **Correctness is not measured.** A "finding" here is something an agent asserted
   with retrieval behind it. Whether it is true is outside this analysis.

---

## 7. Candidate stopping rules, scored against this run

| rule | would it have fired usefully? |
|---|---|
| **New-host discovery rate below threshold** | Fires ~70–80%. **Would have cut the Foster null, the Salvi correction and the USC paper.** Rejected. |
| **New *primary-source* rate below threshold** | Would fire later and would track where the value was. **Best candidate.** Not computable from the export alone at run time without defining "primary", but the classification is simple and available. |
| **Correction rate → 0** | In this run corrections were *increasing* to the end (root's own tally went 6 → 7 → 8 over its last three turns). Would not have fired. |
| **Artefact-production rate below threshold** | Flat to the end; would never have fired. Useless here. |
| **Conclusion stability across branches** | The conclusion never moved after +59.7 min while evidence kept arriving — so this rule would have fired *too early*, before the evidence that justified it, and would have ratified the pre-written verdict. **Actively dangerous.** |
| **Depth cap / budget cap** | What actually stopped this run (99 refusals at depth 4). Effective and predictable, but arbitrary w.r.t. knowledge. |

**Synthesis.** The only signal in this corpus that separated valuable late work
from churn was **whether retrieval was reaching *new primary sources***. Conclusion
stability — the signal a process is most likely to reach for — is exactly the wrong
one, because in this run it was produced by a prior written before the evidence.
