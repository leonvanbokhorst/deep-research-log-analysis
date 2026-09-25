# Evidence independence and convergence

**The claim under test.** The final amplification report states twice that "six
independent evidence streams converged" on the verdict *plausible, novel, and
currently unobserved* (§7.5, line 775 and line 801), and Appendix C describes the
method as "eight parallel research strands".

**Verdict in one line.** The strands were **substantially independent in gathering
evidence and demonstrably willing to contradict one another**; they were **not
independent in producing the conclusion that the report attributes to them**. The
report conflates those two things. The load-bearing convergence sentence was
written by **one deeply nested agent**, was absent from **seven of the eight**
strand briefs, and the verdict was in the draft **before the decisive evidence
arrived**.

Everything below is traceable to `data/`, `tables/`, the raw export, or
`notes/independence.md` (delegated, then independently re-checked — see
`notes/validation.md`).

---

## 1. The "six streams" are not the eight strands

**OBSERVATION.** The phrase enters the report at root `seq 2017` (turn 18, step 3),
**13 seconds** after an `agent/inbox/spliced` message at `seq 2004` from
depth-1 session `6f182957-7587-4604-97e9-5b8275f63b51` ("Concept genealogy and
fit"), which said: *"FINAL VERDICT (unchanged, now resting on six independent
evidence streams)"* and *"All six **agents** converged independently"*.

**DERIVED RESULT.** `data/edges.csv` filtered to `parent = 6f182957…` returns
exactly **six children** — rumour theory, active measures, reflexive control,
perception management, self-amplifying attack concept, computational propaganda.
They are **six sibling sub-agents of one strand**, briefed by that one strand, and
their output was adjudicated by that one strand before relay.

**DERIVED RESULT.** Two other branches also used "six": `31ca772b` (personas) had
six children, and `b61859d5` (computational propaganda) described its own six
graded working files as "all six streams in". The run contains at least three
different referents for "six streams".

**DERIVED RESULT — the probability that the eight strands' evidence base is what
was meant is nil, and the logs contain no test of independence.** The root
re-labelled a branch's internal report about its own helpers into a claim about the
study's evidence base. Note the exact wording drift, which is the entire finding:

| level | wording |
|---|---|
| `6f182957` (d1, to root) | "six independent evidence streams" / "all six **agents** converged independently" |
| report §7.5 (d0) | "**Six independent evidence streams converged** on the same conclusion" |
| report §7.5 close (d0) | "the words **all six strands** converged on independently" |

The root's own text oscillates between "streams" and "strands" — evidence that the
referent was never fixed.

---

## 2. What *is* independent: the evidence base

This is the steelman, and it largely succeeds.

**DERIVED RESULT — source overlap between the 16 depth-1 branches** (the whole
subtree of each; evidence hosts only, excluding search engines, archives and
social platforms, from `data/targets.csv`):

- median pairwise Jaccard over **domain** sets: **0.031** (n = 120 branch pairs)
- union of evidence hosts across all branches: **1,609**
- sum of per-branch host sets: **2,400** → overlap factor only **1.49×**

**DERIVED RESULT.** 1,622 evidence hosts were targeted in total; **584 (36.0%)**
were targeted by more than one session. The hosts shared across many sessions are
the ones any broad search would reach — `theguardian.com` (36 sessions),
`nature.com` (31), `gov.uk` (30), `reuters.com` (26), `anthropic.com` (24),
`bbc.com` (24), `openai.com` (23), `arxiv.org` (23). Shared *web*, not necessarily
shared reasoning.

**DERIVED RESULT — the delegated analysis's own harder test agrees.** At the level
of individual URLs, maximum pairwise Jaccard across the eight amplification strands
was **0.076**, with only **6.2%** of distinct URLs shared; and **every** domain
fetched by three or more strands is search or bibliographic infrastructure
(OpenAlex, Crossref, DuckDuckGo, archive.org, `r.jina.ai`, Google News).

**DERIVED RESULT — decisive items were genuinely re-discovered across streams.**
Three of the report's most important negative findings were independently reached
from different queries by different strands hitting the same primary document:

| finding | independently reached by |
|---|---|
| Botometer AUC 0.85 (not 0.94) | 3 streams, same sentence quoted |
| OpenAI: AI influence ops "do not appear to have meaningfully increased their audience engagement or reach" | 3 streams, `openai.com` |
| USC/arXiv:2510.25003 (simulation-only coordination) | surfaced first by one strand, first verified by another |

**INTERPRETATION — and a correction to the report's own credit.** On the USC paper
the report credits only the platform-propaganda strand, but the logs show another
strand surfaced it first. So for that particular item, **independence is
understated**. Independence is not the report's problem.

---

## 3. What is *not* independent: the production of the conclusion

### 3.1 The verdict sentence has a single point of origin

**OBSERVATION (quoted chain).**

| # | Where | Text |
|---|---|---|
| 1 | root → strand-1 prompt, +57.65 min | *"the most likely finding is that most of the mechanism is already described by existing concepts and only specific parts are new"* |
| 2 | strand-1 → its child | OpenAI *"statement that these operations have not achieved sustained audience engagement"*; *"exaggerating AI agent amplification may be a known failure mode"* |
| 3 | that child → its child | *"any OpenAI/Anthropic statement that these operations have NOT achieved sustained audience engagement or reach"* |
| 4 | **depth-2 agent `edb0f8d3`, +88.4 min** | **FIRST APPEARANCE:** *"The hypothesis should be presented as **a plausible, novel, and currently unobserved threat class — not as an extrapolation from demonstrated effects.**"* |
| 5 | relays up d2 → d1 → d0 | arrives as a branch's internal "FINAL VERDICT" |
| 6 | root `seq 2017`, +95.6 min | *"**Six independent evidence streams converged** on the same conclusion"* |

**DERIVED RESULT.** The formulation appears in exactly **two** places in the entire
research workspace: the depth-2 agent's own source file, and the final report.
**0 of the 21 `findings/*.md` briefs contain it** — including the brief of the very
strand that reported the six-way convergence.

### 3.2 The verdict preceded the decisive evidence

**DERIVED RESULT — ordering of the root's conclusion versus the evidence for it**
(t = run start, from event `time` fields):

| event | t+min |
|---|---|
| root's own hypothesis prompt names the expected finding: *"most likely … neither new nor attributable to AI"* | **+57.7** |
| root writes a **28,375-character draft report** already containing "neither new nor", "that narrower case remains unevidenced", "The amplifier is not the botnet. It is the institution.", and High fit ratings for reflexive control and SARF | **+59.7** |
| Starbird 44:1 — the *only* decisive negative already in hand | +3.9 |
| Foster 2012 null on source-count | **+63.1** |
| Diel 55.5% pooled detection | +65.8 |
| Salvi author correction (+81.2% → +48.7%, n.s.) | +66.0 |
| USC arXiv:2510.25003 (the "single most important constraint finding") | **+80.7** |
| OpenAI "not observed any cases … sustained audiences" | +86.1 |
| Botometer AUC caution | +95.3 |

**DERIVED RESULT.** The report's core verdict was written into the draft at
**+59.7 min**. Every decisive negative except Starbird arrived **after** it —
Foster 3.4 min later, the "single most important constraint finding" **21 minutes**
later, the Botometer caution **35.6 minutes** later.

**OBSERVATION — the draft was read back by the branches.** Three strands read the
root's in-progress report shortly after it was written (`+60.12`, `+60.24`,
`+61.54`). Total exposure is small — **4 read-acts by 2 non-root sessions** — but
the direction is the one that manufactures apparent consensus.

