# What 153 agents actually bought us

## Lessons from a 1.28-billion-token recursive research run

*Practitioner report — working draft*

---

We did not set out to run an experiment on recursive research.

We were using DSH for research.

The task was genuinely open-ended: investigate two related questions, fan the work out into specialist branches, retrieve primary evidence where possible, challenge weak claims, and pull the result back together into something a human could actually use. The run grew much larger than expected: **153 sessions, 10,037 model steps, 16,195 tool calls and 1.286 billion logged tokens** across roughly 96 minutes of wall-clock time.

At first, the scale looked impressive for the obvious reason: it produced a lot.

Then we exported the full session tree and looked at what had actually happened.

That was more interesting.

The agents had gathered evidence with surprisingly little overlap. Deep leaves had corrected claims that their parents had already accepted. Several important findings only appeared late, after source discovery had begun to flatten. At the same time, the final synthesis overstated how independently its central conclusion had emerged. The system was very good at finding wrong facts and much less good at challenging its own framing.

So this report is not a benchmark and not a claim about “agents” in general. It is a close look at one large, traceable research run, using the run itself as the empirical object.

The question is simple:

> **What did all that recursive scale actually buy us?**

And, underneath that:

> **When does more research become more knowledge, and when does it become more confidence?**

---

## 1. The run

The original research was performed in a single DSH root session with recursive delegation to a maximum depth of three. The root remained the sole final synthesiser.

The resulting tree was:

- **1** root session
- **16** depth-1 branches
- **45** depth-2 sub-analyses
- **91** depth-3 leaves

That makes **153 sessions** in total.

The run produced **1,286,531,354 logged tokens**. Of those, **1,258,387,840 were cache reads**, **18,834,657 were fresh/cache-miss input**, and **9,308,857 were output**. The actual prompt-side cache-hit rate was **98.525%**.

DeepSeek's provider billing export later let us reconcile those token classes against what was actually charged. At the prices billed on 25 September 2026, the frozen research run cost approximately **$12.19**.

That number sounds absurdly low next to “1.28 billion tokens”, and that is precisely why the cache architecture matters. The system repeatedly re-used a very large shared prefix instead of paying full price for every logical token processed.

But cheap scale is not the same thing as useful scale. That is where the logs became valuable.

> **Figure 1 — Agent genealogy of the DSH run**  
> 1 → 16 → 45 → 91, including the depth cap and highlighted correction-producing leaves.

---

## 2. The first surprise: the agents really did look in different places

Before inspecting the trace, we expected a lot of recursive duplication: many agents independently searching for the same papers, reading the same reports, and then summarising each other.

That is not what happened.

Across the 16 depth-1 branches, the median pairwise domain overlap was only **0.031**. The union contained **1,609 distinct evidence hosts**, while the sum of branch-level hosts was 2,400. Only **1.9% of 2,416 normalised unique queries** were repeated by more than one session.

In other words, fan-out genuinely bought breadth.

That matters because some of the strongest negative findings were reached independently from different directions. The system was not simply manufacturing volume around a fixed handful of sources. It was exploring a wide evidence surface.

This is one place where “more agents” meant something concrete.

Not more agreement.

More coverage.

---

## 3. The second surprise: deep recursion behaved a bit like accidental peer review

Three of the four largest corrections in the run came from **depth-3 leaves**.

These were not cosmetic edits. They were cases where a narrow specialist went to a primary source and discovered that a stronger claim higher in the tree did not survive contact with the source.

Examples included:

- a primary psychology paper showing **repetition, not number of sources**, undermining a claimed amplification mechanism;
- a recent **author correction** that retired a widely cited persuasion effect size;
- a full-text search that found **no support** for a quotation already attributed to Liddell Hart.

This pattern appeared repeatedly: the broader parent branch established a plausible interpretation, while the narrower child did the tedious source work that destabilised it.

That is probably the most encouraging finding in the entire trace.

Recursive delegation did not make the system better because many agents “voted” for the same conclusion. It made the system better because narrow agents sometimes had enough attention to **check what everybody else had treated as settled**.

> **The value of fan-out was adversarial coverage, not consensus.**

We reconstructed roughly twenty corrections across the run. Most moved in a deflationary direction: removing overstatement, weakening attribution or reducing confidence.

That is a useful behaviour in research.

> **Figure 2 — Epistemic anatomy**  
> Breadth decentralised → verification distributed → judgment centralised.

---

## 4. Then we found the uncomfortable part

The final research report said that **“six independent evidence streams converged”** on the central formulation *plausible, novel, and currently unobserved*.

That sounded strong.

It did not survive provenance analysis.

