# Corpus manifest and schema

**Scope of this document.** This describes the *primary dataset* — the exported DSH
session logs of a completed research run — and the derived tables built from it.
It states what can and cannot be reconstructed. It is deliberately written before
any interpretive conclusion.

---

## 1. What the corpus is

The corpus is a directory export of one DSH (DeepSeek Harness) research session
and its full recursive delegation subtree:

```
dsh-session-session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357/
  session.v3.jsonl                        the root session
  subagents/<session-id>/session.v3.jsonl  152 descendant sessions
```

| Property | Value |
|---|---|
| Session files | 153 (1 root + 152 subagents) |
| Total size | 281,391,742 bytes (268.3 MiB) |
| Total lines (JSONL records) | 67,072 |
| Format | JSONL, DSH session format `version: 3` |
| Root session id | `session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357` |
| Root working directory | `/Users/leonvanbokhorst/repos/deep-research` |
| Root agent preset (declared) | `research-mentor`, overridden at seq 3 to `standard` |
| Provider / model | `deepseek-official` / `deepseek-flash`, reasoning effort `high` (every one of 10,037 assistant steps) |
| Declared context window | 1,000,000 tokens |
| Wall clock (event timestamps) | ≈96 minutes |
| Delegation depth reached | 3 |
| Hash algorithm | SHA-256, per file, recorded in `data/manifest.json` |

Per-file sizes, line counts and SHA-256 digests are in
[`../data/manifest.json`](../data/manifest.json). The complete per-event-type
schema inventory is in the same file under `eventSchemas`.

**Immutability.** No file inside the export was modified. Every derived artefact
in `analysis/` was produced by read-only passes over it. The analysis workspace
itself (`/Users/leonvanbokhorst/repos/deep-research-log-analysis`) is *not* part
of the research corpus, and neither is the original research workspace
(`/Users/leonvanbokhorst/repos/deep-research`) — the latter is used only for
comparison, and is separately identified in
[`../data/external_artifacts.json`](../data/external_artifacts.json).

---

## 2. Record schema (observed)

Every line is one JSON object with `type`, `seq`, `time` (epoch ms) and `data`.
The corpus contains exactly 25 event types. Full key paths are in
`manifest.json → eventSchemas`; here is what each is and what it is good for.

### Session framing (once per file)

| Type | Count | Meaning |
|---|---|---|
| `session` | 153 | Header. `id`, `createdAt`, `cwd`, `parentSession`, `delegationDepth`, `origin`, `agentPreset` |
| `subagent/descriptor` | 152 | Present in subagent files only: `label`, `mode`, `provider`, `agentProvider`, `agentModel`, `agentReasoningEffort` |
| `subagent/catalog` | 152 | Present in **parent** files: `childId`, `childCreatedAt`, `label`, `mode`. **This is the authoritative spawn record** |
| `request/header` | 154 | Serialised LLM request header: provider, model, reasoningEffort, maxTokens, full tool JSON schema |
| `request/context` | 153 | provider, model, `contextWindow` |
| `system/message` | 153 | The full system prompt delivered to that session |
| `session/title` | 153 | Auto-title, with `source.kind` (e.g. `fallback`) |
| `sandbox/mode`, `approval/policy` | 153 each | Per-session sandbox/approval configuration |
| `permission/preset`, `agent-preset/selected` | 1 each | Root only |

### Turn and step structure

| Type | Count | Meaning |
|---|---|---|
| `turn/start` / `turn/end` | 190 / 189 | A user- or agent-driven turn. `turn/end.data.reason.kind` gives the termination reason |
| `step/start` / `step/end` | 10,040 each | One model invocation. 10,037 of these have a matching `assistant/message`; the 3 without one correspond to the 3 `assistant/attempt` records |
| `assistant/message` | 10,037 | The model output: `message.content[]` of `text` / `reasoning` / `tool-call`, plus **`usage`** |
| `tool/call` | 16,195 | `name`, `arguments` (a JSON *string*), `callId`, turn/step |
| `tool/result` | 16,195 | Result text at `message.content[0].content[0].text`; may carry `meta` with structured `sources`, `lines`, `diffs`, `statusCode`, `error` |
| `assistant/attempt` | 3 | A retried/failed model attempt — the only step-start records without a completed assistant message |
| `session/end-seed` | 1 | Marks an end-of-seed boundary in one subagent |

