#!/usr/bin/env python3
"""Create a private, auditable weekly research scaffold.

The public runner intentionally stops before any action recommendation. It proves
the timing and evidence contract while leaving live data integrations and
private focus lists outside the repository.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a weekly review research scaffold.")
    parser.add_argument("--focus-list", default="focus_list.local.json")
    parser.add_argument("--as-of", help="Report date in YYYY-MM-DD; defaults to today.")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument(
        "--market-profile",
        default="generic",
        help="Market adapter label; exchange-specific rules stay outside the public runner.",
    )
    return parser.parse_args()


def load_focus_list(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    subjects = data.get("subjects")
    if not isinstance(subjects, list) or not subjects:
        raise ValueError("focus list needs a non-empty 'subjects' array")
    required = {"code", "exchange", "name"}
    for item in subjects:
        if not isinstance(item, dict) or not required.issubset(item):
            raise ValueError("each focus list item needs code, exchange, and name")
        forbidden = {"shares", "quantity", "cost", "cost_basis", "account", "email"}
        if forbidden.intersection(item):
            raise ValueError("focus list is research-only; remove exposure or personal fields")
    return subjects


def next_monday(day: date) -> date:
    return day + timedelta(days=(7 - day.weekday()) % 7 or 7)


def build_report(
    as_of: date,
    subjects: list[dict[str, str]],
    source: Path,
    market_profile: str = "generic",
) -> str:
    generated_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    start = next_monday(as_of)
    end = start + timedelta(days=4)
    rows = "\n".join(
        f"| {item['code']}.{item['exchange']} | {item['name']} | pending live-data validation |"
        for item in subjects
    )
    return f"""# Weekly Review Research Scaffold: {as_of:%Y-%m-%d}

```yaml
report_generated_at: {generated_at}
evidence_cutoff: {generated_at}
decision_status: research_only
market_profile: {market_profile}
focus_list_source: {source.name}
validation_window: {start:%Y-%m-%d} open to {end:%Y-%m-%d} close, subject to market holidays
```

## Focus List

| Symbol | Display name | Data status |
|---|---|---|
{rows}

## Required Evidence Before Any Directional Conclusion

- Verify price, activity, timestamp, and source agreement.
- Evaluate the trend channel only after data-integrity and survival-risk gates pass; require enough completed historical observations.
- Confirm with core-indicator behavior and separately labelled 5/10/20-data-day capital flows.
- Link organizational facts to a dated primary disclosure. Delete unverified narratives.
- Treat anything disclosed after `evidence_cutoff` as a new event, not a revision of this report.

## Review Rule

Assess this report only in the validation window above. The executable reference point is the next actual market open, never a prior report-day close.
"""


def main() -> int:
    args = parse_args()
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    focus_list_path = (ROOT / args.focus_list).resolve() if not Path(args.focus_list).is_absolute() else Path(args.focus_list)
    subjects = load_focus_list(focus_list_path)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"weekly_review_{as_of:%Y%m%d}.md"
    output.write_text(
        build_report(as_of, subjects, focus_list_path, args.market_profile),
        encoding="utf-8",
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
