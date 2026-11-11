"""Public, privacy-safe research primitives for the weekly review loop.

Everything exported here is domain-neutral and standard-library-only. Provider
clients, credentials and private focus lists stay in ignored local adapters.
"""

from .decision import (
    Decision,
    ResearchEvidence,
    TrendChannelEvidence,
    channel_position_wording,
    decide,
)
from .capital_flows import FlowWindow, aggregate_flows, classify_capital_flow
from .freshness import evaluate_scan_coverage, is_fresh_event
from .source_contract import ContractVerdict, evaluate_source_contract
from .quantile_tiers import (
    TierScale,
    build_tiers,
    classify,
    legacy_percentile,
    quantile,
)
from .claim_audit import AuditReport, Claim, Finding, audit_claims
from .defer_gate import DeferVerdict, GateInput, SupportRecord, evaluate_defer

__all__ = [
    "TrendChannelEvidence",
    "ResearchEvidence",
    "Decision",
    "FlowWindow",
    "aggregate_flows",
    "classify_capital_flow",
    "decide",
    "channel_position_wording",
    "is_fresh_event",
    "evaluate_scan_coverage",
    "ContractVerdict",
    "evaluate_source_contract",
    "TierScale",
    "build_tiers",
    "classify",
    "quantile",
    "legacy_percentile",
    "Claim",
    "Finding",
    "AuditReport",
    "audit_claims",
    "GateInput",
    "SupportRecord",
    "DeferVerdict",
    "evaluate_defer",
]