### Inter-agent and user traffic

| Type | Count | Meaning |
|---|---|---|
| `user/message` | 938 | 10,037 assistant steps produced 16,195 tool calls, but tool results are **not** stored as `user/message` records here; all 938 `user/message` records carry no `source` field. They are the initial human prompt (once) plus agent-injected content |
| `agent/inbox/spliced` | 1,166 | **Messages spliced into a session's context.** `data.target` is `next-turn` or `next-step`; `inserted[].source` may carry `senderSessionId`, `kind`, `form`, `plugin`, `summary`. `removedCount` records context edits. **374** of the spliced messages carry a `senderSessionId` (genuine agent-to-agent traffic); the remainder are prompts and tool-adjacent insertions |

### Tooling and observability

| Type | Count | Meaning |
|---|---|---|
| `web/deepseek-search-llm-request` | 345 | The outbound call the built-in `web_search` tool makes: `endpoint`, `body.model`, the search query |
| `todo/write` | 196 | The session's self-managed todo list (a proxy for stated plan) |
| `deliverables/presented` | 159 | Files a session declared as deliverables, with a description |
| `session/title` | 153 | see above |

---

## 3. Token accounting — exact semantics

`assistant/message.data.usage` has exactly five integer fields:
`inputTokens`, `cacheReadTokens`, `outputTokens`, `reasoningTokens`, `totalTokens`.

DSH's own mapping (verified in the installed harness at
`@deepseek-ai/dsh-llm-deepseek/lib/index.js`, `mapUsage`) is:

```js
inputTokens    = prompt_tokens - cache_read_tokens   // the UNCACHED prompt
cacheReadTokens = prompt_cache_hit_tokens            // the CACHED prefix
outputTokens   = completion_tokens
totalTokens    = prompt_tokens + completion_tokens
```

**DERIVED RESULT.** `inputTokens + cacheReadTokens + outputTokens == totalTokens`
holds in **10,037 of 10,037** steps (0 exceptions). Therefore:

- **logical input processed** = `inputTokens + cacheReadTokens`
- **uncached (fresh) input** = `inputTokens`

### What is *not* recorded

| Wanted | Status |
|---|---|
| Cache **write** / cache-creation tokens | **Absent.** The export contains only one cache field (`cacheReadTokens`, 676 literal occurrences). No `cache_creation`, `cache_write` or `prompt_cache_miss` field exists anywhere in the corpus. Cache writes cannot be separated from uncached input, and cannot be counted. |
| Per-request latency | **Absent** — no start/end per model call is recorded; `step/start` and `step/end` carry no timestamps of their own, only the wrapping `assistant/message` does. |
| Prices / billed cost | **Absent** — no monetary field exists. The cost analysis is therefore expressed in token classes only, with pricing left as an explicit assumption. |
| Cache TTL / eviction events | **Absent.** |
| Provider-side request ids | **Absent.** |

This bounds the cache analysis: it can measure **cache reads** and **uncached
input** precisely, and can measure how the *ratio* evolves. It **cannot** measure
cache writes, so it cannot compute a true cache hit rate over attempted reads, nor
net cost.

---

## 4. What can be reconstructed reliably

| Reconstructable | Basis | Confidence |
|---|---|---|
| Full delegation tree (parent → child) | `session.parentSession` **and** `subagent/catalog.childId` — the two agree for all 152 edges, 0 mismatches | High |
| Delegation depth | `session.delegationDepth` (0/1/2/3) | High |
| Branch labels | `subagent/descriptor.label` | High |
| Exact child prompt | `tool/call.name == "subagent"` → `arguments.prompt` | High |
| Every tool call and its result text | `tool/call` + `tool/result` joined on `callId` | High |
| Token classes per step | `assistant/message.usage` | High (verified arithmetic) |
| Timing / ordering | `time` fields, monotone within a file and consistent across files | High *for ordering and intervals* |
| Agent-to-agent messages | `agent/inbox/spliced` with `source.senderSessionId` | High |
| Shared-file read/write graph | tool arguments naming absolute workspace paths | Medium — depends on path-extraction heuristics |
| Which urls each session retrieved | `web_fetch`/`web_search` args + shell `curl`/`wget` args + `tool/result.meta.sources` | Medium-High for explicit args; Medium for shell-derived |

