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

## 6. The economics of cache-enabled scaling — provider reconciled

A same-day DeepSeek Platform export was added after the original log analysis.
The raw provider files are kept private because they contain account/API-key
identifiers; sanitised hourly aggregates and the full reconciliation are in
[`08-provider-billing-reconciliation.md`](08-provider-billing-reconciliation.md).

**OBSERVATION — prices actually billed on 25 September 2026:**

| token class | observed price |
|---|---:|
| cache-hit input | **$0.003 / 1M tokens** |
| cache-miss input | **$0.15 / 1M tokens** |
| output | **$0.60 / 1M tokens** |

**DERIVED RESULT — exact provider cross-check on the separate analysis run.**
The frozen 4-session analysis export contains 398 model-usage records:
52,629,376 cache-hit input tokens, 551,434 cache-miss input tokens and 358,751
output tokens. DeepSeek Platform's 12:00–13:00 bucket reports **exactly the same
398 requests and the same three token counts**. Applying the provider prices gives
$0.455853828; the provider reports the same value.

That exact match validates the DSH field interpretation used throughout this report.

**DERIVED RESULT — original research-run cost.** Applying those observed provider
prices to the frozen 153-session research trace:

| class | tokens | cost |
|---|---:|---:|
| cache-hit input | 1,258,387,840 | **$3.77516352** |
| cache-miss input | 18,834,657 | **$2.82519855** |
| output | 9,308,857 | **$5.58531420** |
| **total** | **1,286,531,354** | **$12.18567627** |

The input cache-hit rate is **98.525%**:
`cacheRead / (cacheRead + freshInput)`. The earlier 97.81% figure is the share of
*all tokens including output* that consists of cache reads; it is not the prompt
cache-hit rate.

**INTERPRETATION.** The run's logical scale is therefore not merely large but
economically unusual: 1.277B logical input tokens were processed while only 18.8M
were billed as cache misses. Under the observed DeepSeek pricing, the frozen research
run cost about **$12.19**.

This does not make scale epistemically valuable by itself. The same cheap reuse that
made broad fan-out feasible also made late re-synthesis cheap. Cache architecture is
a feasibility condition, not evidence of research quality.

**BOUNDARY.** DeepSeek's 10:00–12:00 hourly account buckets are slightly larger than
the frozen research trace because they include activity outside the trace boundary.
Those residual requests/tokens are deliberately not attributed to the research run.
The exact reconciliation is documented in report 08.

## 7. Limitations

1. **Cache writes and latency remain absent from the DSH session export.** Prices and billed cost are supplied by a separate same-day DeepSeek Platform export and reconciled in report 08; the session logs alone still cannot provide monetary cost.
2. **Context size is inferred**, not reported. `inputTokens + cacheReadTokens` is
   the prompt length, which is a lower bound on position in the window.
3. **Reasoning text is unevenly retained**, though reasoning *tokens* are complete
   (30.9% of output).
4. **Three step records lack an assistant message** (the three `assistant/attempt`
   records); 10,040 `step/start` vs 10,037 `assistant/message`. No unexplained step
   loss — an earlier draft of this analysis wrongly claimed a 5,680-step gap; the
   check did not support it and the claim was removed.
