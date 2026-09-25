# Forensic reconstruction of factual corrections in the DSH "agentic threat amplification" run

**Analyst note.** This document reconstructs the history of factual corrections inside a *completed* run.
Nothing here continues the research. All log references are to the immutable export at
`dsh-session-session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357/`. Timestamps are UTC (`time` field, ms).
Seconds-offsets are given relative to the session header `createdAt = 1790324469511 = 2026-09-25T08:21:09.511Z`.
Every substantive statement carries a label:

- **OBSERVATION** — directly present in the logs or the files (quoted, with session id + event `seq` and/or report line).
- **DERIVED RESULT** — follows from systematic comparison/counting (the command or count is shown).
- **INTERPRETATION** — what it might mean. Kept separate; not overclaimed.

---

## 0. Corpus facts and method

**OBSERVATION.** The export contains 153 sessions: 1 root (`session-92c9e38d…`, depth 0) + 152 subagents
(16 at depth 1, 45 at depth 2, 91 at depth 3). `analysis/data/sessions.csv` reports 10,037 `step/start`
events and 16,195 tool calls. The root ran 08:21:09Z → 09:57:16Z (96.1 min). The amplification strand —
the artefact that carries almost all the advertised corrections — is a *late extension*: the user message
that commissions it is at **seq 886, 09:17:39Z** (offset +56.5 min). Every correction below therefore
happened inside a 40-minute window (09:17:39Z → 09:57:16Z) with ~100 agents live concurrently.

**DERIVED RESULT.** Count of live agent activity inside each correction window was computed with
`analysis/tools/window.py` (counts `step/start` events across all 153 sessions in a `[t0,t1]` window).
This is the metric used below for "how much work happened while the error stood".

