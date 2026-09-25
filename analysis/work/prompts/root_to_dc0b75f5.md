You are a research analyst. TODAY IS 25 SEPTEMBER 2026. Write your brief to `/Users/leonvanbokhorst/repos/deep-research/amplification/findings/08-defensive.md` and reply with a short summary.

TOOLING WARNING: `web_search` is BROKEN session-wide ("unprocessable response body"). Do not waste attempts. Use:
1. `cd /Users/leonvanbokhorst/repos/deep-research && ./tools/news.sh "query" 15` — Google News RSS (works; redirect URLs do not resolve).
2. `./tools/get.sh "URL" out.txt` — HTML to text (fails on PDFs).
3. `web_fetch` for normal HTML; PDFs via `curl` + `pdftotext`.
Find institution URLs via site search or sitemaps.

TASK: **Defensive practice** — how institutions can avoid becoming part of an amplification loop, and what mature practice already exists. This feeds the final section of a study on agentic amplification of ambiguous physical threats.

Investigate, using real institutional sources where possible (official guidance, after-action reviews, parliamentary reports, agency publications):

1. **Attribution discipline.** How do governments communicate when attribution is uncertain? Find official doctrine or guidance on attributing hostile activity, and examples of good and bad practice (e.g. the Dutch AIVD's caution; the German BfV's warning against "Überattribution"; the Dutch government's "act, don't attribute" debate; the UK's approach; NATO/EU statements). Include the argument for **not** attributing, and the costs of over-attribution.
2. **Trusted communication channels and crisis communication.** What does the risk-communication literature say about communicating uncertainty without feeding fear? (e.g. CDC/CERN/FEMA guidance; the "mental models" approach; transparency about what is not known). Include practical findings on message ordering, spokesperson credibility, and the "first 24 hours".
3. **Incident verification and anomaly triage.** Real practice: how do agencies verify drone sightings and unexplained events? Include the UK's incident-counting methodology, the German BKA/Federal Police approach, the US FAA/FBI processes during the 2024 New Jersey wave, and any after-action lessons. What triage criteria distinguish a hostile event from a misidentification?
4. **Detection of synthetic corroboration.** Practical, published techniques for identifying coordinated inauthentic behaviour, AI-generated personas, and fabricated eyewitness material. Include platform and third-party tools; open-source verification practice (Bellingcat, OSINT methods); image/video provenance (C2PA, Content Credentials); and the limits of each. Do NOT provide evasion guidance.
5. **Not amplifying.** The central institutional dilemma: reporting on a hoax spreads it. Find the actual state of the debate — "strategic silence", the "oxygen of publicity", the UK Counter Disinformation Unit / NDSOU approach, the EU EEAS FIMI reports and the dilemma of publishing attributions, and any after-action evidence on whether publishing helped or hurt. This is the most important section.
6. **Public reporting protocols.** How should the public be asked to report suspicious activity without generating a flood of false positives? Find real examples (e.g. the UK's "See It, Say It, Sorted" analogues; drone-reporting guidance; the Dutch NCTV advice on recording drone incidents) and evidence about false-positive rates.
7. **Prebunking as institutional defence** — how agencies have used it, and its limits.
8. **The reflexivity trap.** Institutional decisions that are individually rational but collectively amplify (closing an airport, deploying forces, issuing alerts, buying counter-drone systems). Find any official analysis of this trade-off.
9. **Indicators and warnings** for detecting a deliberate amplification campaign against an ambiguous-event backdrop — as discussed in open sources.

REQUIRED OUTPUT: structured markdown, 2,000-3,000 words, with a practical framing: for each defensive area, what mature practice looks like, what the evidence base is, and the main failure mode. Include URLs, confidence ratings, and an explicit "what is not known" section. Where institutions disagree, say so.

CONSTRAINTS: Defensive and analytic only. Do NOT provide operational instructions for conducting any campaign, and do not write detection-evasion content.