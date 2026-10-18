# Research Protocol

## Evidence before narrative

The public project accepts a conclusion only when its inputs state their source and time window. A failed source is a result, not an invitation to fabricate a replacement.

| Evidence | Required window | Allowed role |
|---|---|---|
| Weekly market movement | First represented data open to week close | Market context and movement confirmation |
| Sector-level flow | Five data days | Confirmation only; never replace with a single-day figure |
| Subject-level flow | 5, 10, and 20 data days | Short, medium, and long-horizon context |
| Organizational events | Freshness threshold shown in the report | Constraint or catalyst only after verification |
| Historical trend channel | At least three completed historical samples | Highest contextual decision weight after hard gates |
| Macro indices and commodities | Explicit weekly dates and source | Context or risk constraint only |
| Disclosure calendar | Next 7 and 30 calendar days | Forward disclosure risk; never infer a missing date |

## Via Negativa

Remove a claim when it is unsupported, stale, materially ambiguous, or cannot be linked to the configured subject. A popular headline, a policy slogan, or a single data point is not sufficient evidence for a directional conclusion.

## Consistency gates

- A trend-channel position above 100% is an active upper-band downside region; below 0% is an active lower-band upside region.
- A "no material event" statement is valid only after every configured scan dimension completes.
- Sector five-day flow and subject 5/10/20-day flow are separate datasets and must show exact dates.
- Subject-flow interpretation uses scale-aware thresholds rather than one absolute number for all subjects.
- Macro indices, commodities, policy, and geopolitical context cannot create a standalone directional conclusion.

## Evolution loop

Each review compares a prior rule with an observed result. Keep an evolution note local by default. Promote a rule only when it recurs across weeks, changes a real decision, and can be expressed without personal data.

## Public/private boundary

The public repository contains generic research logic. Personal subjects may be supplied at runtime with a local focus list (`--focus-list focus_list.local.json`); exposure details, costs, quantities, generated reports, local automation state, provider tokens, and proprietary data remain local and are ignored by Git.
