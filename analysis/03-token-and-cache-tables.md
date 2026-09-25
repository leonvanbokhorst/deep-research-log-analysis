# Token usage and provider-cache behaviour

Data: [`data/usage_steps.csv`](data/usage_steps.csv) (10,037 rows, one per model
step), [`tables/cache_by_depth.csv`](tables/cache_by_depth.csv),
[`data/cache_timeline.csv`](data/cache_timeline.csv).

---

## 1. Field semantics (established, not assumed)

**OBSERVATION — verified against the installed harness.**
`@deepseek-ai/dsh-llm-deepseek/lib/index.js`, function `mapUsage`:

```js
inputTokens     = prompt_tokens - cache_read_tokens   // UNCACHED prompt
cacheReadTokens = prompt_cache_hit_tokens             // CACHED prefix
outputTokens    = completion_tokens
totalTokens     = prompt_tokens + completion_tokens
```

**DERIVED RESULT.** `inputTokens + cacheReadTokens + outputTokens == totalTokens`
holds in **10,037 of 10,037** steps, with zero exceptions. Therefore
**logical input processed = `inputTokens + cacheReadTokens`**, and `inputTokens` is
the count of tokens the provider had to process *without* a cache hit.

**OBSERVATION — cache *writes* are not recorded.** The corpus contains exactly one
cache field. A raw-text search for `cache_creation`, `cache_write`,
`prompt_cache_miss` or any related key across all 153 files returns nothing. Prices,
billing and latency are likewise absent. **No true cache-hit rate and no monetary
cost can be computed from this export.** Everything below is in token classes.

---

## 2. Headline composition

**DERIVED RESULT — whole run:**

| class | tokens | share of total |
|---|---|---|
| cache reads | **1,258,387,840** | **97.81%** |
| uncached (fresh) input | 18,834,657 | 1.46% |
| output | 9,308,857 | 0.72% |
| reasoning (subset of output) | 2,875,281 | 30.9% of output |
| **total** | **1,286,531,354** | 100% |

**DERIVED RESULT.** Logical input processed = **1,277,222,497 tokens**.
Cache-read-to-fresh-input ratio = **66.8×**.

**INTERPRETATION.** The run processed 1.28 **billion** logical input tokens while
introducing only 18.8 **million** tokens of content the provider had not already
seen — a ratio of roughly **68 fresh tokens per 1,000 logical tokens**. Whatever
this run cost, almost none of it was spent on re-reading new material.

---

## 3. The two caching mechanisms

**DERIVED RESULT — a shared, cross-session prefix.** All 153 sessions were given
**byte-identical** system prompts (one distinct SHA-256 across 153 files; 6,897
characters each) and **byte-identical** tool-schema blocks (one distinct hash across
154 `request/header` records).

**DERIVED RESULT — the cache is warm at the very first step of every subagent.**
The first assistant step of each session:

| | value |
|---|---|
| first-step logical context, all sessions | min 10,277 / median 10,858 / max 12,036 |
| first-step **cache read** — 152 of 153 sessions | **exactly 7,936** |
| first-step **cache read** — the root only | 1,280 |
| first-step fresh input, median | 2,905 |
| sessions with zero first-step cache read | **0** |

**OBSERVATION.** 7,936 tokens is a constant, identical across all 152 subagents at
every depth, and the root — which ran first, cold — read only 1,280. This is the
shared system-prompt-plus-tool-schema prefix being served from provider cache.

**DERIVED RESULT — the second mechanism is in-session context accumulation.** Each
session re-sends its own growing conversation every step. Across the run, the root
re-read its own context 369 times over (129.6M cache reads against 351K fresh
input tokens); the most context-heavy branch (`Health and military scare cases`)
84×; `Concept genealogy` 144×.

**INTERPRETATION.** Recursive delegation benefits from cache in a way that ordinary
long-context work does not, because **every new agent inherits a prefix that is both
large and already hot**. 152 separate sessions started warm at ~7,900 cached tokens
each — a benefit unavailable to a single cold session and one that scales with the
number of agents. The mechanism is: one prompt brief → many sessions → all hit the
same prefix.

---

## 4. Cache behaviour by delegation depth

**DERIVED RESULT** (`tables/cache_by_depth.csv`):

| depth | sessions | steps | total tokens | tokens/session | cache reads | fresh input | cache-hit % | output share |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 338 | 130,220,004 | 130,220,004 | 129,582,592 | 351,381 | **99.73%** | 0.22% |
| 1 | 16 | 1,543 | 249,647,052 | 15,602,941 | 245,680,128 | 2,448,687 | 99.01% | 0.61% |
| 2 | 45 | 3,474 | 474,060,261 | 10,534,672 | 464,243,328 | 6,544,438 | 98.61% | 0.69% |
| 3 | 91 | 4,682 | 432,604,037 | 4,753,891 | 418,881,792 | 9,490,151 | 97.78% | 0.98% |

**DERIVED RESULT — two countervailing trends.**

1. **Cache-hit rate falls slightly with depth** (99.73% → 97.78%), because deeper
   agents spend proportionally more of their tokens on genuinely new content: fresh
   input per depth-3 session is ~104,000 tokens, against ~351,000 for the single
   root but spread over 4.75M total rather than 130M.
2. **Fresh input is concentrated at the leaves.** Depth-3 sessions account for
   **9,490,151 of the run's 18,834,657 fresh input tokens — 50.4%** — while
   constituting 60% of all sessions.