**INTERPRETATION.** This is not proof that the strands merely ratified a
pre-written answer; the evidence base they assembled is real and non-overlapping
(§2), and they did contradict the parent on many factual points. But it does mean
the *conclusion* was not produced by convergence. What happened is better described
as: **a prior was stated early, independently gathered evidence was consistent with
it, and one late nested finding was cast as its confirmation.** "Convergence" is
the wrong word for that, and "six independent streams" is wrong for its
provenance.

---

## 4. Assertions without retrieval: the worry that does *not* hold

The strongest form of the propagation concern would be a conclusion circulating
with no retrieval behind it. The delegated analysis tested this directly and found
it **not supported**.

**DERIVED RESULT.**

- Only **7 sessions** assert the decisive null at all (4 in strand 1, 2 in strand 6,
  1 root). **Six of the eight strands never asserted it in that form.**
- All 7 performed retrieval; **0 asserted it with no retrieval act**.
- 3 had the claim in inbound context *and* did their own retrieval *without* the
  evidence appearing in their own results — these are the closest thing to
  inherited assertion, and they are a minority.

**INTERPRETATION.** The process was not producing confident claims from nothing. It
was producing a *small number* of well-retrieved claims and then describing their
provenance inaccurately. That is a **reporting** failure more than an epistemic
one — which makes it more fixable, but also more likely to be missed, because the
underlying work is sound.

---

## 5. Disagreement was real — and asymmetric

