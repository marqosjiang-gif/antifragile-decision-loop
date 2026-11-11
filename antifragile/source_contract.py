"""Data-contract gates for sourced artifacts.

Two failures look identical on a dashboard: "the source is old" and "the source
was refreshed but the chart was never rebuilt". A single freshness check cannot
tell them apart. Publishing therefore requires both gates:

1. Freshness gate  - the raw pull must be recent relative to the report date.
2. Consistency gate - the rendered artifact must carry the *same* as-of as the
   raw pull. A fresh pull plus a stale artifact is a silent regression.

Domain-neutral, standard library only. No provider clients live here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

DEFAULT_MAX_AGE_DAYS = 7


@dataclass(frozen=True)
class ContractVerdict:
    ok: bool
    code: str
    message: str
    raw_as_of: date | None = None
    rendered_as_of: date | None = None

    @property
    def exit_code(self) -> int:
        """0 = publishable, 2 = blocked (a fail-fast entry gate)."""
        return 0 if self.ok else 2


def parse_as_of(value: str | date | None) -> date | None:
    """Accept an ISO date or ISO datetime string; malformed input is not a date."""
    if value is None or isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except (ValueError, TypeError):
        return None


def evaluate_source_contract(
    raw_as_of: str | date | None,
    rendered_as_of: str | date | None,
    report_date: str | date,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
) -> ContractVerdict:
    """Block a render unless the raw pull is fresh AND the artifact matches it.

    The consistency check is deliberately last: a freshness-only gate would let
    "refreshed source + forgotten rebuild" pass with exit code 0.
    """
    raw = parse_as_of(raw_as_of)
    rendered = parse_as_of(rendered_as_of)
    today = parse_as_of(report_date)
    if today is None:
        raise ValueError("report_date must be an ISO date")

    if raw is None:
        return ContractVerdict(
            False, "missing_raw",
            "No raw pull found. Fetch source data before publishing.",
            raw, rendered,
        )
    if rendered is None:
        return ContractVerdict(
            False, "missing_rendered",
            "No rendered artifact found. Rebuild the artifact before publishing.",
            raw, rendered,
        )
    age = (today - raw).days
    if age > max_age_days or age < 0:
        return ContractVerdict(
            False, "stale_raw",
            f"Raw pull is {age} days from the report date; refresh it before publishing.",
            raw, rendered,
        )
    if rendered != raw:
        return ContractVerdict(
            False, "render_drift",
            "Raw pull was refreshed but the artifact still carries an older as-of. "
            "Rebuild the artifact, then re-run this gate.",
            raw, rendered,
        )
    return ContractVerdict(
        True, "ok",
        "Raw pull is fresh and the rendered artifact matches its as-of.",
        raw, rendered,
    )