## 5. What cannot be reconstructed, or only weakly

1. **Reasoning content is not always present.** `assistant/message.content` may
   contain `reasoning` blocks; where a provider omits them the internal rationale
   is invisible. Measured reasoning-token share is 30.9% of output tokens, but the
   *text* of that reasoning is unevenly retained.
2. **Retrieval *outcomes* are noisy.** 1,361 `web_fetch` calls and 6,458 shell
   retrieval acts exist, but the result text frequently contains navigation
   chrome, cookie banners and sitemap boilerplate. URL counts taken from raw
   result text are inflated; only `tool/result.meta.sources` (152 records) is
   clean, and it is too sparse to carry the whole analysis.
3. **The step ledger is nearly complete.** `step/start` = `step/end` = 10,040,
   `assistant/message` = 10,037, `assistant/attempt` = 3. The three missing
   assistant messages are exactly the three retried attempts. **No unexplained
   step loss** — this was checked because an earlier draft of this analysis
   wrongly asserted a 5,680-step gap, which the verification did not support.
4. **Context *size* is only inferable.** The provider does not emit a context
   length. `logical input` (= `inputTokens + cacheReadTokens`) is the best proxy
   because the full prompt is re-sent each step — but it counts the prompt, not
   the model's position in it, and it is a lower bound on true context.
5. **Cost** cannot be computed: no prices, no cache-write counts, no billing data.
6. **Absolute wall-clock time is ambiguous.** `session.createdAt` is offset from
   the `time` field of that session's own first events by ≈2 h in the root file,
   so absolute UTC is unreliable. All timing in this analysis is therefore
   reported as **intervals and orderings**, which are internally consistent.
7. **Claim-level truth is not in the corpus.** The logs record what agents
   asserted and what they retrieved. They do not record whether an assertion is
   *true*. Every "correction" in this analysis is a correction *within the run*
   (an assertion the run itself later contradicted), not a judgement of fact by
   this analysis.

## 6. Derived tables

All in [`../data/`](../data/) and [`../tables/`](../tables/). Every table is
regenerable byte-identically from the tools in [`../tools/`](../tools/).

| File | Rows | What it is |
|---|---|---|
| `data/manifest.json` | 153 files | hashes, sizes, per-type schema inventory |
| `data/sessions.csv` | 153 | per-session rollup: depth, label, counts, token classes, max context |
| `data/edges.csv` | 152 | parent → child, with the full spawn prompt and label |
| `data/usage_steps.csv` | 10,037 | per-step token classes and character volumes |
| `data/toolcalls.csv` | 16,195 | every tool call with normalised arguments |
| `data/genealogy.json` | — | tree + per-node metrics + totals |
| `data/io_acts.csv` | 16,195 | every tool call classified by shared-workspace I/O |
| `data/io_matrix.csv` | 153 | per-session I/O class mix |
| `data/fileprovenance.csv` | 642 | per shared path: writers, readers, cross-session inheritance count |
| `data/retrieval.csv` | 8,217 | every evidence-retrieval act with error heuristics |
| `data/queries.csv` | 3,155 | every search query extracted, normalised |
| `data/targets.csv` | 13,772 | every retrieval target URL/host |
| `data/meta_sources.csv` | 152 | clean structured `meta.sources` records |
| `data/cache_timeline.csv` | 20 | token classes per equal-count bin of model steps |
| `data/correction_candidates.csv` | 971 | mechanically surfaced correction language |
| `tables/branch_table.csv` | 16 | per depth-1 branch subtree rollup |
| `tables/cache_by_depth.csv` | 4 | token/cache composition by depth |
| `tables/discovery_by_work.csv` | 10 | source discovery per decile of model work |
| `tables/host_reuse.csv` | 1,634 | hosts and how many sessions targeted them |
| `tables/redundancy.csv` | 2,416 | repeated queries across sessions |
| `tables/marginal_return.csv` | 10 | novelty proxies per decile (act-ordered) |
| `tables/correction_artifacts.csv` | 2 | filenames signalling retraction |
