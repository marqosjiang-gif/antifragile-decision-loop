<div align="center">

# Antifragile Decision Loop

### Antifragile Weekly Review: Macro-Informed Decision Support

**Collect. Verify. Debate. Arbitrate. Review. Evolve.**

An evidence-first, market-adaptable weekly review loop with an expert council and bounded self-improvement. Macro context informs the risk budget — it never manufactures a trade.

[English](README.md) | [Español](docs/README.es.md) | [简体中文](docs/README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-00d992.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-00d992.svg?logo=python&logoColor=101010)](https://www.python.org/)
[![Market: pluggable adapters](https://img.shields.io/badge/Market-pluggable_adapters-00d992.svg)](#market-boundaries)
[![Cadence: Weekly review](https://img.shields.io/badge/Cadence-Weekly_review-1a1a1a.svg)](#bounded-self-improvement)
[![Mode: Research only](https://img.shields.io/badge/Mode-Research_only-1a1a1a.svg)](#privacy-boundary)

**[Why](#why-this-project) · [Expert council](#the-expert-council) · [Evolution](#bounded-self-improvement) · [Quick start](#quick-start) · [Live preview](docs/preview.html) · [Privacy](#privacy-boundary)**

</div>

> [!IMPORTANT]
> This repository is for quantitative research and decision support. It does not connect to a broker, place orders, or provide investment advice.

## Why This Project

Most single-operator market workflows are too fast to audit and too slow to learn from: daily noise is mistaken for a trend, old news is used as a catalyst, and a backtest price is treated as if it were executable.

**Antifragile Decision Loop** packages a slower, rule-led alternative for weekly review and next-window preparation — not intraday prediction. Verified macro factors adjust the risk budget; they never override technical evidence or create a trade on their own. Its two differentiators are:

1. **Expert council:** collection, verification, synthesis, arbitration, decision and publishing are separate stages with explicit handoff contracts.
2. **Bounded self-improvement:** each report is reviewed against the information available at its cutoff; only recurring, decision-relevant and policy-approved rules are promoted.

Its reusable methods are:

- **Weekly measurement:** calculate returns from the first actual market open to the last actual close of the same trading week.
- **Evidence gates:** verify price, volume, timestamps, source agreement, and missing-data status before interpretation.
- **Signal hierarchy:** historical Bollinger Band (BOLL) evidence has the highest weight only after data-quality and survival-risk gates pass; price-volume confirmation, multi-window capital flow, company disclosures, and macro context follow.
- **Via Negativa:** a narrative without a dated, verifiable source cannot become a trading reason.
- **Time-safe review:** a report may only be judged using information public by its `evidence_cutoff`; later disclosures are new events, not proof that the prior report should have known them.
- **Evolution loop:** retain recurring process rules, while keeping weekly opinions and generated reports local.

The repository contains a public reference runner, a configurable watchlist template, the public research protocol, the expert-council design, the evolution-loop contract, and tests. Your own watchlist, position size, cost basis, account data, API credentials, reports, and local caches stay outside Git.

The public entry point is intentionally small: `quant_loop.py` creates a research scaffold, while `run_weekly_report.py` is only a compatibility wrapper. Venue-specific data clients belong in a local adapter and are never required by the public core.

## The Expert Council

The coordinator routes work through six stages with a single accountability spine:

```mermaid
flowchart TD
    L["Evolution Lead · central relay"] --> S1
    subgraph WEEKLY["Weekly pipeline"]
        S1["① Collect — dated observations: market, filings, news, macro, commodities"] --> S2["② Verify — source agreement, timestamps, missing-data and conflict checks"]
        S2 --> S3["③ Synthesize — compare perspectives, make assumptions explicit"]
        S3 --> S4["④ Arbitrate — hard survival gates + signal hierarchy"]
        S4 --> S5["⑤ Decide — conditional next-week checks and risk controls"]
        S5 --> S6["⑥ Publish — auditable Markdown/HTML report"]
    end
    S6 --> R["⑦ Review — decisions vs outcomes"] --> E["⑧ Evolve — promote only recurring rules"] --> L
```

Eight named roles implement the stages — one accountable owner per stage, nothing bypasses the relay:

| Stage | Role | Responsibility |
|---|---|---|
| Relay | **Evolution Lead** | Central dispatch, stage gating, rule promotion |
| ① | **Info Collector** | One-pass pull of market / filings / news / macro / geo / commodity raw data |
| ② | **Info Verifier** | 168h + 120h window cross-validation → fact table |
| ③ | **Evidence Synthesizer** | Six-lens scoring fused via MCDA (TOPSIS + VIKOR) → neutral evidence matrix |
| ④ | **Signal Arbitrator** | Rule-engine primary verdict + antifragile-philosophy gray zone → 🟢🟡🔴 |
| ⑤ | **Decision Maker** | Translate the traffic light into trigger zones, position deltas, risk controls |
| ⑥ | **Research Editor** | Markdown → self-contained HTML weekly review |
| ⑦ | **Review Expert** | Last week's decisions vs actual outcomes → structured retrospective |
| ⑧ | **Evolution Lead** | Close the loop: consolidate, promote rules, evolve prompts |

Read the detailed public contract in [`docs/expert-team.md`](docs/expert-team.md).

## Bounded Self-Improvement

The loop follows **W1 generate → W2 review → W2.5 human/policy gate → W3 evolve → W1**. It classifies gaps, keeps one-off opinions local, and promotes only recurring improvements. Changes to decision rules, thresholds, agent roles, prompts, data sources or fallback chains require the W2.5 gate; presentation-only fixes may be recorded and promoted automatically. It can improve the research process; it cannot place orders, modify any account, or silently expose private data.

<img src="assets/readme/evolution-loop.png" alt="Evolution loop with a human policy gate and reversible promotion" width="100%" />

Read [`docs/evolution-loop.md`](docs/evolution-loop.md) for the promotion rules and review record.

## Install

```bash
git clone https://github.com/marqosjiang-gif/antifragile-decision-loop.git
cd antifragile-decision-loop

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Quick Start

Create a local watchlist from the public template. The local filename is ignored by Git.

```bash
cp watchlist.example.json watchlist.local.json
```

Edit only the codes and display names you want to research. Do not add share counts, cost basis, account information, or credentials.

Generate a weekly research scaffold:

```bash
python3 quant_loop.py --watchlist watchlist.local.json
```

It creates `weekly_quant_research_YYYYMMDD.md`, containing the run time, an evidence cutoff, the intended next-week validation window, and a watchlist checklist. The file is deliberately ignored by Git.

## How The Public Reference Loop Works

```mermaid
flowchart LR
    A["Weekly market data"] --> B["Timestamp and source checks"]
    B --> C{"Hard gates pass?"}
    C -- "No" --> D["Mark data unavailable\nNo directional conclusion"]
    C -- "Yes" --> E["Historical BOLL evidence"]
    E --> F["Price-volume confirmation"]
    F --> G["5/10/20-day flow\nand company disclosures"]
    G --> H["Macro context adjusts\nthe risk budget"]
    H --> I["Next-week executable review"]
    I --> J["Promote only recurring rules"]
    J --> A
```

The ordering matters. A macro story cannot override valid BOLL evidence, and a BOLL result cannot override a data conflict, a low-sample backtest, or a survival-risk gate.

| Layer | Question | Rule |
|---|---|---|
| Data integrity | Are price, volume, dates, and sources usable? | Unresolved price disagreement blocks a directional conclusion. |
| Historical BOLL | Has this weekly/monthly setup worked with enough completed observations? | It is the highest-weight technical input, not a guarantee. |
| Confirmation | Do price-volume and 5/10/20-day flows agree? | A single-day move cannot erase a medium-term signal. |
| Company evidence | Is there a dated disclosure that changes the thesis? | Later events never backfill the prior report. |
| Macro context | Does a verified factor change the risk budget? | Context can constrain risk, not manufacture a trade. |

## Configuration

| File | Purpose | Public? |
|---|---|---|
| [`watchlist.example.json`](watchlist.example.json) | Schema-only watchlist template | Yes |
| `watchlist.local.json` | Your actual research universe | No, ignored |
| [`config.example.yaml`](config.example.yaml) | Optional local integration placeholders | Yes |
| `config.local.yaml` | Your paths, keys, and local settings | No, ignored |
| [`PUBLIC_PROTOCOL.md`](PUBLIC_PROTOCOL.md) | Data, timing, review, and privacy rules | Yes |
| [`WEEKLY-REVIEW-PROTOCOL.md`](WEEKLY-REVIEW-PROTOCOL.md) | Weekly report generator protocol | Yes |

The reference runner uses only the standard library. Optional research modules may use your chosen data libraries when you build them into a local workflow. Provider credentials and venue-specific rules remain local.

## Usage Example

`watchlist.local.json`:

```json
{
  "universe": [
    {"code": "EXAMPLE-001", "exchange": "DEMO", "name": "Example instrument"}
  ]
}
```

Run:

```bash
python3 quant_loop.py --watchlist watchlist.local.json --as-of 2026-08-03
```

The output deliberately records these boundaries:

- `report_generated_at`: when the report was produced.
- `evidence_cutoff`: the latest public information allowed into the report.
- `validation_window`: the next actual trading week, from the first executable open to the last close.
- `decision_status`: `research_only` until data and rule gates are completed.

## Market Boundaries

The public core is market-adaptable. Exchange calendars, settlement rules, price limits, short-selling rules, corporate-action treatment, currency and liquidity assumptions belong in a market adapter and must not be silently copied across markets. The included examples use synthetic symbols; any market-specific behavior is optional and must be labeled as such.

## Privacy Boundary

- No order routing, brokerage integration, or automatic position changes.
- No claim of future return, win rate, or live trading performance.
- No generated report, local cache, position size, cost basis, email address, token, or API key belongs in a public commit.
- A later announcement can trigger a new review, but it cannot be used to call an earlier report wrong unless it was already public before that report's evidence cutoff.
- A backtest or review starts at the next executable market point, not at a convenient historical close.

## FAQ

### Is this an automatic trading bot?

No. It is a medium-low frequency research workflow. It prepares evidence, constraints, and conditions for a human decision.

### Which strategy has the highest priority?

Historical BOLL evidence, but only after data integrity and survival-risk gates pass. A small sample, a stale series, or unresolved data conflict reduces it to observation-only.

### What role does the macro view play?

A verified macro factor adjusts the risk budget. It can shrink or pause exposure logic; it cannot override technical evidence or invent a trade.

### Why no ready-made instrument list or portfolio?

Personal watchlists and positions are private and can bias a public project. Configure your own local universe from the template.

### Why does the generated file avoid a buy/sell command?

The public reference runner proves the timing and audit structure. A real decision requires live, verified data and your own risk constraints.

## Contributing

Issues and pull requests are welcome. Keep rule changes testable and auditable. Do not submit private watchlists, account data, generated research reports, credentials, or unverified market claims.

## License

Released under the [MIT License](LICENSE).