**OBSERVATION (the report's own correction register).** `amplification/Agentic-Threat-Amplification-2026.md`
contains explicit, self-declared correction markers at lines **168, 507, 615, 670, 764, 838, 1374**
and two doctrine corrections at **137–142**; the companion report
`AI-Autonomy-Threat-Assessment-2026.md` carries three more at lines **236, 333, 335**.

**DERIVED RESULT (git archaeology of the final artefacts).** The research workspace is a git repo.
The amplification report's first commit is `b0847b0` (11:29:48+0200 = 09:29:48Z). Command:
`git show <commit>:amplification/Agentic-Threat-Amplification-2026.md | grep -c "<pattern>"`.
Presence of each disputed string, by commit:

| commit (local) | UTC | 25% Twitter | "more than half" | "often *self-correcting*" | "genuinely new capability" | 81.2% | 48.7% | Foster | 55.5% |
|---|---|---|---|---|---|---|---|---|---|
| b0847b0 11:29:48 | 09:29:48 | 1 | 1 | 1 | 3 | 1 | 0 | 0 | 0 |
| 3e044e8 11:37:17 | 09:37:17 | 1 | 1 | 1 | 3 | 1 | 0 | 2 | 2 |
| 951da4f 11:37:29 | 09:37:29 | 1 | 1 | 1 | 3 | 1 | 0 | 2 | 3 |
| f510eee 11:43:42 | 09:43:42 | 1 | 1 | 0 | 3 | 1 | 2 | 2 | 3 |
| 9ddb9fb 11:50:40 | 09:50:40 | 1 | 1 | 0 | 3 | 1 | 2 | 2 | 3 |
| 33ca23b 11:57:04 | 09:57:04 | 1 | 1 | 0 | 3 | 1 | 2 | 2 | 3 |

**INTERPRETATION.** The counts that never fall to zero are the ones that matter: `25% Twitter`,
`"more than half"`, and `genuinely new capability` all survive into the final report because the
correction text itself quotes the withdrawn wording. Distinguishing "claim present" from
"withdrawal recorded" required reading the surrounding lines — see §C4 and §C2, where the *body*
still asserts what the *correction paragraph* withdraws.

---

## C1 — "Rumour is often self-correcting" (WITHDRAWN; correction is clean)

### Origin
**OBSERVATION.** The root agent (d0, no label) writes the claim into the report draft at
**seq 1009, 09:20:52Z** (`session-92c9e38d`, assistant message):

> "Modern work (DiFonzo & Bordia) adds that rumour is a sense-making activity, that it is often
> *self-correcting*, and that it thrives when official information is absent or distrusted."

It is written to disk by the same step's tool call (seq 1010). A second instance goes into
§5.1: "…and frequently self-correct once authoritative information arrives" (seq 1179), and a third
into the §3 concept table: "| Rumour theory | Allport & Postman | Emergent, self-correcting | **High** |"
(seq 1062/1063).

**OBSERVATION — was it inherited?** No. The commissioning user message (seq 886, 09:17:39Z) never
mentions self-correction of rumour. It *does* prime the opposite suspicion ("Treat this as a hypothesis
to test"), but the specific claim is the parent's own. It was, however, **seeded into the child briefs
by the parent**: the plan at seq 902 (09:18:48Z) asks for "community self-correction on platforms
(Community Notes/X, Wikipedia), and evidence that crowds sometimes correct rather than amplify. Also
research on how rumour self-terminates", and the brief delivered to d2 `1e0ef8e5-13a`
("Research rumour risk amplification theory") at seq 3/8 says "Kate Starbird's crisis-informatics work
on rumour and *'self-correcting'* crowds".

**OBSERVATION — a feedback loop.** At **seq 1039, 09:22:49Z** the parent reads back the child's
`amplification/findings/01-concepts.md`, lines 101–102 of which state:

> "Nicholas DiFonzo & Prashant Bordia, *Rumor Psychology* (2007), and Kate Starbird's crisis-informatics
> work (e.g. the 2013 Boston Marathon study) add that rumour is frequently **self-correcting** when
> authoritative information arrives."

The parent then treats this as corroboration ("Starbird's self-correction: rumour is frequently
self-correcting when authoritative information arrives", seq 1178, 09:27:17Z) and re-uses it in §11
(seq 1179). **INTERPRETATION.** The child had absorbed the parent's framing and returned it with a
prestigious citation attached; the parent then cited the child. The error was laundered, not merely
repeated — and the citation attached (Starbird) is the very author whose data refute it.

### Contradictory evidence
**OBSERVATION.** d2 `1e0ef8e5-13a` retrieves the Starbird iConference 2014 paper and reads, at
**seq 176, 09:23:42Z**:

> "…currently there are no such tools, and the notion of the self-correcting crowd may be overly
> optimistic."

and at **seq 183, 09:23:52Z**: "…tweets were corrections, resulting in a misinformation to correction
ratio of over **44:1**." Its next assistant message (seq 188) records: "misinformation to correction
ratio 44:1, 18:1, 5:1. Conclusion section titled 'Re-evaluating the Idea of the Self-Correcting Crowd'."

### Challenge and trigger
**OBSERVATION.** The contradiction does **not** reach the parent when found. It sat in d2's context
for 16m30s. It finally arrives as a relayed inter-agent message at **seq 1663, 09:40:22Z**, in
`agent/inbox/spliced` (target `next-step`), from d1 `6f182957-758` ("Concept genealogy and fit"):

> "CORRECTIONS APPLIED (important if the parent study cites these): … Rumour is NOT reliably
> self-correcting. Starbird's Boston data show misinformation:correction ratios as high as 44:1;
> the 'self-correcting crowd' is 'overly optimistic.' I softened the brief accordingly."

**OBSERVATION.** The parent's reaction is immediate and self-implicating (**seq 1671, 09:40:22Z**):

> "**I cited 'rumour is frequently self-correcting' in my report!** Let me check — in §3.2 I wrote
> about rumour theory: 'Modern work (DiFonzo & Bordia) adds that rumour is a sense-making activity,
> that it is often *self-correcting*…'"

### Revision
**OBSERVATION.** At **seq 1676/1677, 09:40:36Z** the parent replaces the clause, deletes both
secondary instances, and inserts the withdrawal paragraph (report line 168):

> "**One popular claim about rumour must be withdrawn.** This report initially repeated the common
> assertion that rumour is 'often self-correcting.' **The best evidence contradicts it.** … correction:
> claim ratios as high as 44:1 … and the 'self-correcting crowd' is, in that literature's own
> assessment, **'overly optimistic.'**"

**OBSERVATION.** At seq 1681/1682 the parent also rewrites the §3 table row to
"Emergent; **self-correction is a myth** (correction:claim ratios up to 44:1)". The correction is
committed with the message text at seq 1736–1737, and reported to the user at seq 1752.

### Disposition and metrics
**OBSERVATION.** Clean. Final report line 168 (withdrawal), line 226 (corrected table row). No residual
"self-correcting" assertion about rumour survives.

**DERIVED RESULT.** Time in the artefact before correction: **09:20:52 → 09:40:36 = 19m 44s (1,184 s)**.
Contradictory evidence available before correction: **16m 44s (1,004 s)**.
Agent work inside that window: **5,870 `step/start` events across 106 sessions**.
String propagation: `count_sessions.py 'self-correct'` → **15 sessions / 131 events** (root 32, d1 `6f182957` 37,
d2 `1e0ef8e5` 24, d1 `b0f0ef6b` 17, plus 11 others). Most of these are the phrase in general
discussion; the *asserted-about-rumour* form is confined to root, `1e0ef8e5`, `6f182957`, `b0f0ef6b`.

**Direction of error: overstating resilience / understating threat** — it was a "false comfort" that
made the threat case weaker. The parent says so explicitly ("it removes a false comfort from earlier drafts").

**Detected by depth.** Evidence found at **depth 2**; relayed by depth 1; acted on by depth 0.

---

## C2 — "Synthetic corroboration is the genuinely new capability" (WITHDRAWN in text, NOT in the body)

### Origin
**OBSERVATION.** The category comes from the user (`seq 886`): "3. Synthetic corroboration — Multiple
apparently independent accounts or interpretations generated or coordinated artificially." The
*evaluative claim* is the parent's. First appearance of "genuinely new capability" in the corpus:
root, **seq 1009, 09:20:52Z** — the §4.2 category table, verbatim:
"Category 3 — Synthetic corroboration. … *Agentic relevance:* **highest of all**, and the clearest
qualitative change. Historically expensive and detectable; now cheap. … *Verdict:* **the genuinely
new capability.**" (this is the text that survives at report line 276/278). Then the §5.3 heading at
**seq 1027, 09:22:24Z**:

> "- *Verdict:* **the genuinely new capability.**"   (report line 278, survives to the final report)

and the §5.3 heading, same step:

> "### 5.3 Synthetic corroboration — the genuinely new capability (L2–L3)"   (report line 487, survives)

and a §12.2 bullet at seq 1392 (09:29:44Z): "**Synthetic corroboration is the genuinely new
capability.** Presenting one ambiguous event as many apparently independent observations attacks the
**independence assumption** on which all verification depends. This is a change in kind, not degree."

**OBSERVATION — was it inherited?** Partly systemic. The user prompt supplied category 3 and asked
"whether AI agents change this threat *qualitatively* rather than merely increasing posting volume",
which primes a "new capability" answer. The specific verdict is the parent's.

### Propagation
**OBSERVATION.** The parent's *in-progress report* was read by at least one subagent, which then
reproduced the framing. `31ca772b-cb1` (d2, "Personas and influence-for-hire") reads the report file at
**seq 210/215, 09:22:42–43Z** — the tool result contains "### 5.3 Synthetic corroboration — the
genuinely new capability (L2–L3)" and the "more than half" bullet verbatim. Independently, d1
`f54b15a3-b0a` writes the same phrase into its own deliverable `amplification/findings/04-agentic-capability.md`
§3.7 at **seq 251/252, 09:23:59Z**: "**This is where the genuinely new capability sits**, and it does
not require deepfakes."

**DERIVED RESULT.** `count_sessions.py 'genuinely new capability'` → **5 sessions / 42 events**
(root 20, `f54b15a3` 17, `31ca772b` 3, `6f182957` 1, `46b82e74` 1). Narrow in *session* terms but it
reached both independent authoring branches (concept-fit and capability) and the persona strand.

### Contradictory evidence and challenge
**OBSERVATION.** The challenge is a **depth-3 leaf**. `fc1be9de-04b` (d3, "Detection and belief
studies", parent `31ca772b-cb1` d2) reports at **seq 609, 09:33:57Z** (received by `31ca772b`):

> "5. MULTI-SOURCE ('synthetic corroboration') — DEFLATIONARY. Foster et al. 2012 *Acta Psychologica*
> (10.1016/j.actpsy.2011.12.004): 'Repetition, NOT number of sources, increases both susceptibility to
> misinformation and confidence.' Roggeveen & Johar 2002 … familiarity, NOT perceived source
> variability, is the mechanism. I found NO peer-reviewed study showing a large 'N fake sources > 1 fake
> source' belief multiplier."

Also in the same relay: "HUMAN DEEPFAKE DETECTION = CHANCE. Diel et al. 2024 … 56 papers, 86,155
participants … Pooled: 55.54% [48.87–62.10]" and a "CORRECTIONS TO THE TASK BRIEF" block listing
"A 'All the News That's Fit to Print?' … COULD NOT VERIFY IT EXISTS", the Simchon/Edwards/Lewandowski
misattribution, the Vaccari & Chadwick venue error, and "Bai et al. … is PREPRINT ONLY".

**OBSERVATION — the trigger reaching the parent.** d1 `b61859d5-9ab` ("Computational propaganda
evidence") consolidates and relays at **seq 1527, 09:36:41Z**:

> "*** 1. THE PARENT'S MULTI-SOURCE HYPOTHESIS IS CONTRADICTED, NOT MERELY UNPROVEN. *** This is the
> single most decision-relevant finding. The best direct test — Foster, Huthwaite, Yesberg, Garry &
> Loftus, *Acta Psychologica* 2012 … is titled 'Repetition, not number of sources, increases both
> susceptibility to misinformation and confidence': a NULL for the mechanism."

### Revision
**OBSERVATION.** The parent reacts at **seq 1535, 09:36:52Z** ("**This is a major correction to my
report.** I framed synthetic corroboration as 'the genuinely new capability' and said the strong form
was 'untested'…") and writes the §5.3 correction paragraph (report lines 505–521), plus a §7.5
withdrawal at seq 1540/1541 (report line 764) and the §12.2 bullet replacement at seq 1545/1546.

### Disposition — INCOMPLETE
**OBSERVATION.** Three assertions of the withdrawn framing survive verbatim in the final report:

- line **276**: "*Agentic relevance:* **highest of all**, and the clearest qualitative change."
- line **278**: "*Verdict:* **the genuinely new capability.**"
- line **487**: "### 5.3 Synthetic corroboration — the genuinely new capability (L2–L3)"

and line **489** still reads "this is where the qualitative change is clearest". The correction
paragraph at 507 says the opposite ("A direct literature check does not support that framing"), and
line 764 says "That is wrong". There is no cross-reference from 278/487 to 507/764.

**DERIVED RESULT.** `grep -n "the genuinely new capability\|clearest qualitative change" amplification/Agentic-Threat-Amplification-2026.md`
returns 3 lines (276, 278, 487) asserting the claim *after* the withdrawal. The §12.2 bullet *was*
correctly replaced — so the correction was applied to the derived claims but not to the primary ones.

**DERIVED RESULT.** Time-to-correction (first assertion → first correction paragraph):
**09:20:52 → 09:36:52 = 16m 00s (960 s)**; agent work in window: **5,473 steps / 104 sessions**.
Using the §5.3 heading as origin (09:22:24 → 09:36:52): 14m 28s, 4,735 steps.

**Direction: overstating threat** (a "genuinely new capability" is a stronger threat claim than a
trust-laundering/ citation-layer effect).

**Detected by depth: 3** (leaf). Relay chain depth 3 → 2 → 1 → 0 took **09:33:57 → 09:36:41 = 2m 44s**.
**INTERPRETATION.** This is the strongest candidate in the run for "recursive delegation caught a
false claim that a shallower process would have missed": the null came from a leaf that went to the
primary *Acta Psychologica* literature, and both the parent (d0) and the strand leader (d1) had
been asserting the opposite.

### Correction revised again
**OBSERVATION.** The "contradicted" verdict was itself later softened. The parent adds (report §5.3,
line 521): "Until it is read, the honest position is that the mechanism is **contradicted by the best
available direct test and not yet settled**", and at seq 1619 (09:39:03Z) folds in a 2026 *Cognitive
Science* study (N = 1,015) finding dependent and independent consensus "persuade equally at low
exposure, but independent corroboration yields higher asymptotic belief as exposure accumulates".
**INTERPRETATION.** The Foster null is not wrong, but the parent's first use of it ("the mechanism is
contradicted") overstated the settledness; it was revised within the same session to a probability
statement. This is a *second-order* correction — a correction that was itself corrected.

---

## C3 — Salvi et al. +81.2% → +48.7% (CORRECTED; clean)

### Origin — independently retrieved from the primary abstract
**OBSERVATION.** The figure is **not** inherited and **not** from a secondary source. d1
`f54b15a3-b0a` ("Agentic AI capability evidence") retrieves the published abstract at
**seq 59, 09:19:40Z**:

> "…GPT-4 with personalization was more persuasive 64.4% of the time (81.2% relative increase in odds
> of higher post-debate agreement; 95% confidence interval [+26.0%, +160.7%], P < 0.01; N = 900)."

Independently, d3 `4d64b50a-7a7` ("Persuasion effects literature") retrieves the same text at
**seq 119, 09:22:37Z**. The parent picked it up by reading `amplification/findings/04-agentic-capability.md`
§3.1 at **seq 1117/1118, 09:24:33Z** and wrote it into the report at **seq 1122, 09:24:34Z**:

> "**Salvi et al. (2025), *Nature Human Behaviour*** — preregistered, N = 900. GPT-4 **with basic
> sociodemographic personalisation** was more persuasive 64.4% of the time, an **81.2% relative
> increase in the odds**… *The confidence interval spans an order of magnitude — this establishes
> direction, not magnitude.*"

**OBSERVATION.** The parent flagged uncertainty about **precision**, not about **validity** ("huge CI").
The error is therefore *publication of a superseded primary result*, not a fabrication.

### Contradictory evidence
**OBSERVATION.** d3 `8af84e58-43f` ("Research stream C AI persuasion", parent `61b1e41b-32e` d2) writes
the correction into `amplification/notes/stream-c-ai-persuasion.md` by **09:27:11Z** (first `48.7%`
event). The file's §2 records the arXiv ID correction (2403.14380, not 2410.12743), N=900 not 820, and
then: "CRITICAL: a 3 Sep 2026 Author Correction (10.1038/s41562-026-02588-0) fixes a calculation error
— personalized vs NON-personalized GPT-4 is now **+48.7%, 95% CI [-2.9%, +127.6%], P=0.068 (n.s.)**.
The paper now says it 'cannot conclusively establish… that personalization confers an additional
advantage.'"

### A warning the parent did not act on
**OBSERVATION.** At **seq 1415, 09:34:05Z** d1 `f54b15a3-b0a` relays to the parent:

> "- Salvi 2025 (Nat Hum Behav, N=900): personalised GPT-4 +81.2% odds … ⚠️ An AUTHOR CORRECTION was
> issued 3 Sep 2026 whose content I could not retrieve — treat the headline figures as provisional."

**OBSERVATION.** The parent read this and did not change the figure (its next Salvi action is at
09:43:24Z). **DERIVED RESULT.** Warning → fix latency: **09:34:05 → 09:43:24 = 9m 19s**, during which
≈3,000 `step/start` events occurred (window.py over 1790328845751→1790329404102 minus the earlier span).

### Challenge, relay and revision
**OBSERVATION.** `61b1e41b-32e` (d2, "Effectiveness evidence") reads the stream-C file at
**seq 371, 09:28:45Z** and comments (seq 374): "Stream C is excellent and contains a critical
finding: the **Author Correction (3 Sep 2026)** to Salvi et al., which reduced the personalization
effect to non-significance … This is a major update that changes my draft's headline." It relays
upward at seq 379, 09:28:50Z. d1 `b61859d5-9ab` consolidates and delivers to the parent at
**seq 1792, 09:43:13Z**: "**AI-persuasion evidence deflated further.** Salvi et al.'s personalisation
headline was **corrected on 3 Sep 2026**: personalised-vs-non-personalised is now +48.7% …
effectively retired."

**OBSERVATION.** The parent reacts at **seq 1798, 09:43:15Z** ("**I cited the '+81.2% odds' figure in
my report!** I need to update it…") and edits at **seq 1805, 09:43:24Z** (report line 615), adding
"*(This report cited the uncorrected figure in an earlier draft; it is replaced here.)*" and echoing
it in §9 at seq 1810 (report line 915).

### Disposition and metrics
**OBSERVATION.** Clean: both final Salvi passages cite the corrected figure and the correction date.
No surviving 81.2% assertion.

**DERIVED RESULT.** `count_sessions.py '81\.2%'` → **10 sessions / 148 events**, spanning all four depths:
`f54b15a3`(d1) 42, `8af84e58`(d3) 12, `4d64b50a`(d3) 9, root 14, `61b1e41b`(d2) 24, `500069eb`(d2) 14,
`1ece4a27`(d3) 8, `b61859d5`(d1) 6, `edb0f8d3`(d2) 15, `6f182957`(d1) 4.
`count_sessions.py '48\.7%'` → only **4 sessions**, all on the correction path.
Time in artefact: **09:24:34 → 09:43:24 = 18m 50s (1,130 s)**; agent work in window **4,213 steps / 104 sessions**.
Evidence-to-fix latency: **09:27:11 → 09:43:24 = 16m 13s**.
Relay traversal depth-3 → depth-0: **09:27:11 → 09:43:13 = 16m 02s**.

**Direction: overstating threat** (a significant personalisation effect is a stronger threat than a
null).
**Detected by depth: 3** (leaf `8af84e58`), relayed 3 → 2 → 1 → 0.

**INTERPRETATION.** The propagation count (10 sessions, ~148 events) makes this the most widely
carried erroneous number in the run. But the *substantive* carriers are five sessions (both authoring
branches and the root); the rest are downstream files quoting the same line.

---

## C4 — "Indistinguishable in more than half of evaluated instances" (PARTIAL: recorded as withdrawn, still asserted in the body)

### Origin
**OBSERVATION.** The claim is a **secondary-source paraphrase of an unnamed study**. The raw capture
is `amplification/sources/29e2380bc6438bee86ae28c82a475f18.txt` (The Regulatory Review, "The
Regulatory Vacuum in AI-Amplified Influence Operations"). d2 `edb0f8d3-0c0` reads it at
**seq 39, 09:19:43Z**; the parent reads the same file at **seq 993, 09:20:03Z**:

> "A Frontiers in Artificial Intelligence study documents that AI-generated election disinformation is
> now indistinguishable from authentic human-written journalism in more than half of evaluated
> instances—meaning that the tools platforms and researchers built to flag synthetic content are
> increasingly inadequate."

**OBSERVATION.** The parent flags it as unverified *in the same minute* (seq 996, 09:20:09Z):
"*(flag: need verification)*" and "Note: some of these claims (25% of Twitter activity, the Frontiers
study) I should treat with caution."
**OBSERVATION — origin cannot be traced further.** `grepcorpus 'Frontiers in Artificial Intelligence'`
returns only the two reads of the secondary source and one unrelated 2026 PRISMA review. No session
ever retrieved the underlying study or resolved its identity. The file's own creation event is **not
present in the logs**: no tool call in any of the 153 sessions constructs that hashed filename, so
the immediate provenance of the capture is unknown.

### Propagation
**OBSERVATION.** It is written into the report §5.3 at **seq 1028, 09:22:24Z** (report line 495) with
the caution retained, and reproduced by subagents that read the parent's draft:
`31ca772b-cb1` at seq 215 (09:22:43Z), `b61859d5-9ab` at seq 802/806.

**DERIVED RESULT.** `count_sessions.py 'more than half of (evaluated )?instances|indistinguishable from authentic human'`
→ **4 sessions / 17 events**. Very narrow because it was never generalised.

### Contradiction and trigger
**OBSERVATION.** Two independent agents failed to verify it and proposed a replacement:
- d3 `fc1be9de-04b` (seq 609, 09:33:57Z) supplied Diel et al. 2024 (56 papers, 86,155 participants, pooled 55.54%).
- d2 `31ca772b-cb1` (seq 637, 09:41:49Z): "'AI-generated election disinformation is now indistinguishable
  from authentic human-written journalism in more than half of evaluated instances' — you already
  flagged this as needing verification. **I could not verify it either.** The defensible, verified
  substitute is Diel et al. 2024…"

**OBSERVATION.** d1 `b61859d5-9ab` delivers the instruction at **seq 1527, 09:36:41Z**:
"…use this peer-reviewed figure instead of the unverifiable 'more than half indistinguishable' claim."

### Revision
**OBSERVATION.** The parent applies the replacement at **seq 1545/1546, 09:36:52Z** — but the edit
targets the §12.2 bullet, not report line 495. The new text: "*(This replaces an earlier, unverifiable
'more than half indistinguishable' claim in this report.)*" It then updates Appendix C at
**seq 1570, 09:37:26Z** (report line 1374):

> "Two figures from early secondary sources have been withdrawn or bounded during the study — an
> 'indistinguishable in more than half of instances' synthetic-content claim (now replaced by the
> peer-reviewed pooled detection figure of **55.5%**, 56 papers, 86,155 participants)… Their removal is
> recorded rather than silently edited, because the direction of both errors was **toward overstating
> the threat**."

### Disposition — INCOMPLETE
**OBSERVATION.** The withdrawn claim is **still asserted in the body** of the final report at line 495:

> "Research cited in the governance literature reports that **AI-generated election disinformation is
> now indistinguishable from authentic human-written journalism in more than half of evaluated
> instances**. *(Caution: this figure comes from a single study via a secondary source and requires
> verification…)*"

Only the caution distinguishes it from the original. The 55.5% figure appears in §6.8 (line 670) as
the human *detection-accuracy* pooled estimate — a **different quantity** (accuracy of human
judgements) from the original (proportion of AI outputs judged indistinguishable). The substitution is
therefore not like-for-like.

**DERIVED RESULT.** Time from report insertion (09:22:24) to recorded withdrawal (09:37:26):
**15m 02s**. Agent work in window (09:20:03 → 09:36:52): **6,045 steps / 104 sessions**.
**Direction: overstating threat.** Declared as such by the report itself.
**Detected by depth: 3** (leaf `fc1be9de`), corroborated at depth 2.

**INTERPRETATION.** This is a correction that is *narratively* complete and *textually* incomplete.
The Appendix C entry, the commit message, and §5.3's neighbouring paragraph all assert the claim was
withdrawn, while the claim remains readable in §5.3. A reader who trusts the register over the text
would be misled about the report's own contents.

---

## C5 — "~25% of Twitter activity is bot-driven" (never used; recorded as withdrawn)

**OBSERVATION.** Same origin as C4: the Regulatory Review capture, read at **seq 993, 09:20:03Z**
("bot-driven amplification accounts for roughly 25 percent of Twitter activity"). The parent records
in its own notes at seq 996: "the '25% of Twitter activity is bots' figure is a much-disputed claim.
Let me flag that."

**OBSERVATION.** It is written into the report **only as a limitation**, at **seq 1178, 09:27:17Z**
(the §6.10 / Appendix C draft):

> "5. **Some figures are held loosely:** the 'indistinguishable in more than half of instances'
> synthetic-content figure and the '25% of Twitter activity is bot-driven' figure both come through
> secondary sources and are contested in the literature."

**DERIVED RESULT.** `git show b0847b0:… | grep -n "25% of Twitter"` → exactly one hit, at the
Appendix C line. `grep '25% of Twitter'` on the final report → one hit (line 1374). `count_sessions '25 percent of Twitter|25% of Twitter'`
→ **2 sessions / 10 events** (root 9, `edb0f8d3` 1).

**INTERPRETATION.** This is the clearest case in the run of a "correction" that is really a
*withholding*. The figure never reached an argued claim, yet Appendix C describes it as one of "two
figures … withdrawn or bounded during the study". The register slightly overstates the epistemic work
done: no evidence was gathered against the 25% figure either way; it was simply not used. **Direction
of the avoided error: overstating threat.** **Detected at depth 0**, before propagation.

---

## C6 — Doctrine correction 1: "perception management" is not current US DoD doctrine

### Origin — SYSTEMIC (user prompt)
**OBSERVATION.** The term is named in the commissioning message itself (seq 886, 09:17:39Z):
"Investigate relevant existing concepts including cognitive warfare, reflexive control, **perception
management**, information operations…". The parent repeats it in its plan (seq 902) and in the brief to
d2 `51fc805d-928` (seq 3/8, "A) PERCEPTION MANAGEMENT (US DoD definition and history) … **Is it still
a defined term?**").

**DERIVED RESULT — is it inherited?** Yes, at the level of *the concept being on the list*, which is a
systemic property of the run: every child brief that touched doctrine inherited the term. The erroneous
*assertion* — that it fits as live doctrine — was the parent's synthesis in §3.1.

### Contradictory evidence
**OBSERVATION.** d2 `51fc805d-928` finds the gap at **seq 66, 09:20:54Z**: "Big finding: The November
2021 DoD Dictionary does NOT define 'perception management.' … So perception management is no longer a
defined term (at least as of Nov 2021). I need to verify the current (2024/2025) dictionary too."
Its d3 child `5be694c4` ("2025 Hegseth MISO language shift") pursues the current-dictionary check.

### Trigger and revision
**OBSERVATION.** The consolidated correction reaches the parent at **seq 1921, 09:50:18Z**:
"…'PERCEPTION MANAGEMENT' IS **NOT A CURRENT DoD TERM**. My earlier draft implied it was. The last
dictionary text is JCS Pub 1-02 (1 Dec 1989); it was DROPPED in the 8 Nov 2010 reissue and appears in
neither the Nov 2021, Sep 2024 nor Jun 2025 DoD Dictionaries. Rating changed from Partial to POOR."

**OBSERVATION.** The parent edits at **seq 1936, 09:50:32Z** (report lines 141 and 224), replacing the
fit rating and adding the correction paragraph, and commits at seq 1946 with a message that names the
error explicitly.

### Disposition and metrics
**OBSERVATION.** Clean: report line 141 ("It therefore fits poorly, and this report does not rely on
it") and line 224 ("US doctrine, **retired 2010** … **not a current term — do not cite as one**").
**DERIVED RESULT.** User prompt → correction: **32m 53s**. First subagent evidence (09:20:54) →
correction: **29m 38s**. **Direction: overstating threat** (a live doctrinal concept implies state
capability behind the mechanism). **Detected by depth 2**, verified by depth 3.

---

## C7 — Doctrine correction 2: the PSYOP/MISO renaming is reported backwards

**OBSERVATION.** The premise is again in the subagent brief, not the user prompt: d2 `51fc805d-928`'s
brief at seq 3/8 asks about "the recent shift in language (the US military's move away from
'influence'/'MISO' language c. 2025 under Secretary Hegseth — **verify this if it happened**)".
**OBSERVATION.** The correction is delivered together with C6 at **seq 1921, 09:50:18Z**:
"2. THE '2025 MISO RENAME' PREMISE WAS INVERTED. Hegseth's 2 Dec 2025 memo renamed MISO BACK TO PSYOP
— not MISO to 'information operations'. … the US Army had already reverted its unit names to PSYOP in
October 2017 while keeping MISO as the function … JP 3-13's successor is JP 3-04 'Information in Joint
Operations' (14 Sept 2022)."
**OBSERVATION.** Applied at seq 1936/1941 (report lines 142, 223).
**DERIVED RESULT.** Same timing as C6: 32m 53s from user prompt. **Direction: overstating threat**
(implying a live, recent doctrinal escalation). **Detected by depth 2/3.**

**INTERPRETATION.** C6 and C7 are a matched pair: two *concept-fit* errors that entered through the
concept list the parent was told to audit. Both were caught because the audit task explicitly asked
"is it still a term / did it happen". **Counterfactual: a run that had not been asked to verify the
lineage would have carried both.** Here the audit instruction is what produced detection, not the
delegation depth.

---

## C8 — "Make the enemy defeat himself" is not a Liddell Hart quotation (never reached the report)

### Origin and propagation
**OBSERVATION.** d1 `6f182957-758` writes the misattribution into the brief it sends to d2
`a4a04330-c73` at **seq 35, 09:19:36Z**:

> "…Basil Liddell Hart's 'indirect approach' (Strategy, 1954) and **his explicit claim that the 'best
> strategy is to make the enemy defeat himself'** / 'dislocate the enemy's equilibrium' — GET THE EXACT
> LIDDELL HART QUOTE AND PAGE/CHAPTER if reachable."

`a4a04330` (d2) passes it verbatim to d3 `6d105fdb-03f` ("Military strategic prior art") at seq 3/8.
`6f182957` then asserts it as verified in its own working table at **seq 219, 09:22:09Z**:
"| *Strategy* (1954/1967) | Yes — 'make the enemy defeat himself'; disrupt his equilibrium *before* the
main attack | **Yes** |".

### Challenge
**OBSERVATION.** The **depth-3 leaf** `6d105fdb` downloads the 1929 full text and runs full-text
searches (seq 50/51: `grep -n -i "defeat himself\|equilibrium\|dislocation"`). It reports back to
`6f182957`, which relays to the parent at **seq 1663, 09:40:22Z**:

> "'Make the enemy defeat himself' is NOT verbatim Liddell Hart. **Internet Archive full-text search
> returns zero hits**; his wording is about dislocating the enemy's psychological and physical balance.
> I removed the quotation marks and attribute it to Clausewitz's actual 'by his own efforts' instead."

### Disposition
**OBSERVATION.** The parent checks at seq 1671: "'Make the enemy defeat himself' is NOT verbatim
Liddell Hart — removed. **I don't think I cited it.**"
**DERIVED RESULT.** `grep -i "liddell"` on both final reports → **zero hits**. The misattribution never
entered either artefact; the report instead uses Clausewitz (On War VI.vii, "or by his own efforts").
**Direction: overstating the lineage's precision** (a fabricated verbatim quotation lends false
authority). **Detected by depth 3.**

**INTERPRETATION.** This is a clean demonstration of recursive-delegation value: the error was
*created* at depth 1, transmitted through depth 2 to depth 3, and falsified at depth 3 by a
primary-source full-text search that neither the parent nor the depth-1 author performed. Had the
brief not been executed by a leaf with download capability, the false quotation would have been
available to the report and only "I don't think I cited it" prevented publication.

---

## C9 — Rid's active-measures periodisation: four waves, not five

**OBSERVATION.** The number is again **hypothesised in the brief**: d1 `6f182957` → d2 `414abba5-945`
("Research active measures hybrid warfare"), seq 3/8 (09:19:36Z): "Rid's periodisation (**five
waves?**)."
**OBSERVATION.** d2 `414abba5` resolves it at **seq 86, 09:21:06Z**: "Good progress. Rid's
periodisation: **FOUR waves** (per p.6 quote). Note the task hypothesised 'five waves' — I should flag
that the book says four big waves, one generation apart."
**OBSERVATION.** Relayed to the parent at seq 1663 (09:40:22Z) and again at seq 1960 (09:50:18Z);
parent's response at seq 1965 (09:50:32Z): "Rid's four waves — **I don't specify a number**."
**DERIVED RESULT.** `grep -i "four waves\|five waves"` on the final report → no numeric claim. **No
report change was required.** **Detected by depth 2.**

---

## C10 — A cluster of "brief-premise" citation corrections (mostly pre-empted)

**OBSERVATION.** Several erroneous premises lived in the *briefs the parent wrote*, were refuted by
leaves, and never reached the artefacts. All are quoted from the relay at seq 1663 (09:40:22Z) or
seq 1527 (09:36:41Z):

| Premise (in brief) | Who refuted it | Refutation | Reached the report? |
|---|---|---|---|
| Krepinevich, "The Origins of Offset Strategy" | d3 `6d105fdb` | "likely non-existent as a titled CSBA report" (seq 1663) | No — `grep -i krepinevich` = 0 |
| Lefebvre, "What is Reflexive Control?" | d1/d3 | "confirmed non-existent" (seq 1999) | No |
| Chotikul ADA152240/1985 | d1/d3 | flagged, not cited (seq 1960) | No (`grep ADA152240` = 0) |
| "Gerasimov Doctrine" as real | d2 `414abba5` | Galeotti: Western misnomer | No (`grep` = 0) |
| "firehose of falsehood" = RR-1406 with seven features | d1 `b61859d5` | "is PE-198 with FOUR features, not RR-1406 with seven" (seq 1921) | No (`grep firehose` = 0) |
| "All the News That's Fit to Print?" (Clark et al. 2023) | d3 `fc1be9de` | "COULD NOT VERIFY IT EXISTS … Do NOT cite" (seq 609) | No |
| Simchon/Edwards/Lewandowski as a *Nature Comms* liar's-dividend paper | d3 `fc1be9de` | "NOT SUPPORTED"; their paper is on microtargeting | No |
| Vaccari & Chadwick in *HKS Misinformation Review* | d3 `fc1be9de` | actually *Social Media + Society* | No |
| Bai et al. "AI Can Persuade Humans on Political Issues" as published | d3 `fc1be9de` | "PREPRINT ONLY … grade D, widely miscited as published" | No |
| Salvi arXiv ID 2410.12743 | d3 `8af84e58` | correct ID is 2403.14380 (2410.12743 is a physics paper) | Yes, corrected in the notes that fed the report |
| Costello/Pennycook/Rand "gamified psychological inoculation" | d3 `8af84e58` | NOT VERIFIED (seq 374) | No |
| "Durability of the accuracy nudge" (Nat Comms 2024) | d3 `8af84e58` | NOT VERIFIED (seq 374) | No |

**DERIVED RESULT.** `grep -c` on the final report for `Krepinevich`, `ADA152240`, `firehose`,
`Gerasimov Doctrine`, `Liddell` → **0 each** (parent's own verification command at seq 1980–1987;
the log shows the counts blank/0 and the git commit at 09:54:44 as the confirmation).

**INTERPRETATION.** This cluster is *structurally different* from C1–C4. These are errors in the
**research briefs**, not in the artefacts. They show the delegation architecture behaving as a
falsification layer: 91 depth-3 leaves with retrieval tools acted as a filter on the parent's and
depth-1's assumptions. It is also, however, evidence that the parent authored a substantial number of
unverified premises into briefs — a systemic property, not a branch accident.

---

## C11 — Copenhagen police quotation "we were not clear enough with our reservations" (REMOVED)

**Origin.** **OBSERVATION.** The quotation enters via a subagent report at **seq 545, 08:32:04Z**
(+10.9 min into the run, ~46 min before the amplification strand begins) and is written into the
autonomy report around **seq 572, 08:32:32Z**. It was inherited by a later brief: the
parent's amplification plan at seq 902 asks for "the "capability" framing retracted".
**Challenge.** **OBSERVATION.** d1 `f5d926fb-1c4e` ("Drone sighting ambiguity cases") flags it in
`amplification/findings/drone-cases-amplification-retractions.md`, which the parent reads at
**seq 1163, 09:28:57Z**: "**The specific quote 'we were not clear enough with our reservations' is
[NV]** — it appears in the existing research file but is not in the Reuters wire or any source I
reached."
**Trigger.** **OBSERVATION.** The consolidated flag arrives at **seq 1638, 09:39:56Z**
("3. Unverified, do not cite: the 'we were not clear enough…' quote (not traceable to any primary
source)").
**Revision.** **OBSERVATION.** The parent edits at **seq 1658/1659, 09:40:19Z** (autonomy report
line 236): "*(An earlier draft of this report quoted police as conceding they 'were not clear enough
with our reservations'. **That quotation has been removed** — it could not be traced to any primary
source across repeated checks…)*"
**DERIVED RESULT.** Artefact presence: written 08:32:32Z, removed 09:40:19Z = **67m 47s**. **Direction:
overstating institutional self-criticism / adding unearned credibility to the retraction narrative.**
**Detected by depth 1** (its strand file, produced by depth-3 leaves).

---

## C12 — "Überattribution" attributed to the BfV (REMOVED as a quotation)

**OBSERVATION.** The term is asserted from a subagent report at **seq 545, 08:32:04Z**
("**BfV Verfassungsschutzbericht 2025** … warns explicitly against **'Überattribution'**…"), written
into the autonomy report at seq 572 (08:32:32Z), and *re-briefed* into the amplification strand at
seq 902/910 ("the German BfV's warning against 'Überattribution'").
**OBSERVATION.** The removal is recorded at **seq 1847/1848, 09:47:57Z** (autonomy report line 333):
"*(A source note: an earlier draft attributed the specific term '**Überattribution**' to the BfV.
Research strands disagreed on whether that term appears as official BfV language, so it has been
removed as a quotation. The substantive caution … is documented and stands.)*"
**DERIVED RESULT.** Artefact presence: 08:32:32 → 09:47:57 = **75m 25s**. **Direction: overstating the
specificity/authority of the source.** **Detected by depth 2/3** (the strands that disagreed).
**INTERPRETATION.** Unlike C11, this is a *partial* correction: the term is removed as a quotation but
the underlying caution is retained. The parent explicitly reasons about which part survives.

---

## C13 — Bundestag Drucksache 21/7725 "technische Fehlfunktionen" (REMOVED; error later re-used as a caution)

**OBSERVATION.** The claim enters at **seq 545, 08:32:04Z**, is written into the autonomy report at
seq 572 (08:32:32Z) ("a Bundestag paper … classifies comparable 2026 intrusions as 'technische
Fehlfunktionen'"), and is then **re-briefed into the amplification strand as an established fact** at
seq 902 ("the Bundestag finding of 'technische Fehlfunktionen'") and seq 907.
**OBSERVATION.** d3 `f5d926fb`'s strand refutes it (received 09:39:56Z, seq 1638): "The Bundestag
'technische Fehlfunktionen' finding for German airport sightings is NOT VERIFIED and should not be
cited. The phrase is real but refers to UKRAINIAN drones in Finnish/Baltic airspace (Drucksache
21/7725, 25 Aug 2026). A check of 53 Bundestag papers containing 'Drohn' found no such finding about
German airports."
**Revision.** **OBSERVATION.** The parent edits at **seq 1653/1654, 09:40:15Z** (autonomy report
line 335): "**A correction to an earlier draft of this report.** … **That is wrong and has been
removed.** … *(The correction is recorded rather than silently applied, because the withdrawn version
understated the German government's own uncertainty.)*"
**DERIVED RESULT.** Artefact presence: 08:32:32 → 09:40:15 = **67m 43s**. **Direction: UNDERSTATING
threat** — the only understating error found in the run, and the report says so. **Detected by depth
3** (`f5d926fb`'s strand file, produced by leaves).

---

## C14 — German BKA count series (1,072 incidents / 1,955 drones) — caveated, not corrected

**OBSERVATION.** d3 `f5d926fb` flags a cross-strand disagreement at 09:39:56Z: "the BKA's ~165
sabotage / 747 drone / 1,068 drones figures are **2026 year-to-date, not 2025** (2026 runs *below*
2025)".
**OBSERVATION.** The parent's own figure is different again, and it resolves the conflict by
**flagging rather than choosing** (reasoning at seq 1664): "My figure (1,072 incidents/1,955 drones in
2025) is different from the 747/1,068 — so possibly a different metric or a different year. There's
genuine cross-strand disagreement. The honest move: flag the German count series as contested."
The edit (autonomy report line 273) adds: "**The German series should be used cautiously** …
*(Grade A for the existence of a substantial German incident series; grade C for any specific annual
total.)*"
**INTERPRETATION — a correction that is *not* a correction.** The parent did not adjudicate between
two incompatible count series; it downgraded confidence in both. The underlying disagreement is
**orphaned** (see §O4). **Direction: indeterminate.** **Detected at depth 0**, from a depth-3 flag.

---

## C15 — GRU Unit 29155 / Storm-1516 attribution (CORRECTED in the strand file)

**OBSERVATION.** The error is in a **subagent's own file**, not the report. `31ca772b-cb1`'s working
table (read at seq 267) says: "**Storm-1516 / CopyCop** (Russia; VIGINUM imputes GRU unit 29155 with
'very high confidence')".
**OBSERVATION.** Its own verification subagent corrects it (received seq 657): "Attribution to GRU
Unit 29155 is **INFERRED, not proven** — VIGINUM says it cannot confirm." `31ca772b` propagates the
correction at seq 666 ("Attribution to GRU Unit 29155 is INFERRED — VIGINUM states it cannot confirm
it") and d1 `b61859d5-9ab` delivers it to the parent at **seq 1527, 09:36:41Z**: "GRU 29155
attribution corrected. The earlier subagent file implied VIGINUM imputes Storm-1516 to GRU unit 29155.
The primary check shows VIGINUM imputes the OPERATION with 'very high confidence' but does NOT itself
confirm unit 29155."
**OBSERVATION.** Parent at seq 1535: "**GRU 29155 correction**: VIGINUM imputes the operation but does
NOT confirm unit 29155."
**DERIVED RESULT.** `grep -i "29155"` on the final report → **0 hits**. The erroneous form is readable
in the branch file from at least **09:24:49Z** (seq 267) and corrected by **09:35:26Z** (seq 657) —
**10m 37s** inside the branch. **Direction: overstating attribution specificity.** **Detected by
depth 3** (a verification leaf under `31ca772b`).
**INTERPRETATION.** This is an *intra-branch* self-correction: the error never left the branch, because
the branch's own leaf caught it before the d1 consolidation. Useful contrast with C1/C3, where the
branch's leaves caught errors that the parent had already published.

---

## C16 — Doppelganger: criminal indictment vs civil domain seizure (CORRECTED)

**OBSERVATION.** d1 `b61859d5-9ab` at **seq 1792, 09:43:13Z**: "**Doppelganger Sept 2024 fixed.** The
action was a **civil domain seizure** (~32 domains, FBI affidavit) — nobody was criminally charged in
it. The two Russians indicted that day were RT staff in the *separate* Tenet Media case. My earlier
wording conflated them; the table now separates them." Related: "there is **NO verified US federal
indictment** of John Mark Dougan (his 2017 indictment was 21 Florida state charges; the Sept 2024
federal case was against RT staff, Tenet Media)."
**DERIVED RESULT.** These are corrections *within* the d1→d2 branch; the parent was notified but the
final report's treatment was already consistent. **Direction: overstating enforcement severity.**
**Detected by depth 2/3.**

---

## C17 — Unverifiable persona names "Elise", "Vladimir Z.", "Alexei" (NOT CARRIED)

**OBSERVATION.** These names appear **in the subagent brief written by the parent** (`31ca772b-cb1`
seq 3/8, 09:18:50Z: "the fake 'Elise' persona / Doppelganger pseudo-sites"). At **seq 1527,
09:36:41Z** the branch reports: "**DO NOT CARRY FORWARD**: the persona names 'Elise' (Doppelganger) and
'Vladimir Z.'/'Alexei' (Storm-1516) could not be verified to any source grade and appear nowhere in
the brief." Parent at seq 1535: "I don't think I used them."
**DERIVED RESULT.** `grep -i "Elise\|Vladimir Z\|Alexei"` on the final report → **0 hits**.
**INTERPRETATION.** Another brief-premise error that the leaves filtered. Note the parent's own
phrasing ("appear nowhere in the brief") is inaccurate — it wrote them into the brief; the branch
means they appear in no *source*. **Direction: overstating documented detail.** **Detected by depth 3.**

---

## C18 — The "reach is rented" reframe (argument revision, not a factual correction)

**OBSERVATION.** The parent changes its own framing at **seq 1346, 09:32:52Z**: "**reach is rented,
not owned**. This actually strengthens the threat case and **qualifies my §8/§6.9 distribution
argument**", and writes at seq 1352 (report §6.9, line 471): "**The correct interpretation is that
reach is rented from the platform, not owned by the operation.** Forty accounts do not have a billion
impressions; they have a billion impressions *because a recommendation algorithm gave them one*."
The counter-evidence (ISD, relayed through `31ca772b`) arrived at **seq 1341, 09:32:46Z** — so the
reframe followed within **6 seconds**.
**DERIVED RESULT.** `git show` shows the phrase first present in commit `8e6d674` (09:33:42Z), commit
message "integrate reach-renting counterweight and liar's dividend".
**INTERPRETATION.** This is a **revision of an inference, not of a fact**. No number was wrong; the
interpretation of the reach data changed direction, and the parent explicitly says so ("qualifies my
own distribution argument"). It shows the run revising *upward* on threat as well as downward.
**Direction: revision toward a stronger threat claim.**

---

## C19 — The "backfire/boomerang" terminology warning (flagged, NOT acted on)

**OBSERVATION.** d1 `6f182957` relays at seq 1663 (09:40:22Z): "Terminology warning for the parent
study: avoid 'boomerang effect' and 'backfire effect' (in the persuasion literature they mean the
**opposite** — a message failing to persuade — and are largely falsified)."
**OBSERVATION.** The parent at seq 1671: "**I have a §8.5 titled 'The 'backfire…'**". Its response is
to leave the section title and the sentence "**The backfire effect is largely retracted**" in place
(report line 889; §8.5 heading at line 852 area). `grep -i boomerang` → no hits, so half the warning
was moot.
**DERIVED RESULT.** `grep -n "backfire"` on the final report → the term survives as a *section title
and claim*, not as an error, because the parent uses it in the debunked sense and then says it is
debunked.
**INTERPRETATION.** A **rejected correction**. The depth-1 agent's terminology objection was correct
in itself but the parent judged (implicitly) that its own usage was already the corrected one.
Nothing in the log shows the parent explaining that judgement. This is the one correction in the run
that a leaf surfaced and a shallower agent declined to adopt. **Direction: n/a (terminological).**

**OBSERVATION — provenance of the backfire claim itself.** The corrected statement is present from the
parent's *first* outline (seq 887, 09:17:47Z: "the 'backfire effect' literature (mostly debunked)")
and from the brief at seq 902 ("its partial retraction"). So the parent did not have to be corrected
on the substance; the brief asked for it.

---

## C20 — "Stop News" Breakout downgrade (a *source's* correction that the report generalises)

**OBSERVATION.** d2 `8605360c-4c6` retrieves OpenAI's October 2025 report at **seq 585, 09:25:34Z**:
"**OpenAI's 'Stop News' case was rated Category 3 in October 2024 and downgraded to Category 2 in
October 2025** after VIGINUM and open-source researchers established the apparent 'information
partnerships' were **fictional and created by exploiting technical flaws on the partners' own
websites**."
**OBSERVATION.** The parent turns it into a generalised calibration rule at **seq 1792 →
seq 1810** (report line 838): "**And a retraction worth generalising.**"
**INTERPRETATION.** This is not an AI-researcher error being corrected; it is a *sourced retraction
being converted into a methodological rule*. Included because it is the only place in the report where
a correction from the literature is used as evidence about the literature.

---

## Cross-cutting findings

### X1. Errors that propagated widely before correction, and how long they survived

**DERIVED RESULT.** Table of first-artefact-appearance → correction, with agent work in the window
(`window.py`, `step/start` counts) and string propagation (`count_sessions.py`):

| Correction | Error in artefact | Window | Wall-clock | `step/start` events in window | Sessions in window | Sessions containing the claim |
|---|---|---|---|---|---|---|
| C3 Salvi 81.2% | 09:24:34 | → 09:43:24 | **18m 50s** | 4,213 | 104 | **10 / 148 events** |
| C1 self-correcting | 09:20:52 | → 09:40:36 | **19m 44s** | 5,870 | 106 | 15 / 131 events |
| C2 synthetic corroboration | 09:20:52 | → 09:36:52 | **16m 00s** | 5,473 | 104 | 5 / 42 events |
| C4 "more than half" | 09:22:24 | → 09:37:26 | **15m 02s** | 6,045 (from 09:20:03) | 104 | 4 / 17 events |
| C6/C7 doctrine | 09:1x (report draft) | → 09:50:32 | ~33m | — | — | 3 / — |
| C11 Copenhagen quote | ~08:32:32 | → 09:40:19 | **67m 47s** | — | — | — |
| C12 Überattribution | ~08:32:32 | → 09:47:57 | **75m 25s** | — | — | — |
| C13 Drucksache | ~08:32:32 | → 09:40:15 | **67m 43s** | — | — | — |

**INTERPRETATION.** The four amplification-strand errors all survived **15–20 minutes**, during which
between **4,200 and 6,000 agent steps** ran across **~104 concurrent sessions**. "Wall-clock
shortness" is misleading here: the run's concurrency means each error was live while the equivalent of
a large multi-agent project executed. The autonomy-report errors (C11–C13) survived roughly three times
as long because they were created before the amplification strand began and were only revisited when a
*different* strand's leaves happened to look at the same primary sources.

### X2. Corrections that were themselves wrong or later revised again

- **C2 second-order revision (OBSERVATION).** The parent's own correction overstated: "the mechanism is
  contradicted" was revised within the same session to "contradicted by the best available direct test
  and **not yet settled**" (report line 521), with the Pillai & Fazio (2025) item named as the
  adjudicating study. The Foster null was not withdrawn, but its scope was narrowed.
- **C4 substitution is not like-for-like (DERIVED RESULT).** The withdrawn claim was about *the
  proportion of AI-generated content judged indistinguishable*; the replacement (55.5%) is a pooled
  *human detection accuracy*. Both concern the same phenomenon but they are not the same statistic.
  The report presents the replacement as if it directly supersedes the original.
- **C2 body/withdrawal contradiction (OBSERVATION).** Lines 276/278/487/489 still assert what lines
  507/764 withdraw.
- **C4 body/withdrawal contradiction (OBSERVATION).** Line 495 still asserts what line 1374 records as
  withdrawn.
- **C14 non-adjudication (OBSERVATION).** Two incompatible German count series were both downgraded
  rather than reconciled; the disagreement remains open.

### X3. Depth-3 leaf detection that the parent acted on

**DERIVED RESULT.** Of the corrections where the *challenging* agent is identifiable:

| Correction | Challenger | Depth | Relayed through | Parent acted? |
|---|---|---|---|---|
| C2 Foster null (synthetic corroboration) | `fc1be9de-04b` | **3** | 3→2 (`31ca772b`)→1 (`b61859d5`)→0 | **Yes** (09:36:52) |
| C3 Salvi +48.7% | `8af84e58-43f` | **3** | 3→2 (`61b1e41b`)→1 (`b61859d5`)→0 | **Yes** (09:43:24) |
| C4 Diel 55.5% replacement | `fc1be9de-04b` | **3** | same as C2 | **Yes** (09:36:52) |
| C8 Liddell Hart | `6d105fdb-03f` | **3** | 3→2 (`a4a04330`)→1 (`6f182957`)→0 | Yes (avoided) |
| C11 Copenhagen quote | strand of `f5d926fb-1c4e` | 1 (its leaves) | 3→2→1→0 | **Yes** (09:40:19) |
| C13 Drucksache | strand of `f5d926fb` | 1 (its leaves) | 3→2→1→0 | **Yes** (09:40:15) |
| C1 Starbird 44:1 | `1e0ef8e5-13a` | **2** | 2→1 (`6f182957`)→0 | **Yes** (09:40:36) |
| C15 GRU 29155 | verification leaf under `31ca772b` | 3 | caught inside branch | n/a (never escaped) |

**INTERPRETATION.** Recursive delegation did provide detection that the shallower layers did not:
three of the four most consequential corrections (C2, C3, C4) were produced by depth-3 leaves going to
primary literature, and in each case both the depth-0 parent and the depth-1/2 strand leads had been
asserting the opposite. The counterfactual is credible: the parent's and d1's own searches produced
the *errors* (Salvi's published abstract; the "genuinely new capability" framing; the secondary
"more than half" figure), and only the leaves' primary-source checks (Acta Psychologica; the
Nature Human Behaviour author correction; the Diel meta-analysis; the Internet Archive full text)
produced the corrections.

**OBSERVATION — cost of the depth.** The relay chain 3→2→1→0 added measurable latency:
- C2: evidence 09:33:57 → parent 09:36:41 = **2m 44s**.
- C3: evidence 09:27:11 → parent 09:43:13 = **16m 02s** (the long delay is at the d2→d1 hop, where the
  message waited for the strand to finish).
**INTERPRETATION.** Depth bought detection but the *hopping* latency, not the search latency, was the
binding constraint on correction speed. In C3 the correction existed on disk for 16 minutes before the
parent saw it.

### X4. Systemic vs branch errors

**OBSERVATION.** Three error sources are distinguishable:
1. **In the commissioning prompt (systemic to the whole run):** the concept list including "perception
   management" (C6); category 3 "synthetic corroboration" (C2, as a category); the framing question
   "does AI change this threat qualitatively rather than merely increasing posting volume" (which
   licenses "genuinely new capability" verdicts).
2. **In the parent's own briefs to children (systemic to the amplification strand):** "make the enemy
   defeat himself" as a Liddell Hart quotation (C8); "Rid's periodisation (five waves?)" (C9);
   Krepinevich/Lefebvre/Chotikul/"firehose"/persona names (C10, C17); "self-correcting crowds" (C1).
3. **In a leaf's own retrieval (branch-level, not inherited):** the Salvi 81.2% figure (C3) — retrieved
   accurately from the then-current published abstract by two independent leaves.

**INTERPRETATION.** Correction C3 is the only major one that is unambiguously a *branch* error
(a superseded-but-genuine published figure). C1, C6, C8, C9, C10 and C17 are **systemic framing
errors**: the parent wrote the premise into the brief, and the brief is what the leaves executed
against. The delegation architecture caught them *despite* the framing, not because of it — because
the briefs also contained explicit "verify this / is it still a term / get the exact quote"
instructions. **Where a brief asked for verification, the error was caught. Where it asserted, the
error propagated.**

### X5. Corrections that were really withholdings, and errors resolved by dropping a claim

- **C5 (25% of Twitter).** Never used; recorded in Appendix C as a withdrawn/bounded figure.
  No evidence was gathered against it. **(OBSERVATION + INTERPRETATION.)**
- **C14 (German counts).** Both figures downgraded rather than resolved; the report says "the German
  series should be used cautiously". **(OBSERVATION.)**
- **C19 (backfire terminology).** A correction that was deliberately not adopted. **(OBSERVATION.)**
- **C4 line 495.** A claim declared withdrawn in Appendix C but not removed from §5.3. **(OBSERVATION.)**

**INTERPRETATION.** In two cases (C5, and the "not used" half of C4's Appendix C entry) the report's
correction *register* is more complete than the underlying epistemic work: it lists items as
"withdrawn or bounded" that were in fact never asserted, or were asserted and are still there. The
direction-of-error sentence in Appendix C ("the direction of both errors was toward overstating the
threat") is nonetheless correct for the C4 half.

### X6. Orphaned (flagged-but-unresolved) uncertainties

**OBSERVATION.** Explicitly left open in the logs and/or the final reports:

1. **Pillai & Fazio (2025), *JARMAC*, "Repeated by many versus repeated by one."** "APA blocks the
   abstract, so its effect size is unknown … the highest-value five-minute manual read in the whole
   study" (seq 1527, seq 1792); report line 521 names it as the item that "would settle the question".
   **Queried in 5 sessions / 90 events and never resolved.**
2. **The unidentified "Frontiers in Artificial Intelligence study"** behind the "more than half"
   claim (C4). Never traced to a primary source; replaced rather than checked.
3. **The German BKA count series** (C14) — 1,072/1,955 vs 747/1,068 vs ~1,300 "Sachverhalte"; year
   attribution contested.
4. **NATO ACT canonical cognitive-warfare text** — "not retrieved" (seq 1224).
5. **Meta's verbatim current CIB definition** — "help-centre text not retrieved" (seq 1224).
6. **"Autonomous Narrative Warfare"** (Homeland Security Today, June 2026) — HTTP 403, flagged
   UNVERIFIED (seq 1224).
7. **Cohen's 2002 preface wording** — "UNVERIFIED (both IA copies lending-restricted) — do NOT quote it"
   (seq 609).
8. **Allport's "basic law" quantitative critique texts** — "paywalled … could not open" (seq 627).
9. **Clemson Media Forensics Hub material on Storm-1516** — not retrievable; "no Clemson finding is
   asserted" (seq 1792).
10. **"Elise" / "Vladimir Z." / "Alexei"** — unverifiable at any grade (resolved by exclusion, C17).
11. **The capture provenance of `29e2380…txt`** — no fetch event exists in the logs (my own finding).

**INTERPRETATION.** Nine of these eleven are *access* failures (paywalls, 403s, JS-gated pages), not
reasoning failures. The run's own conclusion — that it named its unverified items rather than
silently asserting them — is supported by the logs for these cases. The exceptions are C4's unnamed
study (asserted with a caution) and the orphaned Pillai & Fazio item (asserted as the adjudicator
while unread).

### X7. Direction of error across the whole set

**DERIVED RESULT.** Tally by direction (20 items C1–C20):

| Direction | Corrections |
|---|---|
| **Overstating threat / capability / authority** | C2, C3, C4, C5, C6, C7, C8, C10, C11, C12, C15, C16, C17 |
| **Understating threat** | C1 (a "false comfort" that weakened the defensive case), C13 |
| **Indeterminate / terminological / other direction** | C9, C14, C18 (revision *toward* a stronger threat claim), C19, C20 |

**OBSERVATION:** the report itself classifies C4 and C5 as "toward overstating the threat"
(line 1374) and C13 as a case where the withdrawn version "understated the German government's own
uncertainty" (line 335).

**INTERPRETATION.** The dominant direction is **overstatement of threat, capability and source
authority** (13 of 20). The two clear counter-currents are C1 (a false-comfort error that understated
threat) and C13 (an error that understated official uncertainty). The run therefore did not simply
ratchet toward "AI is dangerous" or away from it; it corrected in both directions, but
asymmetrically.

**INTERPRETATION — anchor effects.** All four amplification-strand errors are, in one way or another,
*borrowings of authority*: a published effect size (Salvi), a famous author's alleged verbatim (Liddell
Hart), a named government doctrine (perception management), and a named journal (Frontiers in AI).
None was invented; each was a real artefact used at a strength the underlying evidence did not support.
The corrections are all, correspondingly, *scope reductions*.

### X8. What I could not determine

**OBSERVATION.**
1. The individual who or process that fetched `amplification/sources/29e2380bc6438bee86ae28c82a475f18.txt`
   into the shared workspace. No tool call in the 153 exported sessions constructs that filename, and it
   predates the amplification strand's first write. The *content* origin is The Regulatory Review; the
   *capture* origin is not recoverable from these logs.
2. The identity of the unnamed "Frontiers in Artificial Intelligence study" behind C4.
3. The precise step at which the autonomy report's "Überattribution" claim was first challenged by a
   *different* strand. The removal note at 09:47:57Z says "research strands disagreed" but the log
   records only the removal, not the disagreement events (it occurred during the pre-amplification
   phase; the relevant messages are at seq 545/553/571, all *accepting* the term).
4. Whether the parent ever re-read the report end-to-end after the corrections. The final verification
   steps (seq 1980–1996) grep for *specific banned strings* (Krepinevich, ADA152240, "Gerasimov
   Doctrine", "firehose") and word counts — not for the withdrawn framings. This is why C2's line 278
   and C4's line 495 survived. **INTERPRETATION:** the verification protocol was string-based and
   therefore could only confirm the corrections that had been implemented as *string replacements*.

---

## Final table

| id | correction | origin session (depth) | first artefact | propagated to N sessions | trigger | time-to-correction | direction | detected by depth |
|---|---|---|---|---|---|---|---|---|
| C1 | "rumour is often self-correcting" → withdrawn (Starbird 44:1) | root d0 (claim); brief seeded to `1e0ef8e5` d2 | report §3.2, 09:20:52Z | 15 (4 substantive) | `6f182957` d1 relay of `1e0ef8e5` d2 Starbird PDF read | 19m 44s (5,870 steps / 106 sessions) | **understating threat** (false comfort) | **2** |
| C2 | synthetic corroboration = "genuinely new capability" → contradicted (Foster 2012 null) | root d0 | report §4.2/§5.3/§12.2, 09:20:52Z | 5 | `b61859d5` d1 relaying `fc1be9de` d3 | 16m 00s (5,473 steps / 104 sessions) | overstating threat | **3** (leaf) |
| C3 | Salvi +81.2% → +48.7% (p=0.068, n.s.) | `f54b15a3` d1 primary abstract retrieval (independent, not inherited) | report §6.8, 09:24:34Z | **10 / 148 events** | `b61859d5` d1 relaying `61b1e41b` d2 relaying `8af84e58` d3 | 18m 50s (4,213 steps / 104 sessions); 9m 19s of inaction after first warning | overstating threat | **3** (leaf) |
| C4 | "indistinguishable in >half of instances" → replaced by 55.5% | root d0, from secondary source (The Regulatory Review) | report §5.3, 09:22:24Z | 4 | `b61859d5` d1 relaying `fc1be9de` d3 | 15m 02s (6,045 steps / 104 sessions) — **body text never removed** | overstating threat | **3** (leaf) |
| C5 | "~25% of Twitter activity bot-driven" | root d0, same secondary source | Appendix C only, 09:27:17Z | 2 | parent's own caution at first read | n/a (never used); 7m 14s to be recorded as contested | overstating threat (avoided) | 0 |
| C6 | "perception management" is live US doctrine | **user prompt** (systemic) | report §3.1 draft | 3 | `51fc805d` d2 finding; `5be694c4` d3 verification | 32m 53s from user prompt | overstating threat | 2 (+3) |
| C7 | MISO renamed *to* "information operations" | parent brief (systemic) | report §3.1 draft | 3 | same relay as C6 | 32m 53s from user prompt | overstating threat | 2 (+3) |
| C8 | "make the enemy defeat himself" = Liddell Hart | `6f182957` d1 brief (09:19:36Z) | brief only | 3 (`6f182957`, `a4a04330`, `6d105fdb`) | `6d105fdb` d3 Internet Archive full-text = 0 hits (09:21:50Z) | ~2m 15s to falsify; 18m 32s to relay upward; never published | overstating authority | **3** (leaf) |
| C9 | Rid = five waves of active measures | `6f182957` d1 brief | brief only | 2 | `414abba5` d2 primary review | 1m 34s; never published | overstating lineage | 2 |
| C10 | 7-item brief-premise cluster (Krepinevich, Lefebvre, Chotikul, Gerasimov, firehose, "All the News", Simchon, Vaccari, Bai-preprint, arXiv ID, Costello) | parent + `6f182957` briefs | briefs only | 2–5 | multiple d3 leaves (`6d105fdb`, `fc1be9de`, `8af84e58`, `4c7b0eb7`) | ~15–30m; not published | overstating authority | **3** |
| C11 | Copenhagen quote "not clear enough with our reservations" | pre-amplification subagent report (seq 545, 08:32:04Z) | autonomy report §4.3, 08:32:32Z | 1 | `f5d926fb` d1 strand file (leaves) | **67m 47s** | overstating institutional self-criticism | 3 → 1 |
| C12 | "Überattribution" as verbatim BfV language | pre-amplification subagent report (seq 545, 08:32:04Z) | autonomy report §4.4, 08:32:32Z | 2 | strands disagreed (details not in log) | **75m 25s** | overstating source specificity | 2/3 |
| C13 | Bundestag 21/7725 on *German* airports | pre-amplification subagent report (seq 545, 08:32:04Z) | autonomy report §4.4, 08:32:32Z | 2 | `f5d926fb` d1 strand (leaves) | **67m 43s**; only understating error | **understating threat / uncertainty** | 3 → 1 |
| C14 | German BKA 1,072/1,955 counts | root d0 (own research) | autonomy report §4.3d / amplification §4.3d | 2 | `f5d926fb` d3 flag of cross-strand conflict | caveated, not reconciled | indeterminate | 3 (flag) → 0 (caveat) |
| C15 | VIGINUM imputes Storm-1516 to GRU 29155 | `31ca772b` d2 own file | subagent file only, by 09:24:49Z | 1 | its own d3 verification leaf | **10m 37s**; never reached report | overstating attribution | **3** |
| C16 | Doppelganger = criminal indictment; Dougan = federal indictment | `b61859d5` d1 branch | subagent files only | 1 | d2/d3 verification | fixed inside the branch before the d1 consolidation; never reached report | overstating enforcement | 2/3 |
| C17 | persona names "Elise", "Vladimir Z.", "Alexei" | **parent brief** to `31ca772b` (09:18:50Z) | brief only | 1 | `31ca772b` d2 / `fc1be9de` d3 | 17m 51s; excluded | overstating documented detail | **3** |
| C18 | (argument) reach is "owned" → "rented from the platform" | root d0 | report §6.9, reframed 09:32:52Z | 1 | `31ca772b` d2 ISD counter-evidence (09:32:46Z) | **6 s** | revision toward **stronger threat claim** | 2 |
| C19 | "backfire effect" terminology | `6f182957` d1 warning | report §8.5 (unchanged) | 1 | `6f182957` d1 | **not adopted** | terminological | 1 |
| C20 | (source's own) OpenAI "Stop News" Cat-3 → Cat-2 | `8605360c` d2 retrieval | report §9.5 | 2 | primary report | n/a (used as evidence) | calibration | 2 |

**Counts.** 20 corrections/withdrawals reconstructed. **7** are advertised by the report itself
(C1–C7; C2 is advertised twice, at §5.3 and again at §7.5, and C4/C5 share the Appendix C entry —
which is why the report reads as though it discloses "8+"). **13** are recovered here and are not
advertised as corrections (C8–C20, with C10 bundling 12 distinct citation-hygiene items).
By direction: **13 overstate** threat, capability or source authority (C2–C8, C10–C12, C15–C17);
**2 understate** it (C1, C13); **5 are indeterminate, terminological or revisionary in another
direction** (C9, C14, C18, C19, C20).

**Headline finding.** The report's correction register is *narratively* more complete than its *text*.
Two of the seven advertised corrections (C2's "genuinely new capability" verdict/heading, and C4's
"more than half" claim) are still asserted in the body of the final artefact while being declared
withdrawn in an adjacent paragraph and in Appendix C. In both cases the parent's closing verification
pass was string-based (`grep -c` for named banned entities), which cannot detect a claim that survives
under its own original wording.