**OBSERVATION.** 13 documented cases of genuine contestation, including
cross-strand correction of a wrong date (*"there is no verifiable '12 December
2024 joint statement' — the four-agency statement is 17 Dec 2024"*), retraction of
circulating figures (Bundestag "technische Fehlfunktionen"; "~30,000" anthrax
hoaxes; a mis-cited National Academies ID), and a strand declaring a component of
the thesis *"contradicted, not merely unproven"*.

**DERIVED RESULT — the asymmetry.** Every disagreement resolved *against* the
emerging consensus concerns a **checkable factual error** — a date, a citation ID,
a dollar figure, a quotation, a mis-dated statistic. The **one** disagreement that
touched the **interpretive** core was resolved in favour of the lead's prior:

> specialist sub-agent rated reflexive control only **PARTIAL** fit — *"RC is
> human-decision-centric, deliberate, state-centric, with no AI and no
> emergent/self-amplifying claim"* — and the strand lead recorded: *"**I have kept
> RC as High**"*, matching the rating already in the pre-written draft.

**INTERPRETATION.** Verification pressure in this run was **strong on facts and
weak on interpretation**. Recursive delegation gave the process a real capacity to
catch wrong dates and invented quotations, and essentially no capacity to revise a
framing once a parent had committed to it. This is the single most useful
behavioural generalisation in the analysis, and it is consistent with the
correction forensics (`06-anomalies-and-unexpected-behaviour.md` §A8).

---

## 6. Local-vs-external retrieval

**DERIVED RESULT** (`data/io_acts.csv`). Across the whole run: 16,195 tool calls,
classified as `bash_other` 10,173 (these are overwhelmingly external retrieval via
`curl`, since the built-in search was broken), `shared_read` 1,556,
`shared_write` 1,419, `external_fetch` 1,361, `shared_rw` 394,
`agent_coordination` 415, `delegation` 251, `external_search` 135.

**DERIVED RESULT — cross-session inheritance of file content.** 119 research
(not tooling) files were read by a session *after* a different session wrote them,
across 1,174 read-acts. The most-inherited research artefacts were:

| artefact | inherited reads | first writer depth |
|---|---|---|
| the report itself (in progress) | 62 | 0 |
| `findings/04-agentic-capability.md` | 54 | 1 |
| `findings/03-computational-propaganda.md` | 37 | 1 |
| `sources/raw-adversary.md` | 25 | 1 |
| `sources/anthropic-ti-sep2026.txt` | 22 | 2 |

**OBSERVATION — but the dominant channel was messages, not files.** 374
agent-to-agent messages carried 1,645,470 characters; 251 look like full reports
and 148 exceed 4,000 characters. On that measure **152 of 153 sessions produced
output that reached another session.**

**INTERPRETATION — a methodological warning that matters for anyone repeating
this.** A file-provenance-only analysis would have concluded that 86 of 168
presented deliverables were "orphaned". They were not: their content had already
travelled upward inline. **Measuring influence by artefact reads systematically
understates architectures that report by message.** The corrected picture is that
inheritance was real and bounded, and that near-universal output coexisted with
highly concentrated *adjudication* (§A9).

---

## 7. Verdict, stated at the strength the evidence supports

**What the logs support:**

> Eight strands assembled a large and largely non-overlapping evidence base, read
> each other's material sparingly, and contradicted each other and the parent on
> numerous checkable facts. Several independently surfaced the same primary
> negatives from different queries. The report's exact conclusion sentence,
> however, was composed by a single depth-2 agent, is absent from seven of the
> eight strand briefs, and rests on a decisive paper that arrived twenty-one
> minutes after the conclusion entered the draft. The phrase "six independent
> evidence streams" originated as one branch's description of its own six
> sub-agents.

**What the logs do not support:**

- that the conclusion was produced by convergence;
- that the streams were independent *in producing it*;
- that independence can be inferred from the number of agents, the number of
  sources, or the number of strands (all three are large here, and none of them
  bears on this question).

**Flagged uncertainty.**

- Correctness of the verdict itself was **not** re-verified by this analysis. The
  report may well be right. The finding here concerns the provenance of the claim,
  not its truth.
- The delegated analysis asserted that "99 depth-4 agents are missing from the
  export". **That is an error and is corrected here.** All 251 spawn attempts
  reconcile exactly: 152 succeeded (matching the 152 exported subagent sessions)
  and 99 were refused by the depth cap with `Error: subagent depth 4 exceeds
  maxDepth 3`. No agent is missing. This was re-verified directly; see
  `06-anomalies-and-unexpected-behaviour.md` §A1.
- Everything above concerns the *amplification* topic. The earlier autonomy topic
  is analysed separately in `notes/marginal-return.md`.
