# AGENTS.md

## Purpose

Maintain the public multi-source weekly review research core without introducing personal data or unsupported claims.

## Non-negotiable rules

- Use runtime data, never silent mock values, funds, or events.
- Mark unavailable, stale, incomplete, or conflicting inputs explicitly.
- Keep core-indicator validation ahead of technical interpretation.
- Give the historical trend channel the highest contextual weight only after hard data and survival-risk gates pass; require at least three completed historical samples.
- Keep sector 5-day flow separate from subject 5/10/20-day flow.
- Print the start and end dates for every weekly or cumulative metric.
- Use scale-aware thresholds for subject-flow interpretation; one absolute threshold cannot cover both large and small subjects.
- Keep trend-channel wording consistent with band position: above 100% is an active downside region, below 0% is an active upside region.
- Do not turn broad policy, macro headlines, or unverified news into direct directional conclusions.
- Preserve the 168-hour event freshness rule unless a report labels an item as historical background.
- Report "scanned, no material event" only when every configured event dimension completed successfully.
- Treat macro indices, commodities, and other context series as constraints, never standalone directional conclusions.
- Keep disclosure dates forward-looking and explicit; missing dates must remain missing.
- Do not take external actions or send email from the public core.

## Privacy and publication

- Never commit account data, exposure size, cost figures, personal history, report output, email addresses, API keys, tokens, local paths, caches, or WorkBuddy/automation state.
- Keep credentials in environment variables or ignored local files only.
- Before publishing, run a sensitive-data scan, review the staged file list, and stage explicit paths rather than `git add -A`.
- Never publish WorkBuddy scripts that contain embedded subject maps, recipient addresses, access tokens, provider caches, or local interpreter paths.

## Verification

```bash
python3 -m py_compile run_weekly_report.py antifragile/*.py
python3 -m unittest discover -s . -p "test_*.py" -v
git diff --check
```

Public behavior and the full research protocol are documented in `WEEKLY-REVIEW-PROTOCOL.md` and `docs/RESEARCH_PROTOCOL.md`.
