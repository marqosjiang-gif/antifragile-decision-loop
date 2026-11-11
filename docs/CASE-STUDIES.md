# From Insight to Deliverable — Case Studies

> **One-line conclusion:** every mechanism in this repository answers one hiring
> question — can an industry insight be turned into a running, auditable system
> without overstating what the data or the model can actually do?

This document is a **capability map**, not a résumé. All examples are drawn from
the public implementation in this repository. No employer name, client name,
account, real subject, cost, credential or private path appears here. The project
is research-only: it prepares evidence and conditions for a human decision, and
it is not investment advice.

---

## 1. Target-role capability map

Target role: an industry-solution consulting / forward-deployed engineering (FDE)
type position in a cloud-and-AI organisation, serving retail, agriculture,
travel & hospitality, real estate and financial-services clients.

| JD requirement | Verifiable evidence in this repo | Where to look |
|---|---|---|
| R1 · Understand core business processes, identify AI-reshapable scenarios, produce executive-level analysis | An eight-role staged council with explicit handoff contracts; a layered signal hierarchy that separates data integrity, trend evidence, confirmation, disclosures and macro context | [`expert-team.md`](expert-team.md), [`../WEEKLY-REVIEW-PROTOCOL.md`](../WEEKLY-REVIEW-PROTOCOL.md) |
| R2 · Turn insight into a technical solution; understand AI/model limits; co-create architecture with product and engineering | Three business rules translated into runnable gates: dual data-contract checks, a conservative defer state machine, a post-render claim auditor | [`../antifragile/source_contract.py`](../antifragile/source_contract.py), [`../antifragile/defer_gate.py`](../antifragile/defer_gate.py), [`../antifragile/claim_audit.py`](../antifragile/claim_audit.py) |
| R3 · Analyse and model large datasets into decision-grade business analysis | Distribution-derived thresholds replace conventional cut-offs; 5/10/20-window aggregation with scale-aware interpretation; explicit as-of and source labels | [`../antifragile/quantile_tiers.py`](../antifragile/quantile_tiers.py), [`../antifragile/capital_flows.py`](../antifragile/capital_flows.py) |
| R4 · Surface unstated client needs through first-hand investigation | Three "silent failures" found only by walking the pipeline end to end: a refreshed source with a stale chart, a cache whose schema was never consumed, and a threshold describing the wrong distribution | §2 below, [`../PUBLIC_PROTOCOL.md`](../PUBLIC_PROTOCOL.md) |
| Q1 · Consulting / AI project background | A weekly W1 → W2 → W2.5 → W3 cadence with dated review records and reversible rule promotion | [`evolution-loop.md`](evolution-loop.md) |
| Q2 · "Consultant + technical translator" | A natural-language policy ("if support is expected, the pause may be lifted") becomes four explicit states, with human registration as a hard boundary | `defer_gate.py`, §2 Case D |
| Q3 · Curiosity about applied AI, fast learning of new scenarios | Mutation-proven regression locks, lock-coverage thinking, time-safe review (judge a report only with information available at its cutoff) | [`../test_public_iteration.py`](../test_public_iteration.py), [`../PUBLIC_PROTOCOL.md`](../PUBLIC_PROTOCOL.md) |
| Q4 · Cross-team collaboration across business, product and engineering | Single-accountability stages, a human/policy gate before any decision-affecting change, and "presentation-only vs rule change" classification | [`../AGENTS.md`](../AGENTS.md), `evolution-loop.md` |

---

## 2. Four STAR narratives (copy-ready)

Each narrative is written in the third person about the project, so it can be
read as a system description or adapted into a first-person interview answer.

### Case A — "Fresh pull, stale chart" (R2, R4)

- **Situation:** a weekly research artifact is regenerated from a sourced pull.
  A freshness gate existed, and every source file had a valid `as_of`.
- **Task:** make sure the published chart actually reflects the latest pull.
- **Action:** walk the pipeline end to end and add a second, independent gate —
  the rendered artifact's `as_of` must equal the raw pull's `as_of`. A fresh pull
  plus a forgotten rebuild now returns `render_drift` and a fail-fast exit code,
  with a message that tells the operator exactly which step to re-run.
- **Result:** both failure modes become visible and distinguishable; the check is
  locked by a regression test that plants the exact drift and asserts it is caught.
- **First question I would ask a client:** "Who notices when the data is refreshed
  but the deck is not?"

### Case B — "A threshold that was an order of magnitude off" (R3)

- **Situation:** a two-value indicator used inherited cut-offs to label readings
  "strong" or "weak".
- **Task:** decide whether those labels described the data or merely convention.
- **Action:** build a multi-year observed series, compute empirical percentiles,
  and measure where each legacy cut-off actually sat. The "strong" cut-off landed
  near the bottom of the distribution — the scale was wrong by roughly an order
  of magnitude. Replace the constants with five quantile bands derived from the
  series, and keep the thresholds in a versioned source file rather than in prose.
- **Result:** labels now describe relative position in their own history; a helper
  (`legacy_percentile`) exposes any future scale mismatch as evidence, not opinion.
- **First question I would ask:** "Where did this number come from, and what
  percentile is it in your own data?"

### Case C — "Replace a chapter without changing a single decision" (R1, R2)

- **Situation:** stakeholders wanted one analytical section retired and a new
  contextual section introduced, while every downstream decision table had to
  remain unchanged.
- **Task:** separate presentation from the data plane.
- **Action:** disable the old renderer through a single switch (kept, not deleted,
  so rollback stays possible), enrich the shared evidence object unconditionally,
  and leave the decision-table path untouched. Add an optional report-date argument
  so the same run is reproducible.