The “six streams” were six sibling agents spawned by one depth-1 branch. One depth-2 agent first wrote the exact verdict phrase. The final root report imported it shortly afterwards.

More importantly, the root had already written a large draft containing the core framing at about **+59.7 minutes**.

Several of the findings later presented as decisive support had not arrived yet.

The Foster null arrived around +63 minutes. The Salvi correction around +66. The USC paper that the report itself called the “single most important constraint finding” arrived around **+80.7 minutes**. OpenAI's strongest negative evidence arrived around +86. The Botometer caution arrived around +95.

The conclusion may still be a reasonable one.

But the process did not independently generate that conclusion six times.

What happened was subtler:

**a prior was stated early, independent evidence gathering followed, and much of the later evidence was consistent with the prior.**

That is not the same thing as independent conclusion production.

This distinction became one of the core lessons from the run:

> **Independent evidence gathering is not independent judgment.**

> **Figure 3 — Verdict formation vs arrival of key evidence**  
> Show the early draft/verdict against the later arrival of decisive evidence.

---

## 5. The system corrected facts better than framing

Once we noticed the convergence problem, another asymmetry became visible.

The run was quite willing to correct **checkable factual claims**: dates, quotes, dollar figures, source attributions, effect sizes and publication details.

We found thirteen documented disagreements where one part of the tree corrected another.

But the one disagreement that directly touched the interpretive core went the other way. A specialist judged “reflexive control” only a **partial** conceptual fit. The branch lead explicitly recorded that it had **kept the rating high**, matching the framing already present in the draft.

This is one run, so we should resist turning that into a law of agent systems.

But as a design signal it is hard to ignore.

The architecture had many mechanisms for challenging facts and only one place where final interpretation was adjudicated.

The same root that integrated the evidence also decided what the evidence meant.

So the system had something like a distributed immune system for factual error, but a centralised interpretive bottleneck.

That is not necessarily a flaw. Somebody has to synthesise.

The problem is that the synthesiser had no equivalent reviewer.

---

## 6. Finding an error was not the same as fixing it

The agents found corrections that never fully propagated into the final report.

At least two claims were explicitly withdrawn in one place while surviving elsewhere in the document under their original wording.

The final verification pass helps explain why. It searched for known bad strings and named claims. That works when the error is a distinctive quotation or citation. It does not work when a withdrawn idea survives semantically in slightly different prose.

Correction latency also mattered.

Some corrections took several minutes to move up the tree. One took more than sixteen minutes. During that time, thousands of model steps continued elsewhere.

At this scale the limiting factor was no longer simply **finding** an error.

It was routing the correction to the one context that could apply it, and making sure that context actually did so.

That gives us a practical design problem:

> **Correction throughput needs its own architecture.**

Not just better retrieval. Not just more reviewers. A correction needs to become a first-class object that can be tracked until every affected claim has been reconsidered.

---

## 7. The run did not naturally decide it was done

Another thing we initially read too generously was the shape of the tree.

There were 91 depth-3 leaves because the research had reached a sensible stopping point, right?

No.

**Forty of those 91 leaves tried to delegate again.**

Together they made **99 depth-4 spawn attempts**. Every one was rejected because the harness had a hard `maxDepth=3` limit.

The tree was therefore not “finished” in an epistemic sense.

It hit a fence.

That matters because recursive systems can easily create the impression that a tree shape reflects some natural decomposition of a problem. Here the bottom of the tree was partly an infrastructure artefact.

The creature had not reached epistemic satiation. We put up a fence.

---

## 8. When should a recursive research run stop?

This turned out to be harder than expected.

Source discovery clearly decayed. The first tenth of the run found **428 new evidence hosts**. The last two tenths found only **48** and **66**.

If that were the whole story, a simple diminishing-return rule would work.

But artefact production did not decay in the same way. Late in the run, agents were still producing 38–45 new artefacts per decile.

More importantly, several of the **best corrections arrived late**:

- Foster null: ~63% through the work
- Salvi correction: ~66%
- USC constraint paper: ~77%
- OpenAI negative evidence: ~86%
- Botometer caution: ~95%

A stopping rule based only on “we are not finding many new sources anymore” would have cut off much of the most valuable corrective work.

A rule based on **conclusion stability** would have been worse. The central conclusion stabilised before much of the evidence that later justified it had arrived.

So in this run, conclusion stability was not a sign of epistemic maturity.

It was partly a sign of early commitment.

The best candidate signal we found was narrower:

> **Keep watching whether agents are still reaching new primary sources.**

Late work that mattered disproportionately involved primary literature, author corrections, archived full text and original institutional material. Late work that did not matter was more often another pass over an already familiar source space.

That is not yet a stopping algorithm.

But it is a better question than “have the agents started agreeing?”

