# Provider billing reconciliation

This note closes the cost-accounting gap in the original log analysis by combining
the frozen DSH session traces with a same-day DeepSeek Platform billing export.

The raw DeepSeek CSV exports are **not committed** because they contain account and
API-key identifiers that add no analytical value. Sanitised aggregates are committed
under `analysis/data/provider-billing/`.

## Source artefacts

| source | role | SHA-256 |
|---|---|---|
| frozen research-run export | original 153-session research specimen | pinned separately in `analysis/data/manifest.json` |
| `dsh-session-session-bfad8b98-79ad-4cfa-98be-0ace111e2ba6.zip` | separate research-process analysis run | `df7b297b18fd6cd4b8e0258661d2e776855a363c9baf6235b1e4ca1f73a681f9` |
| DeepSeek Platform amount export | hourly request/token accounting | `0870d5a78f263754715d37d9168b214fa68b1116428bdaa01fe104903046b1ae` |
| DeepSeek Platform cost export | hourly billed cost | `946385bdfebbc0267be49cdcee7e054ce6eac99cb2b7929512690735834e0bf8` |

The analysis workspace starts at **2026-09-25 12:18:57.620 +02:00** (first event in
the exported root session), matching the user's recorded transition at about 12:19
local time. Its last event is **12:47:59.411 +02:00**.

## Provider prices observed in the export

DeepSeek billed `deepseek-flash` at:

| token class | USD / token | USD / 1M tokens |
|---|---:|---:|
| cache-hit input | 0.000000003 | **$0.003** |
| cache-miss input | 0.000000150 | **$0.15** |
| output | 0.000000600 | **$0.60** |

These are historical observed prices for this run, not a claim about future
DeepSeek pricing.

## Exact cross-check: analysis run vs provider

The strongest validation is the 12:00–13:00 Platform bucket. The separate analysis
export contains **398** assistant/model usage records. Its aggregate token counts
match the provider bucket **exactly**:

| | DSH analysis export | DeepSeek Platform 12:00–13:00 | difference |
|---|---:|---:|---:|
| requests | 398 | 398 | 0 |
| cache-hit input | 52,629,376 | 52,629,376 | 0 |
| cache-miss input | 551,434 | 551,434 | 0 |
| output | 358,751 | 358,751 | 0 |

Applying the provider prices to the DSH counts gives:

- cache-hit input: **$0.157888128**
- cache-miss input: **$0.082715100**
- output: **$0.215250600**
- **total: $0.455853828**

DeepSeek Platform reports **$0.455854** after rounding.

This exact agreement validates both the DSH token-field interpretation and the
provider-rate reconstruction for this environment.

The analysis run's input cache-hit rate is
**98.963%** = 52,629,376 / (52,629,376 + 551,434).

## Original research-run cost

The frozen research trace contains:

| class | tokens | observed price | reconstructed cost |
|---|---:|---:|---:|
| cache-hit input | 1,258,387,840 | $0.003 / 1M | **$3.77516352** |
| cache-miss input | 18,834,657 | $0.15 / 1M | **$2.82519855** |
| output | 9,308,857 | $0.60 / 1M | **$5.58531420** |
| **total** | **1,286,531,354** | | **$12.18567627** |

The research run's input cache-hit rate is **98.525%**. The previously reported
97.81% is the share of **all tokens including output** represented by cache reads;
it is not the input cache-hit rate.

## Why the hourly provider total is larger

The original research specimen runs from roughly **10:21 to 11:57 local time** and
sits inside two coarse provider buckets (10:00–11:00 and 11:00–12:00). Those
buckets contain:

- 10,384 provider requests
- 1,259,387,246 cache-hit input tokens
- 21,680,130 cache-miss input tokens
- 9,605,610 output tokens
- **$12.793547238** billed

The frozen research trace itself contains 10,037 model steps and lower token counts.
The residual is therefore **not attributed to the research run**:

- 347 requests
- 999,406 cache-hit input tokens
- 2,845,473 cache-miss input tokens
- 296,753 output tokens
- **$0.607870968**

The provider export is hourly and cannot identify the source of that residual.
No attempt is made to infer it.

## Two frozen specimens

For the two trace-bounded activities analysed here:

| specimen | reconstructed / verified cost |
|---|---:|
| original 153-session research run | **$12.18567627** |
| separate 4-session research-process analysis | **$0.455853828** |
| **combined** | **$12.641530098** |

The full DeepSeek Platform 10:00–13:00 account window totals **$13.249401066**.
The difference, **$0.607870968**, is the unattributed residual above.

## What this changes

The original analysis could only describe cache economics using hypothetical
discounts because billing information was absent from the session export. The
provider data now lets us replace that with observed historical cost.

The result is more striking than the hypothetical calculation: the research system
processed **1.277B logical input tokens**, while only **18.8M** were cache misses.
The provider charged roughly **$12.19** for the full frozen research run.

That figure should be read as an empirical property of this specific combination of
DSH, `deepseek-flash`, its prefix/cache behaviour, and DeepSeek's prices on
25 September 2026 — not as a general cost claim for recursive agent research.