- **Result:** the report changes shape, the decision layer is bit-for-bit stable,
  and a structural lock plus a mutation test prove the switch is really enforced.
- **First question I would ask:** "Which part of this report is allowed to change,
  and which part must never move?"

### Case D — "A sentence becomes a state machine" (Q2, R2)

- **Situation:** a business rule said that after a risk boundary is breached, a
  pause on new additions may be lifted when fundamental support is expected.
- **Task:** implement it without letting a model guess what "expected" means.
- **Action:** define four states — `NOT_APPLICABLE`, `FORBID`, `INSUFFICIENT`,
  `ALLOW`. The system only *consumes* human-registered support records with a
  declared basis and as-of; anything inferred, unverified, stale or missing a
  forward checkpoint degrades conservatively to `INSUFFICIENT`. `ALLOW` lifts the
  pause only, and still defers any increase to a checkpoint.
- **Result:** the ambiguous word "expected" is replaced by an auditable contract;
  the model's capability boundary is encoded instead of asserted in documentation.
- **First question I would ask:** "Which facts are you willing to have the model
  infer, and which must a human register?"

---

## 3. Interview question bank (with answer anchors)

| # | Likely question | Answer anchor |
|---|---|---|
| 1 | Why two gates instead of one freshness check? | They catch different failures; a fresh source with a stale artifact passes a freshness check with exit 0. |
| 2 | How do you falsify a threshold? | Compute its empirical percentile in the observed series; if a "strong" cut-off sits near P15, retire it and derive bands from quantiles. |
| 3 | Where is the boundary of an LLM here? | It does not register support facts, does not adjudicate between two competing explanations, and does not take external actions. |
| 4 | Data is correct but the conclusion is wrong — why? | Time window, unit/scale, or schema contract. Check as-of alignment, then whether the consumer ever read the field. |
| 5 | Design a human-in-the-loop gate. | Classify changes as decision-affecting vs presentation-only; require approval, evidence, previous version, test result and rollback path. Skipping a card is not approval. |
| 6 | Why audit claims after rendering? | Templates drift; cautious copy can become absolute and unattributed after formatting. The auditor is read-only and returns 0/1/2. |
| 7 | How do you handle a failed data source? | Keep it visible, downgrade to observation, never let a fallback impersonate the primary source. |
| 8 | How do you know your regression locks work? | Mutation testing: deliberately break the rule and confirm the test turns red; a lock that cannot fail is not a lock. |
| 9 | What is a rolling regime board? | One authoritative background document; each weekly report writes only the delta, so executive attention goes to what changed. |
| 10 | A client asks the system to execute decisions automatically. | Decline: this is research-only, no external action, no account integration, no performance claim. Offer a decision-support alternative. |
| 11 | Tell me about a time you reversed your own judgement. | A driver-attribution call was corrected after dual-source verification showed two indicators moving together; the correction was recorded as a rule, not quietly forgotten. |
| 12 | What does "executive-ready" mean to you? | A short delta, an explicit as-of, named sources, visible uncertainty, and one clear decision condition — not a longer report. |

---

## 4. Reverse questions for the interviewer

1. Is the first deliverable for this role an insight report, a reusable prototype, or a client-facing architecture?
2. Where is the hardest alignment today on "what the model can and cannot do"?
3. Who owns the acceptance criteria when a consulting recommendation becomes a product feature?
4. Is there a standard playbook for "data is insufficient but a conclusion is still requested"?
5. How is an executive-level analysis reviewed before it leaves the team?
6. How often does the team do first-hand client discovery, and what does a typical discovery output look like?
7. Which capability does the preferred certification actually validate in day-to-day work?

---

## 5. Copy-ready templates

**60-second project pitch**

> "I built a weekly, evidence-first decision loop. Instead of letting one model
> produce a conclusion, eight single-owner stages hand off explicit contracts:
> collect, verify, synthesise, arbitrate, decide, publish, review, evolve. The
> interesting part is the boundary engineering — dual data-contract gates,
> distribution-derived thresholds, a conservative defer state machine, and a
> post-render claim auditor. Every change that could affect a decision passes a
> human gate, and every rule is proven by a mutation test. It is research-only:
> it prepares evidence for a human, it never acts on an account."

**Whiteboard order (5 boxes)**

1. Business question → observable data (with as-of and source).
2. Two hard gates → data integrity / consistency.
3. Evidence hierarchy → what may and may not produce a conclusion.
4. Human/policy gate → which changes are allowed to ship.
5. Review → only recurring, decision-relevant rules get promoted.

**One-page case template**

```markdown
Situation:  (one sentence, no jargon)
Task:       (what had to stay unchanged)
Action:     (the mechanism, named as a file or function)
Result:     (a checkable outcome, not an adjective)
Boundary:   (what the system deliberately refuses to do)
Question:   (the first thing I would ask the client)
```

---

## 6. Notes and caveats

- All numbers above describe **engineering facts** (states, bands, gates, tests),
  not holdings, returns, accounts or performance claims.
- Do not present this repository as a production trading system. It does not
  execute actions, does not hold credentials, and does not claim accuracy.
- Every external number in a real interview answer should carry an as-of date and
  a reachable source; if it cannot, say "not verified" instead of guessing.
- This document maps capability to a public JD. It makes no claim about any
  application, interview outcome, certification or employment status.

## 7. Self-check checklist

- [ ] Conclusion first, then evidence.
- [ ] Every claim maps to a file, function or test in this repository.
- [ ] No client, employer, subject, account, credential or local path.
- [ ] No performance, accuracy or "live results" promise.
- [ ] Research-only boundary stated at least once in every narrative.
- [ ] At least one reverse question prepared for the interviewer.
- [ ] `python3 -m unittest discover -s . -p "test_*.py" -v` passes locally.
