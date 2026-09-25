You are a research analyst. TODAY IS 25 SEPTEMBER 2026. Write your brief to `/Users/leonvanbokhorst/repos/deep-research/amplification/findings/04-agentic-capability.md` and reply with a short summary.

TOOLING WARNING: `web_search` is BROKEN session-wide ("unprocessable response body"). Do not waste attempts. Use:
1. `cd /Users/leonvanbokhorst/repos/deep-research && ./tools/news.sh "query" 15` — Google News RSS (works; redirect URLs do not resolve).
2. `./tools/get.sh "URL" out.txt` — HTML to text (fails on PDFs).
3. `web_fetch` for normal HTML.
4. PDFs: `curl -sL -o /tmp/x.pdf "URL" && pdftotext -layout /tmp/x.pdf /tmp/x.txt`.
For academic work use OpenAlex (`https://api.openalex.org/works?search=...`), arXiv API, and Semantic Scholar API via curl.

TASK: What do AI agents actually make **newly possible** in the manipulation of public perception around ambiguous events? Separate (1) technical possibility, (2) demonstrated capability, (3) credible evidence of deployment, (4) documented real-world impact.

Assess each of these specific claimed capabilities with hard evidence and effect sizes:
1. **Persuasion efficacy**: what do controlled studies show about LLM persuasion versus human persuasion? Look for: Salvi et al. (2025) on AI persuasion and its durability; Bai et al. and the "AI can persuade conspiracy believers" RCT (Costello, Pennycook & Rand 2024); personalised/microtargeted political persuasion; the GPT-4o persuasive-writing studies. Report **effect sizes** and methodological criticism. Crucially: does persuasiveness survive contact with real audiences and competing information?
2. **Continuous monitoring of public reaction** — social listening, sentiment tracking, real-time narrative detection. Commercial availability and cost.
3. **Adaptive narrative selection** — agents that test messages and shift approach based on response. Any demonstrated use, or only A/B testing analogues?
4. **Localised and multilingual messaging** — translation quality, dialect/local idiom, cost per message.
5. **Long-running persona management** — can agents sustain a consistent human-seeming identity over months? Evidence of detection, and of failures. Look for studies on LLM-generated accounts passing as human, and platform detection.
6. **Cross-platform coordination** — tooling and detection.
7. **Synthetic corroboration** — generation of apparently independent accounts, synthetic eyewitness testimony (image/video/audio), fake "independent" analyses. Include deepfake robocall cases (e.g. the January 2024 New Hampshire Biden robocall) and any prosecutions.
8. **Automated rebuttal evasion** — agents that notice and route around fact-checks. Any evidence?
9. **Exploitation of emerging narratives** — "newsjacking" automation.
10. **Cost and access**: what does it cost in 2026 to run N personas or generate N pieces of content? Compare to the human baseline.

Also cover: the **limits** — model guardrails and their bypass cost, platform integrity enforcement, rate limits, phone/identity verification, the economics of platform detection, and evidence that audiences are more resilient than assumed.

REQUIRED OUTPUT: structured markdown, 2,000-3,000 words, with a capability table: capability | technical possibility | demonstrated | deployed | measured impact | confidence | source. Flag clearly where claims rest on vendor marketing or on lab demonstrations rather than real-world use.

CONSTRAINTS: Analytic only. Do NOT provide operational instructions, prompts, tooling recommendations or implementation detail for running any influence campaign. Keep to capability assessment, evidence and defence.