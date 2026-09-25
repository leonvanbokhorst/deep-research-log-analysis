# DSH research-process analysis

An empirical reconstruction of a completed DSH recursive research run
(25 September 2026, 153 sessions, 1.29B tokens, 96 minutes), asking:

> **How does large-scale recursive agent delegation affect the quality, diversity,
> redundancy, correction, traceability, and cost of open-ended research?**
>
> **When does more research become more knowledge, and when does it become more
> confidence?**

This workspace is the **analysis**. It is not part of the research corpus.

---

## Start here

**[`analysis/00-synthesis.md`](analysis/00-synthesis.md)** — the synthesis report:
what the scale bought, what it did not buy, and what the run teaches about recursive
agent research.

---

## Files

### Reports

| file | contents |
|---|---|
| [`analysis/00-synthesis.md`](analysis/00-synthesis.md) | final synthesis |
| [`analysis/01-corpus-manifest-and-schema.md`](analysis/01-corpus-manifest-and-schema.md) | manifest, hashes, event schema, token semantics, reconstruction limits |
| [`analysis/02-agent-genealogy.md`](analysis/02-agent-genealogy.md) | delegation tree, branch table, influence, termination |
| [`analysis/03-token-and-cache-tables.md`](analysis/03-token-and-cache-tables.md) | token classes and cache behaviour |
| [`analysis/04-contribution-mapping.md`](analysis/04-contribution-mapping.md) | report sections → branches; falsification as contribution |
| [`analysis/05-independence-and-convergence.md`](analysis/05-independence-and-convergence.md) | test of the "six independent evidence streams" claim |
| [`analysis/06-anomalies-and-unexpected-behaviour.md`](analysis/06-anomalies-and-unexpected-behaviour.md) | 12 anomalies |
| [`analysis/07-marginal-return-and-stopping.md`](analysis/07-marginal-return-and-stopping.md) | diminishing returns and stopping rules |
| [`analysis/notes/corrections.md`](analysis/notes/corrections.md) | forensic reconstruction of ~20 corrections |
| [`analysis/notes/independence.md`](analysis/notes/independence.md) | full independence analysis |
| [`analysis/notes/validation.md`](analysis/notes/validation.md) | verification of the delegated analyses |

### Data

`analysis/data/` — 19 derived datasets, including `manifest.json` (SHA-256 of every
corpus file), `genealogy.json`, `sessions.csv`, `edges.csv` (with full spawn
prompts), `usage_steps.csv`, `toolcalls.csv`, `io_acts.csv`, `fileprovenance.csv`,
`messages.csv`, `queries.csv`, `targets.csv`, `retrieval.csv`,
`correction_candidates.csv`.

`analysis/tables/` — 14 rollup tables, including `branch_table.csv`,
`cache_by_depth.csv`, `cache_timeline.csv`, `discovery_by_work.csv`,
`message_flow.csv`, `agent_productivity.csv`, `stopping_signals.csv`,
`redundancy.csv`, `host_reuse.csv`, `contribution.csv`.

`analysis/work/` — intermediate outputs from the delegated marginal-return analysis
(`findings_inventory.csv`, `decile_series.csv`, `marginal_by_phase.csv` and raw
probe JSON).

### Tools

`analysis/tools/` — 21 reproducible scripts. The pipeline:

```
corpus.py        shared loader (read-only over the immutable export)
manifest.py      hashes + schema inventory        -> data/manifest.json
extract.py       sessions/edges/usage/toolcalls   -> data/{sessions,edges,usage_steps,toolcalls}.csv
sources.py       retrieval acts + URLs            -> data/{retrieval,url_mentions,hosts}.csv
io_classify.py   shared-workspace I/O graph       -> data/{io_acts,fileprovenance}.csv
messages.py      agent-to-agent message channel   -> data/messages.csv
discovery.py     source discovery + redundancy    -> tables/{discovery_by_work,redundancy,host_reuse}.csv
analyze.py       genealogy, cache, timing         -> data/genealogy.json, tables/*.csv
stopping.py      phases, productivity, stopping   -> tables/{phases,stopping_signals,agent_productivity}.csv
contribution.py  report sections -> branches      -> tables/{contribution,branch_outputs}.csv
corrections.py   mechanical correction surface    -> data/correction_candidates.csv
```

Plus `grepcorpus.py`, `count_sessions.py`, `window.py`, `dump.py`, `timeline.py`,
`findings_inventory.py`, `deciles.py`, `marginal.py`, `probes.py`, `show_hits.py`
(written during the delegated analyses).

### The immutable corpus

`dsh-session-session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357/` — the exported session
logs (153 JSONL files, 281 MB). **Never modified.** Every hash is in
`analysis/data/manifest.json`.

The original research workspace (`/Users/leonvanbokhorst/repos/deep-research`) is
used for comparison only and is hashed in
`analysis/data/external_artifacts.json`.

---

## What is *not* in version control

Two categories are deliberately excluded (see `.gitignore`):

1. **The corpus export** (269 MB). It is externally-supplied source data rather than
   authored work. It is fully pinned — SHA-256, byte size and line count for all 153
   files — in `analysis/data/manifest.json`, which **is** committed, so the analysed
   object is identified even though it is not shipped. To restore, place the export
   back in this directory and run `python3 analysis/tools/manifest.py` to verify
   every hash.
2. **Large regenerable intermediates** in `analysis/work/` (`tl_*.jsonl`,
   `retrieval_acts.json`, `spawns*.json` and similar). The curated summaries beside
   them — `findings_inventory.csv`, `decile_series.csv`, `marginal_by_phase.csv` —
   are committed.

**Consequence for reproduction.** The scripts in `analysis/tools/` need the corpus,
so a fresh clone cannot regenerate `analysis/data/` until the export is restored.
The committed datasets and tables are sufficient to check every number quoted in
the reports without re-running anything.

---

## Three findings worth knowing before reading anything else

1. **The "six independent evidence streams" were six sibling sub-agents of one
   branch**, and the report's conclusion sentence was written by one depth-2 agent,
   21 minutes *before* the paper the report calls its most important constraint
   finding arrived. See [`05`](analysis/05-independence-and-convergence.md).

2. **Recursion did not stop from diminishing returns — it hit a depth cap.** 99
   fully-written spawn attempts were refused with `depth 4 exceeds maxDepth 3`. See
   [`06`](analysis/06-anomalies-and-unexpected-behaviour.md) §A1.

3. **The dominant channel between agents was messages, not files.** Any analysis
   that counts artefact reads will declare 86 of 168 deliverables "orphaned" and be
   wrong. See [`06`](analysis/06-anomalies-and-unexpected-behaviour.md) §A2.

## Reproducing

```bash
cd analysis/tools
python3 manifest.py && python3 extract.py && python3 sources.py \
  && python3 io_classify.py && python3 messages.py && python3 discovery.py \
  && python3 analyze.py && python3 stopping.py && python3 contribution.py \
  && python3 corrections.py
```

All scripts are deterministic and read-only with respect to the corpus.
