"""Capital-flow window calculations with explicit data-day coverage."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Mapping


@dataclass(frozen=True)
class FlowWindow:
    data_days: int
    start: date
    end: date
    net_amount: float


def classify_capital_flow(
    net_amount: float,
    total_capitalization: float,
) -> str:
    """Classify 20-day capital flows using liquidity-aware public thresholds.

    Larger and smaller capitalized subjects must not share one absolute threshold.
    The output is research context, not a standalone action instruction.
    """
    if total_capitalization <= 0:
        raise ValueError("total_capitalization must be positive")
    if total_capitalization >= 100_000_000_000:
        inflow, outflow, neutral = 3_000_000_000, -3_000_000_000, 1_000_000_000
    else:
        inflow, outflow, neutral = 150_000_000, -150_000_000, 50_000_000
    if net_amount > inflow:
        return "persistent_inflow"
    if net_amount < outflow:
        return "persistent_outflow"
    if abs(net_amount) < neutral:
        return "range_bound"
    return "mixed"


def aggregate_flows(
    rows: Iterable[Mapping[str, object]], windows: tuple[int, ...] = (5, 10, 20)
) -> dict[int, FlowWindow]:
    """Aggregate verified daily capital flows and retain the exact date range.

    Each row requires ``date`` (ISO date or ``date``) and ``net_amount``.
    Duplicate data days are rejected to prevent accidental double counting.
    """
    parsed: dict[date, float] = {}
    for row in rows:
        raw_date = row.get("date")
        day = raw_date if isinstance(raw_date, date) else date.fromisoformat(str(raw_date))
        if day in parsed:
            raise ValueError(f"duplicate data day: {day.isoformat()}")
        parsed[day] = float(row["net_amount"])

    ordered = sorted(parsed.items())
    result: dict[int, FlowWindow] = {}
    for size in windows:
        if size <= 0:
            raise ValueError("flow window must be positive")
        if len(ordered) < size:
            continue
        sample = ordered[-size:]
        result[size] = FlowWindow(
            data_days=size,
            start=sample[0][0],
            end=sample[-1][0],
            net_amount=sum(amount for _, amount in sample),
        )
    return result
