"""Privacy-safe research primitives for the weekly market review loop."""

from .decision import TrendChannelEvidence, Decision, ResearchEvidence, decide
from .capital_flows import FlowWindow, aggregate_flows
from .freshness import is_fresh_event

__all__ = [
    "TrendChannelEvidence",
    "Decision",
    "FlowWindow",
    "ResearchEvidence",
    "aggregate_flows",
    "decide",
    "is_fresh_event",
]
"""Public, privacy-safe research primitives."""

from .decision import channel_position_wording
from .capital_flows import classify_capital_flow
from .freshness import evaluate_scan_coverage

__all__ = [
    "channel_position_wording",
    "classify_capital_flow",
    "evaluate_scan_coverage",
]
