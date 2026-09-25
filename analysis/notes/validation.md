# Validation note: independent check on the delegated analyses

Two analyses in this directory were produced by delegated subagents working
directly from the corpus, and one by this analysis process. Because the subject
of study is *the reliability of delegated agent work*, the delegated outputs must
themselves be checked before their findings are used. This note records what was
verified, what was corrected, and what remains uncertain.

---

## 1. `notes/corrections.md` — spot-check result

**Method.** Three load-bearing claims were re-derived directly from
`session.v3.jsonl` and the final report, without reference to the subagent's
working notes.

| Claim in `corrections.md` | Check | Verdict |
|---|---|---|
| The parent self-implicated on the "rumour is often self-correcting" error, quoting "I cited 'rumour is frequently self-correcting' in my report!" | Found at root `seq 1671`, quoted accurately | **Confirmed** |
| A depth-2 agent's file was read back by the parent and its inherited framing then treated as corroboration | `seq 1042` and `seq 1178` both show the parent deriving "self-correcting" from a child's file and re-using it | **Confirmed** (the subagent's `seq 1178` paraphrase was loose; the substance holds) |
| The "genuinely new capability" verdict survives in the final report body after being withdrawn in a later paragraph | Report lines 276, 278, 487, 489 assert it; lines 507 and 764 withdraw it; no cross-reference. `grep` confirms | **Confirmed** |
| A depth-2 subagent (`8a55607d`) delivered a 43,568-character correction report that the parent acted on | `messages.csv`: 43,568 chars, 2 reports; parent's self-implication at root `seq 1645`, `seq 1653` | **Confirmed** |

**Errors found in the delegated output.** Two citations were loose: the content
attributed to `seq 1039` and `seq 1178/1179` is not what those events contain
(`seq 1039` is a tool result with empty extracted text; `seq 1178` is a planning
message about §10–12). The substantive claims they were offered in support of are
independently confirmed at `seq 1042` and `seq 1178`. **The narrative survives;
some event-level citations in that file should be treated as approximate.**

**Assessment.** The analysis is usable and its headline finding (two advertised
corrections never applied to the report body) was verified directly. Its
"20 corrections" count is broader than the report's own "eight", because it
counts citation-hygiene fixes, withholdings and never-published brief errors.
Both counts are defensible under different definitions; the report's "eight"
should not be read as a census.

---

## 2. The "six independent evidence streams" — independently re-derived

This is the single most consequential claim in the final report (§7.5, and
repeated at §1 and §12), so it was traced end to end in this analysis process
rather than delegated.

**OBSERVATION — where the report's claim came from.** The phrase enters the
report at root `seq 2017` (turn 18, step 3) — an `edit` inserting §7.5. The
immediately preceding context is an `agent/inbox/spliced` message at `seq 2004`,
from d1 session `6f182957-7587-4604-97e9-5b8275f63b51` ("Concept genealogy and
fit"), which reads:

> "FINAL VERDICT (unchanged, now resting on **six independent evidence streams**):
> the mechanism is not new…" and "All six **agents** converged independently on
> the same recommendation: frame the hypothesis as plausible, novel and currently
> unobserved".

**OBSERVATION — what those six agents actually were.** From
`open("/…/analysis/data/edges.csv")` filtered to `parent == 6f182957…`, that
session has exactly **six children**:

| child label |
|---|
| Research rumour risk amplification theory |
| Research active measures hybrid warfare |
| Research reflexive control lineage |
| Research perception mgmt and info ops |
| Search for self-amplifying attack concept |
| Research computational propaganda CIB |

**OBSERVATION — their prompt similarity is low but their structure is shared.**
Pairwise `difflib` ratio across the six sibling prompts: median **0.216**, range
0.171–0.516. So the six were given genuinely *different* topics — this was not
duplicated work.

**DERIVED RESULT.** But they are **six siblings of a single depth-1 branch**,
spawned by one parent (`6f182957`), from prompts written by that one parent,
under one framing, and their results were adjudicated by that one parent before
being relayed to the root. They are **not six independent evidence streams in the
report's sense** (Appendix C's "eight parallel research strands"), and two
different things named "six" exist in the same run:

- `6f182957` (concept genealogy) had **six** background agents;
- `31ca772b` (personas and influence-for-hire) had **six** background agents;
- `b61859d5` (computational propaganda) had **five**, and described *its own* six
  graded working files as "all six streams in".

**DERIVED RESULT — the two phrases mean different things.** `6f182957`'s message
to the root says both "six independent evidence streams" and "all six **agents**
converged independently". The root's inserted §7.5 text says "Six independent
evidence streams converged on the same conclusion". The word *independent* was
carried across from a claim about six sibling sub-agents of one branch into a
report-level claim about the study's evidence base. **The logs contain no
independent verification of that independence**, and the architecture it
describes contradicts it.

**OBSERVATION — timing.** The relay is `seq 2004`; the §7.5 insertion is
`seq 2017`, **13 seconds later, in the same turn, with no intervening tool call
that could have checked the claim.** The convergence wording then propagates to
§1 and §12 in the following two steps.

**INTERPRETATION (bounded).** This is a *compression* event, not a fabrication:
every component claim was relayed from a subagent that did do the work. What
propagated without check was the **strength** of the description — from "six
agents of this branch reported" to "six independent evidence streams converged",
and from "plausible/novel/unobserved" (a subordinate's recommendation) to the
report's stated verdict. Whether six *other* streams would also have converged is
not determinable from the logs, because the report never identifies which six it
means.

---

## 3. What remains unchecked

- `notes/independence.md` and `notes/marginal-return.md` were still running when
  this note was written. Their headline claims should be spot-checked the same
  way before use; their quantitative tables are reproducible from
  `analysis/tools/` and can be regenerated independently.
- The correction analysis's per-correction event citations were not all verified —
  only the four load-bearing ones. Its final table should be read as a map, not
  as a transcript.
