# Evidence independence in the *Agentic Threat Amplification* run

**Object of test.** The claim, made twice in `/Users/leonvanbokhorst/repos/deep-research/amplification/Agentic-Threat-Amplification-2026.md` (§7.5, lines 775 and 801), that

> "Six independent evidence streams converged on the same conclusion"

where the conclusion is that agentic amplification of ambiguous physical threats is "plausible, novel and currently unobserved", with the decisive constraint that "autonomous agent-to-agent propaganda coordination has been demonstrated only in simulation — never observed in the wild."

**Corpus.** 153 sessions (root + 152 subagents) under `dsh-session-session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357/`, read line-by-line via `analysis/tools/corpus.py`. Secondary comparison: the research workspace `/Users/leonvanbokhorst/repos/deep-research/amplification/`.

Every timestamp below is a DSH event `time` (ms epoch). `d0` = root, `d1` = strand, `d2`/`d3` = nested agents. Session ids are abbreviated to 8 hex characters and are traceable in the corpus.

---

## 0. Method — what I could and could not measure

### Measured directly from the logs
| Quantity | How |
|---|---|
| Session tree, parentage, delegation depth, labels | `session` header + `subagent/descriptor` + `subagent/catalog`, cross-checked against `analysis/data/edges.csv` |
| Full text of every `subagent` spawn prompt (251 spawns; 152 match an exported child session) | `tool/call` where `name == "subagent"`, `arguments.prompt` |
| Pairwise prompt similarity | `difflib.SequenceMatcher` ratio, token Jaccard, 6-gram Jaccard, longest-common-token-span |
| External retrieval acts | `web_search`, `web_fetch`, and `bash` containing `curl`/`wget`/`get.sh`/`news.sh`/`ddg.sh`/`web.sh`/`bn.sh`/`j.sh`/`s.sh` |
| Search-proxy queries | `news.sh`/`bn.sh`/`ddg.sh` query strings recovered by regex from `bash` commands |
| Local reads of shared artefacts | `read`/`grep` file paths **and** shell read verbs (`cat`/`head`/`grep`/`wc`/`sed`…) naming a path under the workspace |
| Write-before-read (inheritance) | For every read of an evidence artefact, look for a *prior* write of that same artefact by a **different** session |
| First mention of a claim | First event (any type) per session in which a regex for the claim matches, then sorted by time |
| Provenance of a claim inside a session | Event tag: `asst-text`/`asst-reasoning` (agent's own), `tool/result` (its own retrieval), `tool/call:subagent` (it wrote the claim into a child prompt), `inbox/spliced`/`user/message` (received from another agent) |

### Could NOT be measured — stated as limits, not inferred
1. **99 depth-4 agents are absent from the export.** 251 `subagent` spawns exist but only 152 child sessions were exported; the missing 99 are the children of depth-3 sessions (e.g. `e289f909` spawned 4, `1deec50d` spawned 4, `fd99d7af` spawned 4, `37c2487b` spawned 3, …). **Their prompts are in the logs; their transcripts, retrievals and assertions are not.** Every "N of 8 streams" count below therefore under-counts work done at depth 4. This weakens any claim that a strand "did not find" something.
2. **Full HTTP histories are not recoverable.** Many `bash` commands run helper scripts (`tools/s.sh`, `tools/j.sh`, `tools/ddgc.sh`) whose internals live in the workspace, not in the log. URLs are extracted where they appear literally in the command; URLs that only appear inside a helper script's own output are captured only via `tool/result` text.
3. **`web_search` was unusable for the whole amplification phase.** Its last use is at `1790327877895`, ~19 s after the phase began (`1790327859369`); all 135 calls are in the earlier autonomy phase. So "search coverage" is really "Google News RSS + direct fetch + site-search coverage". Identical for all eight strands.
4. **Domain and URL overlap are not the same as evidential overlap.** Two strands may fetch the same document from different hosts, or different documents from the same host. I report both levels and flag which shared entries are *infrastructure* rather than evidence.
5. **The report's own §7.5 attribution of "six streams" is internally ambiguous.** The report's Appendix C names **eight** strands; §7.5 names **six**. The logs resolve this (see §4.3), but the report's wording does not.

---

## 1. Identifying the streams

### OBSERVATION — the eight amplification strands
The root session spawned eight `subagent` calls at `1790327928258`–`1790327928261`, matching Appendix C's list one-for-one. (The other eight depth-1 sessions, created at `1790324565xxx`, belong to the earlier autonomy study and are labelled `P1`–`P8` below for contrast.)

| ID | Label (descriptor) | Brief written | Appendix-C name | Subtree sessions |
|---|---|---|---|---|
| **S1** | `6f182957` Concept genealogy and fit | `findings/01-concepts.md` | concept genealogy | 20 |
| **S2** | `56542a81` Risk psychology and sociology | `findings/02-risk-psychology.md` | risk psychology and sociology | 1 |
| **S3** | `b61859d5` Computational propaganda evidence | `findings/03-computational-propaganda.md` | computational propaganda | 22 |
| **S4** | `f54b15a3` Agentic AI capability evidence | `findings/04-agentic-capability.md` | agentic capability | 20 |
| **S5** | `f5d926fb` Drone sighting ambiguity cases | `findings/05-drone-cases.md` | drone-sighting cases | 11 |
| **S6** | `46b82e74` Health and military scare cases | `findings/06-health-military-cases.md` | health and military scares | 11 |
| **S7** | `b0f0ef6b` Counterexamples and resilience limits | `findings/07-counterexamples.md` | counterexamples and resilience | 1 |
| **S8** | `dc0b75f5` Defensive practice and non-amplification | `findings/08-defensive.md` | defensive practice | 19 |

(Subtree counts include the strand itself; `P1`–`P8` = Ukraine, Middle East, swarm audit, GNSS/edge AI, criminal misuse, NATO/EU assessments, defender economics, AI planning.)

### OBSERVATION — the "six streams" are not the eight strands
The phrase "six independent evidence streams" traces to **`6f182957` (S1) describing its own six depth-2 children**, not to the eight-strand architecture:

> `1790330187652`, S1 `send_message` to root: *"FINAL VERDICT (unchanged, now resting on **six independent evidence streams**): … Recommendation for the parent study, which **all six agents converged on independently**: frame the hypothesis as plausible, novel and CURRENTLY UNOBSERVED"*

S1's six children were `488c117a` (reflexive control), `414abba5` (active measures), `51fc805d` (perception management/IO), `1e0ef8e5` (rumour/SARF/cascades), `edb0f8d3` (computational propaganda/CIB), `a4a04330` (self-amplifying prior art) — a subset of S1's *own* subtree. The root re-used the phrase and re-scoped it twice:

> `1790330206844`, root `edit` to the report: *"Six independent evidence streams converged on the same conclusion"*
> `1790330206846`, same edit: *"in the words **all six strands** converged on independently"*
> `1790330236597`, root final message: *"So **all six strands** independently converged on the same formulation"*

**DERIVED RESULT.** The number "six" originated one level down (six agents inside one strand) and was re-labelled by the root as six of the eight strands. The two framings are not the same claim.

---

## 2. Inherited context — how much of the conclusion was pre-loaded

### 2.1 The human prompt (top of the tree) does *not* pre-load the conclusion
`1790327859369`, 4,352 chars — a genuinely falsification-oriented brief: *"Treat this as a hypothesis to test, not a presumed phenomenon"*; *"Do not assume these capabilities are already being used operationally"*; *"Examine counterexamples and failed campaigns. Ask whether institutions and populations are actually as manipulable through ambiguity as the hypothesis assumes."* It does, however, hand over the causal chain verbatim, the five-category taxonomy, the concept list, and the four concluding questions that become report sections 5–7 and 10. **Verdict: framing supplied, conclusion not supplied.**

### 2.2 The eight strand prompts (root → S1…S8): one pre-stated expectation
**OBSERVATION.** The root's prompt to **S1** (spawned `1790327928258`) contains the only explicit statement of an expected outcome in the entire amplification phase:

> *"Be rigorous — **the most likely finding is that most of the mechanism is already described by existing concepts and only specific parts are new.** Say so if that is what the evidence shows."*

**DERIVED RESULT — prompt facet coverage across all 191 amplification-phase spawns:**

| Facet | Prompts containing it |
|---|---|
| identical `web_search is BROKEN` tooling block | **186 / 191** |
| the H1 hypothesis sentence verbatim | 8 / 191 |
| states a likely/expected finding ("most likely finding") | **1 / 191** (root→S1) |
| labels its section "the most important" / "the empirical heart" | 5 / 191 |
| tells the child what (not) to conclude | **2 / 191** |
| instructs scepticism / adversarial stance | 9 / 191 |
| names ≥5 candidate sources or authors | 12 / 191 |
| names the report's output path | 191 / 191 |
| **the conclusion formulation itself** ("plausible, novel, unobserved") | **0 / 191** |

The last row matters for the steelman: the *conclusion was never written into any prompt*. What was pre-loaded was (a) the conclusion's *direction* at exactly one node, and (b) the *sources* that would later support it.

### 2.3 The two prompts that steer the child's finding
**OBSERVATION**, root→S1 (`1790327928258`) and S1→`edb0f8d3` (`1790327976095`):

S1 wrote into `edb0f8d3`'s prompt: *"OpenAI's 'Influence and Cyber Operations' threat reports (2024-2026) — what they actually found about AI-enabled IO, and **their own statement that these operations have not achieved sustained audience engagement**"*, and *"This is essential for a rigourous fit audit: **exaggerating AI agent amplification may be a known failure mode.**"* The same prompt pre-names *"Rauchfleisch & Kaiser"*, *"Eady et al. 2023"*, *"Bail et al."*, and *"Meta/Facebook 2018-2020 IO research"*.

`edb0f8d3` then wrote into `1ece4a27`'s prompt (`1790328137731`): *"**including any OpenAI/Anthropic statement that these operations have NOT achieved sustained audience engagement or reach**"*; *"**The countervailing evidence**: studies/papers finding that AI-generated propaganda is *less* effective… Include the 'AI slop' / low-engagement finding"*; and *"**4. Agentic AI and influence**: anything on autonomous AI agents … **Note whether this is demonstrated or speculative.**"*

**DERIVED RESULT.** The two prompts that produced the report's decisive null (the OpenAI reach statement and the simulation-only framing) were written by agents who already knew what answer they expected. This is a *directed search for confirmation of a hypothesised null*, not an open search that happened to find one.

### 2.4 Caveat that cuts the other way
**OBSERVATION.** The same prompts routinely instruct the opposite too: root→S7 (*"Be adversarial toward the hypothesis"* and *"Do not manufacture counter-evidence — if the disconfirming case is weak, say so"*), root→S2 (*"Note that SARF describes accident/technology risk more than adversarial action — say where that limits transfer"*), S1→`1e0ef8e5` (*"Be rigorous and sceptical — flag where the 'Gerasimov Doctrine' or similar is a Western invention"*). The prompts are, on their face, two-sided. The bias is in *which* negative findings were pre-named.

### 2.5 Prompt similarity between the eight strands
**DERIVED RESULT.** Pairwise similarity of the eight root→strand prompts (each 451–573 words, 3,799 words total):

* `difflib` ratio: **0.186 – 0.282** (mean ≈ 0.23)
* token Jaccard: **0.207 – 0.339**
* 6-gram Jaccard: **0.033 – 0.117**
* Longest verbatim token span common to **all eight**: **19 tokens** — *"you are research analyst today is 25 september 2026 write your brief to users leonvanbokhorst repos deep-research amplification findings"*. Iterative longest-common-span extraction recovers only **41 / 3,799 tokens (1.1 %)** of shared verbatim text.

**INTERPRETATION.** On verbatim text, the eight prompts are *not* near-duplicates — the topics genuinely differ and the boilerplate is small. But this measure understates shared structure: the shared content is *framing*, not wording (identical tooling block, identical hypothesis vocabulary — "deliberate amplification", "ambiguous physical events", "coordinate inauthentic behaviour", "reflexive control", "amplification stations" — and a common demand for "demonstrated vs claimed vs inferred" separation and A–E evidence grades). `difflib` cannot see that. I therefore treat prompt similarity as **low at the lexical level, high at the framing level**, and lean on the facet table (§2.2) rather than the ratio.

### 2.6 The hypothesis block is propagated verbatim inside S1
**OBSERVATION.** All six of S1's depth-2 prompts (`1790327976095`–`1790327976109`) carry the same block verbatim: *"THE HYPOTHESIS TO AUDIT (context only): 'agentic threat amplification' — that AI agents could deliberately amplify ambiguous PHYSICAL threats (drone sightings, sabotage reports, infrastructure incidents, unexplained disruptions) so that communities, media and institutions generate much of the disruptive effect themselves. Proposed novelty: (i) AI agents as the amplification engine (autonomous, cheap, scalable), (ii) targeting ambiguous physical incidents rather than beliefs/opinion, (iii) the target population/institution supplies the disruptive effect."* Each child was then asked to rate "fit" against a **pre-specified three-part novelty claim**. S1's final fit table is the aggregate of those ratings.

---

## 3. Source overlap between streams

### 3.1 External retrieval volume (DERIVED RESULT)

| Stream | live web calls (`curl`/`wget`/`web_fetch`/`web_search`) | News-RSS calls | distinct fetched URLs | distinct domains | domains unique to this stream |
|---|---|---|---|---|---|
| S1 concept genealogy | 676 | 31 | 653 | 153 | 94 (61 %) |
| S2 risk psychology | 11 | 7 | 17 | 13 | 4 (31 %) |
| S3 computational propaganda | 638 | 289 | 440 | 106 | 43 (41 %) |
| S4 agentic capability | 597 | 262 | 500 | 108 | 61 (56 %) |
| S5 drone sightings | 310 | 154 | 254 | 86 | 44 (51 %) |
| S6 health/military scares | 476 | 190 | 307 | 112 | 63 (56 %) |
| S7 counterexamples | 34 | 10 | 29 | 16 | 3 (19 %) |
| S8 defensive practice | 747 | 112 | 736 | 218 | 137 (63 %) |

Caveat: URL counts are inflated by API query strings (`api.openalex.org/works?search=…` counts once per query). Domain counts are the robust column.

### 3.2 Domain-level Jaccard (DERIVED RESULT)

```
                  S1     S2     S3     S4     S5     S6     S7     S8
S1 concept     1.000  0.037  0.151  0.111  0.091  0.086  0.043  0.124
S2 riskpsych   0.037  1.000  0.044  0.043  0.010  0.025  0.036  0.022
S3 compprop    0.151  0.044  1.000  0.223  0.085  0.135  0.099  0.125
S4 agentic     0.111  0.043  0.223  1.000  0.054  0.089  0.088  0.098
S5 drones      0.091  0.010  0.085  0.054  1.000  0.100  0.052  0.118
S6 health      0.086  0.025  0.135  0.089  0.100  1.000  0.067  0.111
S7 counterex   0.043  0.036  0.099  0.088  0.052  0.067  1.000  0.035
S8 defensive   0.124  0.022  0.125  0.098  0.118  0.111  0.035  1.000
```
Maximum = **0.223** (S3–S4); median ≈ **0.086**.

### 3.3 URL-level Jaccard (DERIVED RESULT)
Raw URLs: maximum **0.031** (S3–S4); 70 of 2,837 distinct URLs (2.5 %) were fetched by ≥2 streams.
Path-normalised (query strings stripped): 1,686 distinct URLs, **105 (6.2 %) shared by ≥2 streams**, maximum Jaccard **0.076** (S3–S4).

### 3.4 The shared domains are infrastructure, not evidence (OBSERVATION)
Domains fetched by ≥3 streams — **all of them** are search engines, archives, or bibliographic APIs:

`archive.org/wayback/available` (7) · `bing.com/search` (6) · `web.archive.org/cdx` (6) · `api.semanticscholar.org` (6) · `html.duckduckgo.com` (6) · `api.openalex.org` (6) · `lite.duckduckgo.com` (6) · `en.wikipedia.org/w/api.php` (5) · `content.guardianapis.com` (5) · `eutils.ncbi.nlm.nih.gov` (5) · `ebi.ac.uk/europepmc` (5) · `api.crossref.org` (5) · `news.google.com/rss/search` (5) · `r.jina.ai` (5) · `mojeek.com/search` (4) · `export.arxiv.org` (4)

**INTERPRETATION.** At the level of *what was actually retrieved*, the eight streams are substantially non-overlapping. This is the strongest evidence **for** the independence claim, and it is genuine: no stream was reading another stream's source list wholesale.

### 3.5 But strands did read each other's material (DERIVED RESULT)
Reads of evidence artefacts under `amplification/{findings,notes,research,sources}/` where the file had been written **earlier by a different session**:

| Stream | inherited raw web captures (`sources/*.txt`) | inherited sibling analysis (`findings/`, `notes/`) | inherited sibling research (`research/`) | inherited report | **total inherited reads** | own-file reads |
|---|---|---|---|---|---|---|
| S1 | 3 | 9 | 2 | 2 | **16** | 77 |
| S2 | 0 | 0 | 0 | 0 | **0** | 14 |
| S3 | 9 | 15 | 0 | 2 | **26** | 122 |
| S4 | 0 | 12 | 0 | 1 | **13** | 89 |
| S5 | 0 | 4 | 0 | 3 | **7** | 14 |
| S6 | 17 | 21 | 0 | 3 | **41** | 117 |
| S7 | 0 | 0 | 0 | 1 | **1** | 12 |
| S8 | 0 | 0 | 7 | 0 | **7** | 79 |
| **Total** | **29** | **61** | **9** | **12** | **111** | **522** |

Cross-read artefacts (read after another session wrote them), with readers:

| Artefact | inherited reads | read by strands |
|---|---|---|
| `amplification/sources/raw-adversary.md` | 8 | S6 |
| `Agentic-Threat-Amplification-2026.md` (the report) | 7 | S3, S6, S1 |
| `amplification/findings/01-concepts.md` | 6 | S3, S1 |
| `amplification/sources/raw-publichealth.md` | 5 | S6 |
| `amplification/findings/06-health-military-cases.md` | 5 | S6, S1, S5 |
| `amplification/findings/04-agentic-capability.md` | 4 | S3 |
| `amplification/findings/07-counterexamples.md` | 3 | S3, S5 |
| `amplification/findings/02-risk-psychology.md` | — | S1, S5 |
| `amplification/findings/03-computational-propaganda.md` | 2 | S3 |

Downloaded primary-source captures read by ≥4 sessions: `nj-faa-joint-statement.txt` (6 sessions: ROOT, S1, S4, S5, S6, S8), `nj-fbi-dhs-statement.txt` (5), `abc-havana-2026.txt` (5), `eeas-4th-fimi-2026.txt` (4), `amplification/research/eeas-fimi-4th.txt` (3).

**INTERPRETATION.** Inheritance of *evidence material* is real but bounded: **111 inherited read acts against 522 own-file reads and thousands of live fetches.** The mechanism by which two strands can appear to "converge" on a source is visible — one agent downloads the EEAS report, three or four others read the local copy — but it accounts for a small share of total retrieval. The exceptions are S6 (`41` inherited reads, 17 of them raw captures) and S3 (`26`), which are the most downstream-heavy strands.

### 3.6 The report was read by strands *while they were researching it* (OBSERVATION)
The root wrote the first 28 KB draft of the report at **`1790328052156`** — about **two minutes** after the eight strands were spawned (`1790327928258`). Three strands then read that draft:

* `6f182957` (S1) — `1790328076889` (`head -120`) and `1790328080694` (`sed -n '120,256p'`)
* `46b82e74` (S6) — `1790328083962` (`head -120`)
* `31ca772b` (S4's child) — `1790328162034`, `1790328163992` (`read offset 300, limit 40`)

**OBSERVATION — what was already in the first draft.** In the `1790328052156` write, before any strand had reported:
> §0.1: *"The study states at the outset that **the most likely finding — and the one the evidence supports — is that most of this mechanism is neither new nor attributable to AI**, and that the genuinely new element is narrower and more specific than the popular framing suggests."*
> §1: *"It is **not** L3 evidence for agentic amplification of ambiguous physical threats specifically — that narrower case remains **unevidenced**."*
> §1: *"**The amplifier is not the botnet. It is the institution.**"*
> §2 table: H1b *"not established as engineered"*; H1d, H1e *"plausible but unevidenced"*.
> §3.1: reflexive control *"Fit: **High**"*; §3.2: SARF *"**Fit: High — and this is the single most useful framework in the study**"*.

**INTERPRETATION.** This is the clearest circularity channel in the run. The thesis, the falsification table, and the concept-fit ratings were in the draft **before** the strands that were supposed to establish them reported; two of the eight strands read the draft; and the strands' final fit table (S1: *"HIGH — reflexive control … HIGH substrate / POOR actor — rumour theory, SARF"*) reproduces the draft's preliminary ratings. The convergence between draft and strand output is partly **feedback**, not agreement between independent measurements. It is not a *pure* artefact — S1 also revised several ratings against the draft (see §6) — but the direction of travel was fixed early.

---

## 4. Discovery versus propagation

### 4.1 The conclusion's provenance chain (OBSERVATION, quoted)
This is the decisive trace for the sentence in §7.5.

| # | Time | Where | Event | Text |
|---|---|---|---|---|
| 1 | `1790327928258` | root → S1 | `subagent` prompt | *"the most likely finding is that most of the mechanism is already described by existing concepts and only specific parts are new"* |
| 2 | `1790327976095` | S1 → `edb0f8d3` | `subagent` prompt | OpenAI *"statement that these operations have not achieved sustained audience engagement"*; *"exaggerating AI agent amplification may be a known failure mode"* |
| 3 | `1790328137731` | `edb0f8d3` → `1ece4a27` | `subagent` prompt | *"any OpenAI/Anthropic statement that these operations have NOT achieved sustained audience engagement or reach"*; *"Note whether this is demonstrated or speculative"* |
| 4 | **`1790329772457`** | `edb0f8d3` (d2) | `write` `sources/platform-propaganda.md` | **FIRST APPEARANCE:** *"The hypothesis should be presented as **a plausible, novel, and currently unobserved threat class — not as an extrapolation from demonstrated effects.**"* |
| 5 | `1790330120131` | `edb0f8d3` → S1 | `inbox/spliced` | the same formulation arrives in S1's context |
| 6 | `1790330187652` | S1 → root | `send_message` | *"Recommendation for the parent study, which **all six agents converged on independently**: frame the hypothesis as plausible, novel and CURRENTLY UNOBSERVED"* |
| 7 | `1790330187667` | root | `inbox/spliced` | receives it |
| 8 | `1790330206844` | root | `edit` to report §7.5 | *"**Six independent evidence streams converged on the same conclusion**"* … *"in the words **all six strands** converged on independently: plausible, novel, and currently unobserved"* |

**DERIVED RESULT.** The formulation has **a single point of origin** in the corpus: `edb0f8d3` at `1790329772457`. It then travelled up one branch (d2 → d1 → d0) and was relabelled as the convergence of six.

**DERIVED RESULT — it is absent from every strand deliverable.** A full-text search of `/Users/leonvanbokhorst/repos/deep-research/amplification/` finds the phrase `plausible … novel … unobserved` in exactly **two** places: `sources/platform-propaganda.md` line 77 (written by `edb0f8d3`) and the final report (lines 79 and 801). **0 of the 21 files in `findings/` contains it — including `findings/01-concepts.md`, written by S1, the strand that reported it as a six-way convergence.** Seven of the eight strands never expressed the conclusion in that form at all.

### 4.2 First-mention timeline for the decisive evidence (DERIVED RESULT)

| Item | First appearance in the corpus | Producer | Independent re-discovery |
|---|---|---|---|
| **USC / WWW 2026, arXiv:2510.25003** (simulation-only agent coordination) | `1790328247207` — Google News RSS headline *"USC Study Finds AI Agents Can Autonomously Coordinate Propaganda Campaigns Without Human Direction"* in `cc07f9d4` (d2, **S4**); characterised *"simulation only"* at `1790328348298`. Separately retrieved as a paper by `0c1ed671` (**S1**, d3) `1790329312163` and `1ece4a27` (**S1**, d3) `1790329345660` (arXiv + ACM DOI `10.1145/3774904.3792580`) | **S4 first, S1 first-verified** | **YES — two streams (S4, S1)** |
| **Foster et al. 2012, "Repetition, not number of sources"** | `1790328255902` — `fc1be9de` (d3, **S3**), abstract via Semantic Scholar. S4's `43ef5bbb` searched the same concept at `1790328232667`, 3.5 min earlier, and did not surface it | **S3** | **NO** — one stream |
| **Rauchfleisch & Kaiser, Botometer AUC 0.85 / 0.94** | *Name* pre-seeded in S1's sub-prompt `1790327976090` (*"the 2018 critique of bot detection by Rauchfleisch & Kaiser"*). *Number* first retrieved `1790328402107` by `4db3eaea` (d3, **S3**); independently `1790328496510` by `da686808` (d3, **S4**); independently `1790329265636` by `d07fdde4` (d3, **S1**) — all three quoting the same sentence *"the ROC-AUC is worse with our complete data (AUC = 0.85) than … 0.94"* | **S3**, then S4, then S1 | **YES — three streams, same document** |
| **OpenAI: operations "do not appear to have meaningfully increased their audience engagement or reach"** | `1790328004753` — `f73d55cf` (d2, **S3**), fetched from `openai.com`; independently `1790328427095` `dabeb4b9` (d3, **S4**); independently `1790328618211` `1ece4a27` (d3, **S1**). Pointer pre-seeded in the root→S3 prompt and in S1→`edb0f8d3`'s prompt | **S3**, then S4, then S1 | **YES — three streams, same document** |
| **Starbird Boston 2013, "44:1" misinformation:correction ratio** | *Pointer* pre-seeded by the root's own reasoning `1790327877890` and written into the root→S2 and root→S7 prompts (`1790327928227`, `1790327928239`). *Number* first retrieved `1790328232437` by `1e0ef8e5` (d2, **S1**), reading the Starbird PDF | **S1** | **NO** — one stream |
| **OpenAI "Breakout Scale Category Two"** | `1790328027047` — S1 `edb0f8d3` reasoning; reached S4 via the Anthropic report (`1790328053721`) | **S1**, then S4 | partial (2 streams, different documents) |

### 4.3 Reading of the timeline
**INTERPRETATION, grounded in the numbers above.**
* Two of the five decisive items were **genuinely re-discovered** by independent streams hitting the same primary document through different queries (Botometer, OpenAI). One (USC) was **surfaced first by S4 and first verified by S1** — i.e. the report's "decisive constraint finding" was, in fact, an independent discovery by more than one strand, but the report credits only one (*"The last agent (platform propaganda / CIB) supplied the single most important negative finding"*, S1 `1790330187694`). The independence is **understated**, not overstated, in this one case.
* Two items (Foster 2012; Starbird 44:1) were **single-stream discoveries**. Neither is a multi-stream convergence.
* In both single-stream cases the *concept* was prompt-seeded even though the *document* was not: the root's H1 prompt names the Starbird/Boston case, and S1's own sub-prompt names Rauchfleisch & Kaiser.
* The **negative-finding direction** was pre-specified in all cases by at least one ancestor prompt.

---

## 5. Assertions without a producing retrieval act

**Method.** A session "asserts the decisive negative finding" if its own text or a message it sends contains one of: the arXiv id `2510.25003`; "demonstrated only in simulation"/"only in simulation"/"simulation only"; "never observed in the wild"; "no verified case of state synthetic media amplifying a specific physical incident"; "no case of AI agents engineering disruption through ambiguous physical incidents"; "no fully autonomous real-world agentic campaign". For each such session I recorded whether (a) the claim text was already in its inbound context (`user/message` / `inbox/spliced`), (b) it performed any retrieval act at all, (c) the claim appears in one of its *own* `tool/result` payloads.

**DERIVED RESULT** — 7 sessions assert it. All 7 performed retrieval; **none asserted it with zero retrieval acts.**

| Pattern | Sessions |
|---|---|
| claim was in inbound context (prompt/message) **and** session did its own retrieval **and** the evidence did *not* appear in its own results | 3 |
| claim **not** in inbound context, own retrieval, **evidence in own results** | 2 (the genuine discoverers: `cc07f9d4`/S4, `1ece4a27`/S1) |
| claim not in inbound context, own retrieval, no evidence in own results | 1 |
| claim in inbound context, own retrieval, evidence in own results | 1 |

| Stream | sessions asserting the decisive null |
|---|---|
| S1 concept genealogy | 4 |
| S6 health/military scares | 2 |
| ROOT | 1 |
| **S2, S3, S4\*, S5, S7, S8** | **0** (S4's discovery is phrased as *"simulation only"* on the coordination-risk point, not as the §7.5 constraint statement) |

**INTERPRETATION.** The "no case found" claim is *not* being parroted by sessions that never looked: only 7 sessions state it, they are concentrated in the two strands that actually searched for it (S1, S6), and both stated it after retrieving source material. The stronger form of the "propagation" worry — an assertion circulating with no retrieval behind it — **is not supported by the logs**. What *is* supported is something narrower and more consequential: the assertion existed in the draft (§3.6) and in prompts (§2.3) before it existed in the evidence chain, and only a minority of strands ever engaged with it at all.

---

## 6. Genuine disagreement and later reversals

**OBSERVATION — real, documented disagreement existed and was mostly resolved by the strand lead overriding a child.**

| # | Disagreement | Resolution | Consequence |
|---|---|---|---|
| 1 | **Reflexive control fit: HIGH or PARTIAL?** S1 `1790330060042`: *"the reflexive-control agent rates RC only **PARTIAL, not High** — because RC is human-decision-centric, deliberate, state-centric, with no AI and no emergent/self-amplifying claim. That is a narrower fit than my earlier framing implied. **I have kept RC as High** on the strength of Komov's taxonomy … but the nuance is recorded."* | **Lead overrode the specialist subagent.** The report keeps "Fit: High". | A specialist's judgment was overridden by the lead's prior, which matched the pre-written draft (§3.6). |
| 2 | **Perception management is current doctrine?** S1 `1790330060084`: *"My earlier draft implied it was. … it was DROPPED in the 8 Nov 2010 reissue … **Rating changed from Partial to POOR**."* | Self-correction, accepted | Report §3.2 downgrades it. |
| 3 | **The "2025 MISO rename" premise was inverted.** S1 `1790330060084`: *"Hegseth's 2 Dec 2025 memo renamed MISO **BACK TO PSYOP** — not MISO to 'information operations'. And it was not sudden…"* | Corrected against the parent's premise | Report corrected. |
| 4 | **Rumour is self-correcting?** S1 `1790329225787`: *"Rumour is **NOT** reliably self-correcting. Starbird's Boston data show … 44:1; the 'self-correcting crowd' is 'overly optimistic.' **I softened the brief accordingly.**"* | Self-correction | Directly contradicts a premise in the root→S2 prompt ("community self-correction"). |
| 5 | **Liddell Hart quotation.** S1 `1790329225787`: *"'Make the enemy defeat himself' is NOT verbatim Liddell Hart … **I removed the quotation marks.**"* | Self-correction | — |
| 6 | **Fabricated citations.** S1 removed/blocked Krepinevich *"Origins of Offset Strategy"*, Lefebvre *"What is Reflexive Control?"*, Chotikul 1985/ADA152240, *"Gerasimov Doctrine"*, Starbird *"Communities of Collusion"*, *"Birds of a Feather"*, a "2020 NATS/CAA Gatwick report". | Verified against primary sources | Ghost citations suppressed. |
| 7 | **NJ joint-statement date.** `5ae391ef` (S8 subtree) `1790328750117`: *"**DATE ERROR TO CORRECT IN OTHER STRANDS:** there is no verifiable '12 December 2024 joint statement' — the four-agency statement is **17 Dec 2024**."* | Propagated upward to `ac188085` and out | Cross-strand correction; demonstrates the shared workspace functioning as an error-correcting channel, not only an echo chamber. |
| 8 | **Bundestag "technische Fehlfunktionen".** S5 `1790329196325`: *"is NOT VERIFIED and should not be cited. The phrase is real but refers to UKRAINIAN drones in Finnish/Baltic airspace."* | Retracted | Removed from the report. |
| 9 | **BKA figures mis-dated.** S5: *">165 sabotage cases, 747 drone incidents … are 2026 YEAR-TO-DATE, NOT 2025."* | Corrected | — |
| 10 | **"Hide in the noise" attribution.** S5: *"traces to FPRI … and its attribution thesis concerns CHINA, not Russia; the phrase's documented coinage (Moellering, MWI 2022) means close to the opposite."* | Corrected | — |
| 11 | **"Synthetic corroboration is a belief multiplier".** S3 `findings/03-computational-propaganda.md`: *"The multi-source 'synthetic corroboration' hypothesis is **contradicted**, not merely unproven. … What survives is **trust-laundering**, not a belief multiplier."* | S3 contradicts a component; report §7.4 records it: *"one claim this study must withdraw."* | Genuine reversal of an earlier established interpretation. |
| 12 | **Anthrax hoax count.** S6 `1790329206457` retracted a circulating "~30,000" figure and the "AMI ≈$23m" cleanup figure. | Corrected against GAO/peer review | — |
| 13 | **Citation ID error.** S6 `1790329204522`: a research stream cited *"National Academies catalog ID 13163 … that ID is the Reference Manual on Scientific Evidence; the correct review is 13098."* | Corrected | — |

**INTERPRETATION.** The run contains substantial, well-documented internal contestation. It is *not* a case of unbroken sycophantic convergence: strands contradicted the parent's premises, corrected each other's dates and citations, retracted figures, and one strand explicitly declared a component of the thesis "contradicted". **The disagreements that were resolved *against* the emerging consensus are all of the same kind: factual, checkable errors (dates, IDs, dollar figures, quotations).** The one disagreement that touched the *interpretive* core — the reflexive-control fit rating — was resolved *in favour of* the lead's prior. That asymmetry is the pattern worth flagging: verification pressure was strong on facts and weak on interpretation.

---

## 7. Steelmanning the independence claim

**What would count as genuine independence, and is it present?**

| Test | Present? | Evidence |
|---|---|---|
| Different streams fetched materially different sources | **YES** | Domain Jaccard median 0.086, max 0.223 (§3.2); URL Jaccard max 0.076 (§3.3); 51–63 % of each stream's domains are unique to it (§3.1); every domain shared by ≥3 streams is search/bibliographic infrastructure (§3.4) |
| At least one decisive finding re-discovered by a second stream from a different query | **YES** | Botometer numbers: 3 streams, same sentence, independent fetches (S3 `1790328402107`, S4 `1790328496510`, S1 `1790329265636`). OpenAI reach statement: 3 streams (S3, S4, S1). USC simulation-only: S4 first (`1790328247207`), S1 verified (`1790329312163`, `1790329345660`) |
| Conclusions asserted without any retrieval behind them | **NO** | 7 asserting sessions, all with retrieval; 2 with the evidence in their own results (§5) |
| Streams contradicted each other and the parent | **YES** | 13 documented cases (§6), incl. retraction of a circulating figure, a wrong date propagated and corrected, and S3's "contradicted, not merely unproven" on synthetic corroboration |
| The conclusion was pre-written before the strands ran | **YES — this is the failure** | First 28 KB draft at `1790328052156` already contained "most likely finding … neither new nor attributable to AI", "that narrower case remains unevidenced", "The amplifier is not the botnet. It is the institution.", and the High/High fit ratings for reflexive control and SARF (§3.6) |
| Strands read that pre-written conclusion | **YES** | S1 `1790328076889`/`1790328080694`; S6 `1790328083962`; S4's child `1790328162034` |
| The single conclusion sentence was produced by | **ONE agent** | `edb0f8d3`, `1790329772457`; absent from all 21 strand briefs (§4.1) |
| The "six streams" count is real | **NO** | It is a re-scoping of six children of one strand (§1) |
| Direction of the negative finding was pre-specified | **YES, at 2 nodes** | root→S1 ("most likely finding"); S1→`edb0f8d3` and `edb0f8d3`→`1ece4a27` ("have NOT achieved sustained audience engagement"; "Note whether this is demonstrated or speculative") |
| Candidate sources were supplied rather than found | **PARTLY** | 12/191 prompts name ≥5 candidate authors; S1's prompt names 16, S2's 17, S1→`1e0ef8e5` 13, S4→`fc1be9de` 10 (§2.5). S3's and S6's prompts name almost none |

**Honest reading.** The streams were **substantially independent in their evidence-gathering and demonstrably willing to contradict each other**, but **not independent in the production of the conclusion that §7.5 attributes to them**. Those are two different things and the report conflates them. The correct statement the logs support is:

> Many strands independently assembled a large, largely non-overlapping evidence base; on that base several strands, and one agent in particular, reached a negative verdict; the report's exact conclusion sentence was written by one nested agent, was absent from seven of the eight strand briefs, and was in the draft before most strands reported.

---

## 8. Verdict

**OBSERVATION — directly in the logs, quoted.**
1. The report was first written at `1790328052156`, before the strands reported, and already contained the thesis and the fit ratings.
2. The exact conclusion phrase first appears at `1790329772457` in `edb0f8d3` (a depth-2 agent inside strand S1) and is absent from every `findings/*.md` file.
3. "Six independent evidence streams" was authored by `6f182957` (S1) about **its own six children**; the root re-labelled it "all six strands" at `1790330206846`.
4. S1 was told, in its prompt, *"the most likely finding is that most of the mechanism is already described by existing concepts"*.
5. `edb0f8d3` and `1ece4a27` were told, in their prompts, to look for OpenAI's statement *"that these operations have NOT achieved sustained audience engagement"* and to *"note whether this is demonstrated or speculative"*.
6. Three strands read the pre-strand draft of the report (`1790328076889`, `1790328083962`, `1790328162034`).

**DERIVED RESULT — with the numbers.**
7. Domain Jaccard between streams: median **0.086**, max **0.223**; path-normalised URL Jaccard: max **0.076**; **6.2 %** of distinct URLs shared; **every** domain shared by ≥3 streams is search/bibliographic infrastructure.
8. **111** inherited evidence-artefact read acts vs **522** own-file reads across the eight streams; **61** inherited reads were of sibling *analysis* files.
9. **0 of 21** strand deliverables contain the conclusion formulation.
10. **7** sessions assert the decisive null; **0** assert it with no retrieval act; only **2** have the evidence in their own results.
11. Only **1 of 191** amplification-phase prompts states a likely finding; **2 of 191** steer what (not) to conclude; **186 of 191** repeat the identical tooling block.
12. Prompt similarity: `difflib` **0.186–0.282**; verbatim boilerplate ≈ **1.1 %** of tokens; but the shared *framing* (hypothesis vocabulary, evidence-grade scheme, four-level taxonomy) is present in most prompts.

**INTERPRETATION — the judgement.**
* The **streams were not independent in the sense §7.5 claims**: the sentence "six independent evidence streams converged" describes a conclusion produced once, at depth 2, and propagated up a single branch, with the count of "six" imported from a different level of the hierarchy. As a *provenance* claim it is wrong.
* The **underlying evidence gathering was substantially independent**, and the run shows real, documented self-correction and cross-strand contradiction (§6). As an *epistemic* claim, "the negative finding is not an artefact of one search strategy" is **partly supportable**: the Botometer, OpenAI-reach and USC items were each hit by two or three streams independently. The Foster-2012 and Starbird-44:1 items were not.
* The strongest single criticism is not source-sharing but **conclusion-first structure**: the thesis, the falsification table and the concept-fit ratings existed in the draft before the research that was meant to justify them, and the strands read that draft. Agreement between draft and strands is therefore weak evidence of convergence.
* **Uncertainty:** 99 depth-4 agents (the children of depth-3 sessions) are missing from the export. Their retrieval and reasoning are invisible. Every "N of 8" count here is a lower bound on independent discovery; it is *not determinable from the logs* whether any of them independently derived the conclusion, re-derived it, or merely restated it.

**Net.** The claim "six independent evidence streams converged" is **not supported**. The defensible claim is weaker and differently worded: *a large, mostly non-overlapping evidence base was assembled by eight strands; several strands independently surfaced the same primary negatives; one nested agent composed the report's verdict sentence; and the verdict, together with the fit ratings, was present in the draft before most strands reported.* Whether the verdict is *correct* is a separate question this analysis does not address — no source was re-verified here.