> **Figure 4 — Discovery falls while artefact production stays alive**  
> Overlay markers for late decisive corrections.

---

## 9. The economics were strange enough to change the design space

The run's logical input volume was **1.277 billion tokens**.

Only **18.8 million** of those were cache misses.

The provider-side billing data gave us an unusually clean cross-check. A later, separate four-session analysis run produced exactly **398 model calls**, and DeepSeek's 12:00–13:00 billing bucket contained exactly 398 requests with identical cache-hit, cache-miss and output-token totals.

That let us validate both the DSH accounting fields and the historical prices.

For the original research run:

- cached input: **$3.78**
- fresh input: **$2.83**
- output: **$5.59**
- total: **$12.19**

This does not mean “a billion tokens costs twelve dollars”.

It means that **this particular recursive architecture, with this model, this shared prefix and these provider prices, made enormous logical context reuse extremely cheap**.

That changes what is technically feasible.

It also creates a trap.

If repeated re-synthesis is nearly free, a system can keep producing polished output long after it has stopped learning much.

Cheap tokens can support better checking.

They can also support very inexpensive epistemic bureaucracy.

> **Figure 5 — Token and cost composition**  
> Show the enormous cached logical volume next to its surprisingly small monetary share.

---

## 10. What we would change next time

We would not respond to this run by making the tree smaller.

The breadth and deep verification were genuinely useful.

We would change where independence is introduced.

A next version should probably include:

**A second adjudicator that does not inherit the synthesiser's framing.**  
Not another evidence-gathering branch. A deliberately separate interpretation pass.

**Explicit interpretive dissent.**  
Some agents should be asked to challenge the framing, not merely verify factual claims inside it.

**First-class correction propagation.**  
A correction should identify affected claims and remain open until those claims have been revisited.

**Process claims should be verified like research claims.**  
The least reliable statements in this run were some of the system's claims about its own process: how many independent streams converged, how many corrections it had made, and why the run had stopped.

**Primary-source novelty as a live stopping signal.**  
Not because every primary source is valuable, but because it tracked high-value late work better than general source novelty or agreement did here.

**A hard budget remains useful.**  
The depth cap was arbitrary epistemically, but predictable operationally. Recursive systems still need fences.

---

## 11. What this report does not show

This is one research run.

It used one harness, one model/provider configuration, one maximum recursion depth, one final synthesiser and two related research questions. The research topic itself may also have encouraged skeptical, source-heavy behaviour in ways that another domain would not.

We did not independently re-litigate every substantive claim in the original research report.

We therefore cannot claim that depth 3 is optimal, that 153 agents is a useful number, that these economics generalise to another provider, or that recursive research systems generally behave this way.

What we *can* do is reconstruct this run unusually well.

The full session tree is preserved by per-file hashes. The delegation structure, token accounting, tool calls, messages, source retrieval, corrections and timing can all be inspected. The provider billing was independently reconciled against a separate frozen run.

That makes this less like a controlled study and more like a **forensic case study of a real research process**.

That is exactly how we intend it.

---

## 12. The bit we are taking forward

The most important lesson is not that 153 agents are better than one.

The run did something more interesting than that.

It showed that different epistemic functions scaled differently.

**Breadth scaled well.**

**Verification scaled surprisingly well.**

**Judgment did not decentralise just because research did.**

The same early commitment that helped the root turn a huge amount of material into a coherent report also made the independence of its final interpretation weaker than the final prose suggested.

That tension is probably the thing worth designing for next.

> **Recursive scale made it easier to know more. It did not automatically make it easier to know whether our interpretation was right.**

---

## Evidence and reproducibility

This practitioner report is a human-facing synthesis of the forensic analysis in this repository.

The underlying technical reports are:

- [`analysis/00-synthesis.md`](analysis/00-synthesis.md)
- [`analysis/02-agent-genealogy.md`](analysis/02-agent-genealogy.md)
- [`analysis/03-token-and-cache-tables.md`](analysis/03-token-and-cache-tables.md)
- [`analysis/05-independence-and-convergence.md`](analysis/05-independence-and-convergence.md)
- [`analysis/06-anomalies-and-unexpected-behaviour.md`](analysis/06-anomalies-and-unexpected-behaviour.md)
- [`analysis/07-marginal-return-and-stopping.md`](analysis/07-marginal-return-and-stopping.md)
- [`analysis/08-provider-billing-reconciliation.md`](analysis/08-provider-billing-reconciliation.md)

The original substantive research is frozen at
[`leonvanbokhorst/deep-research@33ca23b`](https://github.com/leonvanbokhorst/deep-research/commit/33ca23b474a11b5ee90563a9f59ed002de485abd).
