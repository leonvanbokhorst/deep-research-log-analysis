# Contribution: branches mapped to the final artefacts

Data: [`tables/contribution.csv`](tables/contribution.csv) (93 report sections ×
top-matching artefacts), [`tables/branch_outputs.csv`](tables/branch_outputs.csv),
[`tables/message_flow.csv`](tables/message_flow.csv),
[`tables/phases.csv`](tables/phases.csv).

---

## 1. Method and its limits

**What was done.** The final amplification report was split into 93 sections
(≥600 characters). Each section's vocabulary was compared against the 2,161 files
in the research workspace, and the top six matches per section were mapped to their
first-writer session and delegation depth (`tools/contribution.py`).

**LIMITATION — read this before using the table.** Vocabulary similarity is a
*ranking device*, not a measure of intellectual contribution. It finds where the
same words appear, not where the reasoning came from. It cannot detect a branch
that contributed by **falsifying** a claim, **changing a confidence rating**,
**identifying a gap**, or **preventing an incorrect conclusion** — and those were
among the most valuable contributions in this run (§3). The table should be used to
locate candidates, never to apportion credit.

**A second, larger limitation, discovered while measuring.** The dominant transfer
channel between agents was not files but `send_message`: 374 messages, 1,645,470
characters, 251 report-like, 148 over 4,000 characters. A file-based contribution
measure declared **86 of 168 presented deliverables "orphaned"** — including the
main report and several depth-1 briefs. That was an artefact of the measure. Against
the message channel, **152 of 153 sessions produced output that reached another
session.** Any subsequent analysis of this run that counts only artefact reads will
misprice it.

---

## 2. The report's own account, and what the data supports

**OBSERVATION — the report's framing.** `Agentic-Threat-Amplification-2026.md`
§0.2, §1 and Appendix C: "Eight parallel research strands plus the author's own
primary-source work", with "the author's own primary-source work" named explicitly.

**DERIVED RESULT — that is a fair description of the division of labour.**

| contributor | tokens | share of run |
|---|---|---|
| root (synthesis + own primary-source work) | 130,220,004 | **10.1%** |
| 152 subagents (distributed evidence gathering) | 1,156,311,350 | 89.9% |

**DERIVED RESULT.** Root tokens by topic and phase
(`tables/phases.csv`): **26.2M** on topic 1 (turns 1–6) and **104.0M** on topic 2
(turns 7–18). Root share *within* each phase: 8.5% (P1), **3.8%** (P2), 7.5% (P3),
22.8% (P4).

**OBSERVATION.** The root performed 391 tool calls, including 168 `bash`
(institutional primary sources: Europol SOCTA, AIVD/NCTV/DTN, EPRS, NATO), 112
`edit`, 31 `read`, 16 `subagent`, 10 `send_message`, 9 `web_search`, 6 `web_fetch`
and 18 `present`.

**INTERPRETATION.** The report's self-description is accurate and modest. It does
not overclaim the strands; if anything the phrase "eight parallel research strands
plus the author's own primary-source work" undersells how much the author did, since
the root also performed the entire synthesis, all the correction adjudication, and a
substantial share of the institutional evidence gathering itself.

**The one claim the data does not support** is §7.5's "six independent evidence
streams converged" — traced in full in
[`05-independence-and-convergence.md`](05-independence-and-convergence.md).

---

## 3. Branches that materially changed the report

Contribution defined as **any observable effect on the final artefact**, including
falsification and correction.

### 3.1 Branches that supplied cited evidence

| branch | depth | artefacts | inherited reads | principal contribution |
|---|---|---|---|---|
| Agentic AI capability evidence | 1 | **1** | 54 | The single most-read evidence file in the run (`findings/04-agentic-capability.md`); supplied the AI-persuasion section and, indirectly, the Salvi figure that later had to be corrected |
| Computational propaganda evidence | 1 | 2 | 37 | Consolidated the Foster null and relayed it upward — the trigger for the report's largest correction |
| Health and military scare cases | 1 | 11 | 36 | Breadth: cross-domain generalisation of the ambiguity→disruption mechanism; also flagged the Bundestag and BKA errors |
| NATO EU institutional threat assessments | 1 | 6 | 7 | Largest message output (45,783 chars, 58 URLs); the institutional evidence base |
| Concept genealogy and fit | 1 | 1 | 6 | The concept-fit audit and the "configuration term, not a threat class" verdict |