**INTERPRETATION.** The leaves are where new information actually entered the
system, and they are also the most token-efficient per session (4.75M tokens each
vs 130.2M for the root). This is consistent with the productivity finding
(`06-anomalies-and-unexpected-behaviour.md` §A2): the deepest layer was doing the
most genuinely new reading per token, even though a majority of its sessions
produced nothing another session read.

---

## 5. Cache behaviour over time

**DERIVED RESULT** (`data/cache_timeline.csv`, 20 equal-count bins of assistant
steps):

| bin | steps | sessions active | fresh input | cache reads | cache-hit % | mean depth | context/step |
|---|---|---|---|---|---|---|---|
| 1 | 501 | 34 | 1,679,735 | 18,215,552 | 91.56% | 1.63 | 39,711 |
| 2 | 502 | 44 | 2,230,862 | 43,540,608 | 95.13% | 2.05 | 91,178 |
| 3 | 502 | 42 | 887,223 | 47,966,720 | 98.18% | 2.32 | 97,319 |
| 4 | 502 | 38 | 576,637 | 68,289,792 | 99.16% | 2.21 | 137,184 |
| 5 | 502 | 31 | 457,886 | 83,547,776 | 99.45% | 2.00 | 167,342 |
| 6 | 502 | 65 | 1,153,589 | 51,289,728 | 97.80% | 1.63 | 104,469 |
| 7 | 501 | 80 | 1,735,825 | 16,739,328 | **90.60%** | 2.54 | **36,877** |
| 8 | 502 | 75 | 1,408,386 | 32,351,104 | 95.83% | 2.52 | 67,250 |
| 9–16 | — | 71–94 | 1,405,631 → 596,845 | 37,313,408 → 84,898,304 | 96.4 → 99.3% | ~2.4–2.5 | 77,130 → 170,309 |
| 17 | 502 | 54 | 431,305 | 91,147,008 | 99.53% | 2.27 | 182,427 |
| 18 | 502 | 47 | 403,998 | 102,512,384 | 99.61% | 2.19 | 205,013 |
| 20 | 502 | 20 | 468,369 | 103,115,136 | **99.55%** | 1.77 | **206,342** |

**OBSERVATION — the batch boundary is visible as a cache reset.** Bin 7 shows cache
hit rate dropping to **90.60%** and context-per-step collapsing to **36,877**
(from 167,342 in bin 5) — because batch 2's 8 new branches and their children
started fresh contexts on the shared prefix. It then recovers monotonically as those
contexts fill.

**DERIVED RESULT.** By the last bin, **99.55%** of all input is served from cache and
each step processes ~206K logical tokens, of which ~940 are fresh. **Fresh input per
step falls roughly 4× from the first bin to the last** (3,352 → 933) while output
per step *rises* (546 → 1,059).

**INTERPRETATION.** Late in the run the system was overwhelmingly **regenerating
text from context it already held**, not reading new material — consistent with the
discovery-decay finding in `07-marginal-return-and-stopping.md`. High cache
efficiency is not evidence of value; it is the signature of a process whose
marginal input has collapsed.

---

## 6. The economics of cache-enabled scaling

**DERIVED RESULT.** Cost reduction depends entirely on the cache-read discount,
which is not in the data. Under three illustrative discounts:

| assumed cache-read price (vs fresh) | input-equivalent tokens, no cache | with cache | reduction |
|---|---|---|---|
| 1/5 | 1,277,222,497 | 270,512,225 | 78.8% |
| 1/10 | 1,277,222,497 | 144,673,441 | 88.7% |
| 1/20 | 1,277,222,497 | 81,754,049 | **93.6%** |

**DERIVED RESULT — cost scales with agent count, not with tree size.** Because each
new agent starts warm, the marginal cost of one more depth-1 branch is dominated by
its *own* accumulated context and output, not by a cold prefix. The distribution is
therefore unusually favourable to fan-out: 130M of the run's 1.286B tokens (10.1%)
were spent in the root, and the remaining 90% bought 152 agents.

**INTERPRETATION — what cache made feasible, stated carefully.**

- The run's *logical* volume (1.28B input tokens) would be impractical to recompute
  at full price. Serving 97.8% of it from cache is very likely the condition that
  made a 153-agent, 96-minute run affordable at all.
- But **cache efficiency is not an argument for scale**. The same mechanism that
  makes fan-out cheap also makes *re-synthesis* cheap, which is why the late run
  could produce 81 new artefacts from an exhausted source pool without the volume
  showing up as new knowledge.
- The 7,936-token shared prefix is the clearest lever: it is paid once per agent
  and is identical for all of them. A run that varies its system prompt or tool set
  per branch would forfeit it.

**Explicitly not computable.** No money figure is offered. Cache writes are
unrecorded, so the cache-fill cost — plausibly the dominant term for short-lived
sessions — cannot be estimated. A session that writes 300K tokens of context and
reads it back 8 times may be *net negative* on caching, and this export cannot
distinguish that case.

---

## 7. Limitations

1. **Cache writes, prices, latency absent** — see §1. No cost claim is made.
2. **Context size is inferred**, not reported. `inputTokens + cacheReadTokens` is
   the prompt length, which is a lower bound on position in the window.
3. **Reasoning text is unevenly retained**, though reasoning *tokens* are complete
   (30.9% of output).
4. **Three step records lack an assistant message** (the three `assistant/attempt`
   records); 10,040 `step/start` vs 10,037 `assistant/message`. No unexplained step
   loss — an earlier draft of this analysis wrongly claimed a 5,680-step gap; the
   check did not support it and the claim was removed.
