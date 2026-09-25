# Deep Research Log Analysis

**A forensic case study of one 153-session recursive AI research run.**

This repository asks a different question from the research that produced it:

> **What did 153 recursively delegated agents actually buy us?**

The original DSH run produced substantial research output. Rather than only judging the final reports, we exported the full session tree and reconstructed the process itself: delegation, source discovery, corrections, inter-agent messages, provenance, stopping behaviour, token use, caching and provider cost.

The result is a practitioner-oriented analysis of **1.286 billion logged tokens, 153 sessions, 10,037 model steps and 16,195 tool calls** from a single traceable research run.

**Report DOI:** [10.13140/RG.2.2.27040.14080](https://doi.org/10.13140/RG.2.2.27040.14080)

## Start here

**For the readable account:**  
[**What 153 agents actually bought us**](practitioner-report.md) — the practitioner report, with figures and the main lessons from the case.

**For the technical reconstruction:**  
[**analysis/00-synthesis.md**](analysis/00-synthesis.md) — the evidence-heavy synthesis, with links to the detailed analyses and derived data.

**For the research the agents were actually doing:**  
[**leonvanbokhorst/deep-research**](https://github.com/leonvanbokhorst/deep-research) — the original substantive research artefact. The object analysed here is frozen at commit [`33ca23b`](https://github.com/leonvanbokhorst/deep-research/commit/33ca23b474a11b5ee90563a9f59ed002de485abd).

In short:

- **deep-research** = what the agents researched and concluded
- **deep-research-log-analysis** = what the 153-agent process actually did

## What we found

The case did not reduce to “more agents are better”. Different epistemic functions scaled differently.

**Breadth scaled well.** The 16 depth-1 branches explored largely different evidence spaces; median pairwise domain overlap was only **0.031**, and only **1.9%** of normalised unique queries were repeated across sessions.

**Deep verification was unexpectedly useful.** Three of the four largest corrections originated in depth-3 leaves. Narrow descendants sometimes reopened claims their ancestors had already accepted and found primary-source problems.

**Independent evidence gathering was not independent judgment.** The final report described “six independent evidence streams” converging, but provenance showed those streams were sibling agents under one branch and the central framing had already appeared before several decisive findings arrived.

**Corrections did not always propagate.** The system could find an error without reliably updating every place where the old claim survived.

**The tree did not naturally finish.** Forty of 91 depth-3 sessions attempted another level of delegation; **99 depth-4 spawn attempts** were rejected by the harness. The run stopped at a fence.

**Stopping was a high-variance problem.** General source discovery declined sharply, yet several of the most valuable corrections arrived late. Conclusion stability would have been an especially poor stopping signal because the central framing stabilised early.

**Messages mattered more than files.** Once inter-agent messaging is included, **152 of 153 sessions** contributed output that reached another session.

**Caching changed the economics dramatically.** The frozen run reconstructs to about **$12.19** at the actual DeepSeek rates billed that day. The prompt-side input cache-hit rate was **98.525%**. Cheap scale made the run feasible; it did not make the scale epistemically valuable by itself.

The compact summary is:

> **Breadth decentralised. Verification distributed. Judgment centralised.**

## Repository map

```
.
├── practitioner-report.md          human-facing account
├── figures/                        explanatory figures used in the report
└── analysis/
    ├── 00-synthesis.md             technical synthesis
    ├── 01-corpus-manifest-and-schema.md
    ├── 02-agent-genealogy.md
    ├── 03-token-and-cache-tables.md
    ├── 04-contribution-mapping.md
    ├── 05-independence-and-convergence.md
    ├── 06-anomalies-and-unexpected-behaviour.md
    ├── 07-marginal-return-and-stopping.md
    ├── 08-provider-billing-reconciliation.md
    ├── data/                       derived datasets and provenance records
    ├── notes/                      forensic working analyses
    ├── tables/                     roll-up tables
    └── tools/                      deterministic reconstruction scripts
```

For the detailed file-by-file guide, see [`analysis/README.md`](analysis/README.md).

## Reproducibility and provenance

The original 153-session export is not committed because it is a large externally supplied corpus. Its contents are pinned file-by-file by SHA-256 in [`analysis/data/manifest.json`](analysis/data/manifest.json). The relationship between this analysis and the frozen research artefact is recorded in [`analysis/data/case-study-provenance.json`](analysis/data/case-study-provenance.json).

The committed datasets and tables are sufficient to inspect the numbers quoted in the reports. To regenerate them from scratch, the original export must first be restored locally. The scripts under [`analysis/tools/`](analysis/tools/) are deterministic and read-only with respect to that corpus.

Raw provider billing exports are also intentionally excluded because they contain account/API-key identifiers. Sanitised derivatives used for the cost reconstruction are included.

## Scope

This is **one forensic case study**, not a benchmark of agent systems in general. It used one harness, one model/provider configuration, one recursion limit, one final synthesiser and two related research questions.

The point is not to claim that 153 agents is an optimal number. The point is that this run is unusually inspectable, allowing us to distinguish what recursive scale genuinely contributed from what the final prose merely made it look like it contributed.

## Author

**Leon R. van Bokhorst**  
Research Group IxD · Fontys University of Applied Sciences

Suggested citation:

> van Bokhorst, L. R. (2026). *What 153 agents actually bought us: Lessons from a 1.28-billion-token recursive research run.* Research Group IxD, Fontys University of Applied Sciences. [10.13140/RG.2.2.27040.14080](https://doi.org/10.13140/RG.2.2.27040.14080)
