You are a research analyst. TODAY IS 25 SEPTEMBER 2026. Write your brief to `/Users/leonvanbokhorst/repos/deep-research/amplification/findings/07-counterexamples.md` and reply with a short summary.

TOOLING WARNING: `web_search` is BROKEN session-wide ("unprocessable response body"). Do not waste attempts. Use:
1. `cd /Users/leonvanbokhorst/repos/deep-research && ./tools/news.sh "query" 15` — Google News RSS (works; redirect URLs do not resolve).
2. `./tools/get.sh "URL" out.txt` — HTML to text (fails on PDFs).
3. `web_fetch` for normal HTML; PDFs via `curl` + `pdftotext`.
For academic work use OpenAlex (`https://api.openalex.org/works?search=...`), arXiv and Semantic Scholar APIs via curl.

TASK: The **disconfirming evidence**. The parent study hypothesises that AI agents could deliberately amplify ambiguous physical threats so target societies generate most of the disruption. Your job is to establish how strong the case AGAINST that hypothesis is. Be adversarial toward the hypothesis.

Cover:
1. **Failed or counterproductive influence campaigns.** Documented cases where a covert influence operation was detected, backfired, reinforced the target's position, or had negligible measurable effect. Include assessments of the Internet Research Agency's actual reach and effect, the failure modes of Doppelganger and Storm-1516, and any operation that strengthened institutional resolve.
2. **Measurement scepticism.** What do rigorous studies say about the real-world persuasive effect of exposure to misinformation and propaganda? Include: the "minimal effects" tradition; measured exposure rates to foreign influence content; the argument that most people are not exposed and those who are are already aligned; and the debate over the "backfire effect" (including its partial retraction).
3. **Prebunking and inoculation.** van der Linden, Roozenbeek and colleagues: measured effect sizes, durability, scalability, and whether platform-scale deployment has worked (e.g. Google/Jigsaw prebunking videos, the "inoculation" trials). What are the limits?
4. **Platform and state countermeasures.** Enforcement statistics, coordinated inauthentic behaviour takedowns, account removal rates, and evidence on how fast networks are detected. Include the EU DSA transparency and crisis-mechanism experience, and the UK model.
5. **Cognitive and social resilience.** Habituation to alerts, scepticism, the "cry wolf" effect, community self-correction on platforms (Community Notes/X, Wikipedia), and evidence that crowds sometimes correct rather than amplify. Also research on how rumour self-terminates.
6. **Why panic is hard to sustain.** Historical moral panics: how long did they last, what ended them, and how often did deliberate attempts to create one fail? Consider the "satanic panic", "video nasties", "knockout game" (a case widely assessed as largely media-manufactured), and "rainbow fentanyl".
7. **Institutional impermeability.** Evidence that agencies resist or discount ambiguous threat reporting, and the failure modes in the other direction (under-reaction). Discuss the trade-off honestly: the same scepticism that resists manipulation also risks ignoring real threats.
8. **The strongest version of the counter-case.** Write the best possible argument that agentic amplification is a minor concern relative to the physical threat, and state what would have to be true for it to matter.

REQUIRED OUTPUT: structured markdown, 2,000-3,000 words, effect sizes where they exist, URLs, confidence ratings, and a clear closing verdict on the **strength of the disconfirming case** (strong / moderate / weak) with reasons.

CONSTRAINTS: Analytic only, no operational guidance. Do not manufacture counter-evidence — if the disconfirming case is weak, say so.