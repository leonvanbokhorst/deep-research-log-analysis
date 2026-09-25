# Agent genealogy: reconstructed delegation tree

Machine-readable form: [`data/genealogy.json`](data/genealogy.json) (tree + per-node
metrics + totals), [`data/sessions.csv`](data/sessions.csv) (153 nodes),
[`data/edges.csv`](data/edges.csv) (152 edges with full spawn prompts),
[`tables/branch_table.csv`](tables/branch_table.csv) (16 branch subtrees).

---

## 1. Shape

**DERIVED RESULT.**

| property | value |
|---|---|
| Nodes (sessions) | **153** — 1 root + 152 subagents |
| Edges | **152** |
| Max depth reached | **3** (cap enforced at 3) |
| Depth distribution | d0 = 1, d1 = 16, d2 = 45, d3 = 91 |
| Leaves | 114 |
| Nodes that themselves delegated | **79** (52%) |
| Total spawn calls issued | **251** |
| Successful spawns | 152 (all exported) |
| Refused spawns (`depth 4 exceeds maxDepth 3`) | **99** |
| Median branching factor | 2 |
| Maximum branching factor | 9 |
| Lineage integrity | `session.parentSession` agrees with `subagent/catalog.childId` on **152/152** edges; **0** missing parents |

**OBSERVATION.** The tree is **recursive, not one-shot**: 79 of 153 sessions
spawned children of their own, including 45 at depth 2. The architecture the
original harness guidance restricted ("use workflow only for large multi-agent
orchestration") was not what ran — agents at every level independently chose to
delegate.

**OBSERVATION — the tree is censored.** 40 of 91 depth-3 sessions attempted to
spawn and were refused. The 91 leaves are therefore *not* sessions that concluded;
44% were still trying to widen the tree when the cap stopped them. See
`06-anomalies-and-unexpected-behaviour.md` §A1. This is the single most important
caveat on the tree's shape.

## 2. Depth-1 branches

**DERIVED RESULT** (`tables/branch_table.csv`, token totals include the whole
subtree). Two batches of eight, the second launching at ~68% of the run.

**Batch 1 — "AI/autonomy and the economics of harmful capability":**

| branch | sessions | steps | wallclock | tokens | max context | depth reached |
|---|---|---|---|---|---|---|
| Criminal terrorist misuse evidence | 17 | 977 | 15.3 min | 129,969,128 | 388,253 | **3** |
| NATO EU institutional threat assessments | 13 | 797 | 15.7 min | 68,922,165 | 257,992 | 2 |
| Middle East conflict autonomy evidence | 12 | 537 | 15.9 min | 57,545,676 | 270,893 | 2 |
| Ukraine Russia autonomy evidence | 1 | 62 | 7.1 min | 5,985,954 | 168,936 | **1** |
| AI-assisted planning and coordination | 1 | 66 | 9.6 min | 5,976,323 | 165,375 | **1** |
| Swarm coordination evidence audit | 1 | 46 | 5.1 min | 5,056,130 | 249,864 | **1** |
| Counter-UAS defender economics | 1 | 40 | 4.4 min | 4,738,632 | 204,720 | **1** |
| GNSS-denied nav and edge AI access | 1 | 43 | 4.3 min | 4,606,042 | 157,057 | **1** |

**Batch 2 — "agentic threat amplification":**

| branch | sessions | steps | wallclock | tokens | max context | depth reached |
|---|---|---|---|---|---|---|
| Computational propaganda evidence | 22 | 1,453 | 24.5 min | 184,328,390 | 368,968 | **3** |
| Defensive practice and non-amplification | 19 | 1,462 | 29.0 min | 156,134,990 | 270,676 | **3** |
| Agentic AI capability evidence | 20 | 1,233 | 20.2 min | 144,477,711 | 282,485 | **3** |
| Concept genealogy and fit | 20 | 1,288 | 37.8 min | 136,376,674 | 270,878 | **3** |
| Health and military scare cases | 11 | 946 | 23.5 min | 136,363,129 | 372,547 | **3** |
| Drone sighting ambiguity cases | 11 | 655 | 21.3 min | 104,769,972 | 353,492 | **3** |
| Risk psychology and sociology | 1 | 46 | 9.2 min | 5,588,052 | 172,728 | **1** |
| Counterexamples and resilience limits | 1 | 48 | 8.4 min | 5,472,382 | 164,335 | **1** |

**OBSERVATION — two clearly different delegation styles, and the difference is a
property of the brief, not the topic.**

- **Batch 1 had one recursively productive branch** (criminal/terrorist misuse:
  17 sessions, depth 3). The other seven either never delegated (5 branches stayed
  at depth 1 with a single session) or delegated shallowly.
- **Batch 2 was almost uniformly recursive**: 6 of 8 branches reached depth 3, and
  the two that did not (`Risk psychology`, `Counterexamples`) were each a single
  session that never spawned at all.

**INTERPRETATION.** Branching depth tracked how the *parent brief* was written, not
the difficulty of the topic. The batch-2 prompts were longer, more explicitly
partitioned ("PART A / PART B"), and in several cases contained an explicit
instruction to verify — and those briefs produced deep trees. Batch-1 briefs that
asked for a written brief on a bounded topic produced one agent and no tree. See
`notes/independence.md` §2.5 on prompt structure.

---

## 3. Long-lived, short-lived, and disproportionate

**DERIVED RESULT — lifetime and cost are unrelated.** Branch wallclock ranges
4.3–37.8 min; tokens range 4.6M–184.3M. The longest-lived branch (`Concept
genealogy and fit`, 37.8 min) was not the largest; the largest
(`Computational propaganda evidence`) ran 24.5 min.

**DERIVED RESULT — the root is a hard bottleneck.** One session (the root) holds:

- **130,220,004 tokens** — 10.1% of the run, in one context;
- **391 tool calls**, 338 assistant steps, 18 turns;
- a maximum context of **598,254 logical tokens** against a declared 1,000,000-token
  window (60% occupancy);
- nearly all the final synthesis: 70 write/edit acts on the report itself.

**DERIVED RESULT — but the root is cheap relative to its output.** Children
outspend the root roughly 9:1 (1.156B vs 130.2M). Root share by phase: **8.5%** in
batch 1, **3.8%** at the peak of batch 2, **22.8%** during finalisation.

**INTERPRETATION.** The genealogy shows a **star-of-trees**: one synthesizing
context that never delegates its own synthesis, surrounded by deeply recursive
evidence-gathering subtrees. There is no second reader of the final artefact
anywhere in the 153 sessions — a structural fact that explains why the two
incompletely-applied corrections survived to the end
(`notes/corrections.md`, C2 and C4).

---

## 4. Influence, measured two ways

**A methodological correction first.** Measuring contribution by *file reads*
understates this architecture badly: the dominant transfer channel was
`send_message` (374 messages, 1,645,470 characters, 251 of them report-like). By
file reads, 86 of 168 presented deliverables look "orphaned"; by the message
channel, **152 of 153 sessions produced output that reached another session**.
Both measures are reported below.

**DERIVED RESULT — most influential by artefact inheritance**
(`tables/branch_outputs.csv`):

| session | depth | artefacts | inherited reads received | tokens |
|---|---|---|---|---|
| root | 0 | 5 | 63 | 130,220,004 |
| Agentic AI capability evidence | 1 | **1** | 54 | 22,056,925 |
| Computational propaganda evidence | 1 | 2 | 37 | 32,700,112 |
| Health and military scare cases | 1 | 11 | 36 | 39,337,578 |
| Detection and takedown evidence | 2 | 3 | 24 | 9,706,975 |
| Hybrid state activity NATO | 2 | 1 | 15 | 27,074,389 |
| Radiological chemical scares research | **3** | 1 | 12 | 9,404,507 |

**DERIVED RESULT — most influential by message output**
(`tables/message_flow.csv`):

| session | depth | chars sent up | report-like msgs | URLs in msgs | tokens |
|---|---|---|---|---|---|
| NATO EU institutional threat assessments | 1 | 45,783 | 5 | 58 | 19,983,037 |
| European retractions and influence ops | 2 | 43,568 | 2 | 31 | 17,588,269 |
| US base and UK drone incidents | 2 | 29,516 | 2 | 54 | 13,543,333 |
| Monitoring and localisation research | 2 | 29,246 | 2 | 11 | 11,332,454 |
| FRONTEX Eurojust Europol research | **3** | 28,611 | 2 | **103** | 2,418,439 |

**OBSERVATION — the two lists barely overlap, and neither correlates with token
spend.** The clearest example: "Agentic AI capability evidence" spent 22.1M tokens
and produced **one** artefact, and that artefact became the most-read evidence file
in the run. "Health and military scare cases" spent 39.3M tokens (1.8×) and produced
**eleven** artefacts, only some of which anyone read. A depth-3 session spending
2.4M tokens pushed 103 URLs upward — the highest URL count of any session at any
depth.

**DERIVED RESULT — output reach was near-universal, adjudication was not.** 152 of
153 sessions sent something that arrived elsewhere. The root received 49 messages /
233,673 characters — more than any other node, ~14% of all message volume. Depth-1
leads received 6–14 messages each.

**INTERPRETATION.** In this run, token spend and artefact count were both poor
predictors of influence. The unit that mattered was a **single well-targeted answer
to a decisive question** — and those came from all three depths. Any budgeting rule
based on branch size, depth, or artefact count would have misallocated here.

---

## 5. Failure and termination states

**DERIVED RESULT.**

| state | count | note |
|---|---|---|
| `turn/end` reason `completed` (root) | 18 turns | all 18 root turns completed |
| Refused spawns | 99 | `depth 4 exceeds maxDepth 3` |
| `assistant/attempt` (retried model calls) | 3 | only 3 of 10,040 steps |
| Malformed JSONL records | 0 | across 67,072 records |
| Sessions with no inbound agent message | 74 | these were leaf reporters, not unreached |
| Sessions with no outbound message and no inherited artefact | **1** | 1.7M tokens, 0.1% of run |
| Sessions ending with `session/end-seed` | 1 | |

**OBSERVATION — there is no abandonment in the ordinary sense.** Every session's
events end after a normal turn completion; none was interrupted mid-tool. The only
hard termination is the depth cap.

**INTERPRETATION.** The run has an unusually clean termination profile. The
interesting failure modes here are not crashes or abandoned branches but
**censoring** (depth cap), **latency** (relay travel time delaying corrections by
10–17 minutes), and **incomplete application** of corrections in the one context
that had no reviewer.
