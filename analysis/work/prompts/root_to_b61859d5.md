You are a research analyst. TODAY IS 25 SEPTEMBER 2026. Write your brief to `/Users/leonvanbokhorst/repos/deep-research/amplification/findings/03-computational-propaganda.md` and reply with a short summary.

TOOLING WARNING: `web_search` is BROKEN session-wide ("unprocessable response body"). Do not waste attempts. Use:
1. `cd /Users/leonvanbokhorst/repos/deep-research && ./tools/news.sh "query" 15` — Google News RSS (works; redirect URLs do not resolve).
2. `./tools/get.sh "URL" out.txt` — HTML to text (fails on PDFs).
3. `web_fetch` for normal HTML.
4. PDFs: `curl -sL -o /tmp/x.pdf "URL" && pdftotext -layout /tmp/x.pdf /tmp/x.txt`.
Find publisher URLs via site search (`https://site/?s=query`) or sitemaps. Platform transparency reports are often at predictable URLs.

TASK: The state of evidence on **covert influence operations and coordinated inauthentic behaviour, 2023-2026**, with emphasis on whether AI has changed the mechanism rather than just the volume.

Investigate:
1. **Storm-1516** (Russian-linked; fake videos, fabricated whistleblowers, persona networks) — what it did, how it was detected, what Microsoft/Recorded Future/Alethea/Clemson found, and its measured reach. Also **Doppelganger** (and its 2024 takedown by the US DOJ), **Spamouflage/Dragonbridge**, **Operation Overload**, **Matryoshka**, and **Portal Kombat** (Viginum's findings).
2. **Platform and lab threat reports**: OpenAI's "Influence and Cyber Operations" reports (2024, 2025, 2026), Meta's Adversarial Threat Reports, Google Threat Analysis Group, X, and Anthropic's threat intelligence reports. What AI-enabled influence activity have they actually caught? How capable was it? Any agentic/automated behaviour described?
3. **Commercial influence-for-hire**: private firms selling coordinated manipulation, "PR firms" running astroturfing, the market for fake engagement, and any documented cases.
4. **Effectiveness evidence**: what is actually known about the reach and persuasive effect of these campaigns? Look for academic measurement studies (e.g. on the Internet Research Agency's real reach), platform data, and sceptical assessments. Also evidence that campaigns were **ineffective** or counterproductive.
5. **Persona management and synthetic corroboration**: documented cases of long-running fake personas, fabricated "independent" experts or eyewitnesses, fake local news sites (NewsGuard's tracking of AI-generated news sites), and networks presenting one source as many. This is the most important section for the parent study — be thorough.
6. **Detection and takedown**: how networks are found (behavioural signals, infrastructure, stylometry, platform integrity teams), and how quickly. Include coordinated inauthentic behaviour enforcement statistics.
7. **Where the evidence is thin**: explicitly flag any claim that AI has qualitatively changed influence operations without measurement behind it.

REQUIRED OUTPUT: structured markdown, 2,000-3,000 words, source URLs, confidence ratings, separating **demonstrated** from **claimed** from **inferred**. Include a table of cases with actor, method, AI involvement, measured effect, and detection.

CONSTRAINTS: Analytic only. Do NOT provide operational guidance for running any influence campaign. Describe methods only at the level needed to assess capability and defence.