### 3.2 Branches whose contribution was *falsification*, not text

These are the highest-value contributions in the run and are invisible to any
similarity- or reuse-based measure.

| session | depth | tokens | what it did |
|---|---|---|---|
| `fc1be9de` Detection and belief studies | **3** | — | Went to *Acta Psychologica* and returned **Foster et al. 2012, "Repetition, not number of sources"** — the null that contradicted the root's own "genuinely new capability" claim |
| `8af84e58` Research stream C AI persuasion | **3** | — | Found the **30-day-old author correction** to Salvi et al. that retired the field's most-cited positive effect size |
| `6d105fdb` (verification leaf) | **3** | — | Internet Archive full-text search returning **zero hits** for a "Liddell Hart" quotation the depth-1 agent had put in its own brief |
| `6f182957` Concept genealogy and fit | 1 | 136,376,674 | Relayed both the Foster null and the Starbird 44:1 correction to the root, and removed seven fabricated citations from its own brief |
| `8a55607d` European retractions and influence ops | **2** | 17,588,269 | Wrote the run's single best evidence file (30KB, `[P]/[J]/[T]/[NV]`-graded, with explicit retrieval failures); delivered the corrections the root acted on at turn 12 |
| `f5d926fb` | 1 | 18,316,648 | Retracted the Bundestag "technische Fehlfunktionen" claim, mis-dated BKA figures, and the "hide in the noise" inversion |

**OBSERVATION — the pattern.** Three of the four largest corrections came from
**depth-3 leaves**; the fourth came from a depth-2 agent. In each case the root and
the depth-1/2 leads had asserted the opposite. Relay latency was the bottleneck:
**2m44s** for the Foster null, **16m02s** for the Salvi correction.

### 3.3 The best evidence file was written at depth 2

`amplification/findings/drone-cases-amplification-retractions.md` — `8a55607d`,
17.6M tokens, written 11:25–11:27. It carries per-claim source grades, verbatim
non-English quotations with translations, explicit `[NV]` not-verified flags, and a
**"searched ~130 queries"** audit trail. It is the highest-quality artefact in the
workspace by evidentiary discipline and it is the direct source for the report's
case-comparison appendix and much of §5.1.

---

## 4. Branch contribution to the *first* report

**DERIVED RESULT — the autonomy report's evidence is far more concentrated.** Five
of its eight depth-1 branches never delegated at all (one session each), and the
largest branch by token spend supplied institutional and Middle East material.
Principal contributors by inherited reads: `46b82e74` ("Health and military scare
cases", 36) — though that branch belongs to topic 2 — and `f54b15a3`, `b61859d5`,
`230a12e6` (swarm audit) for topic 1.

**OBSERVATION.** The autonomous-swarm branch (`230a12e6`, "Swarm coordination
evidence audit") produced a sceptical audit that concluded large-N coordination is
"real, cheap and solved — but only for pre-planned flight in benign conditions."
That is a *deflationary* finding and it shaped the autonomy report's central
negative claim about autonomy.

---

## 5. What the contribution map cannot settle

1. **Counterfactual contribution is unmeasurable.** A branch that changed a
   confidence rating from High to Medium leaves no textual trace. Several clearly
   did this (the reflexive-control fit downgrade, the "reach is rented" reframe).
2. **The two topics are not separable by token accounting.** Batch 2's branches
   read batch 1's workspace files; the depth-2 "European retractions" file draws on
   both.
3. **Attribution to *individual* claims is not achievable from the logs.** The logs
   record what each session wrote and sent; they do not record which sentence of the
   final report came from which sentence of which intermediate file, because the
   root rewrote nearly everything (112 `edit` calls) rather than assembling.
4. **The most influential input may be the one nobody read.** The user's
   commissioning prompt supplied the five-category taxonomy, the four-level
   framework, the "qualitative rather than volume" question, and the
   "agentic threat amplification" label itself. Every branch inherited them. By any
   causal measure the prompt contributed more to the report than any strand — and it
   is invisible to every table in this directory.
