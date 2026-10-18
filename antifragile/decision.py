"""Auditable decision arbitration with the trend channel as the highest weighted signal."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ChannelStance = Literal["upside", "hold", "downside", "none"]


@dataclass(frozen=True)
class TrendChannelEvidence:
    action: ChannelStance = "none"
    completed_samples: int = 0
    win_rate: float | None = None
    efficiency_per_day: float | None = None
    verified: bool = False
    timeframe: Literal["daily", "weekly", "monthly", "unknown"] = "unknown"
    band_position_pct: float | None = None

    @property
    def sample_is_actionable(self) -> bool:
        return self.verified and self.completed_samples >= 3


@dataclass(frozen=True)
class ResearchEvidence:
    price_verified: bool
    activity_verified: bool
    channel: TrendChannelEvidence = field(default_factory=TrendChannelEvidence)
    flow_5d: float | None = None
    flow_20d: float | None = None
    flow_verified: bool = False
    fundamentals_verified: bool = False
    adverse_event_verified: bool = False
    survival_risk: bool = False


@dataclass(frozen=True)
class Decision:
    label: Literal["upside", "hold", "downside", "observe"]
    action: str
    confidence: Literal["high", "medium", "low"]
    reasons: tuple[str, ...]


def decide(evidence: ResearchEvidence) -> Decision:
    """Apply hard validation, then trend channel > confirmation indicators > capital flows > fundamentals/events.

    Lower-priority evidence can reduce confidence or tighten risk, but cannot
    silently override an actionable historical trend-channel signal.
    """
    if evidence.survival_risk:
        return Decision(
            "observe",
            "A verified survival-risk gate blocks new exposure.",
            "low",
            ("survival-risk hard gate failed",),
        )
    if not evidence.price_verified or not evidence.activity_verified:
        return Decision(
            "observe",
            "Do not issue a directional judgement until price and activity data are verified.",
            "low",
            ("price/activity hard gate failed",),
        )

    channel = evidence.channel
    reasons: list[str] = ["price and activity data verified"]
    if channel.verified:
        reasons.append(
            f"channel={channel.action}, timeframe={channel.timeframe}, "
            f"completed_samples={channel.completed_samples}"
        )
    else:
        reasons.append("trend channel unavailable")

    flow_negative = (
        evidence.flow_verified
        and evidence.flow_5d is not None
        and evidence.flow_20d is not None
        and evidence.flow_5d < 0
        and evidence.flow_20d < 0
    )
    if evidence.flow_verified:
        reasons.append("5/20-day capital flows verified")
    else:
        reasons.append("capital flows unverified")

    if channel.sample_is_actionable and channel.action == "downside":
        return Decision(
            "downside",
            "The best historical trend-channel downside region is active; tighten exposure by plan.",
            "high" if flow_negative or evidence.adverse_event_verified else "medium",
            tuple(reasons),
        )
    if channel.sample_is_actionable and channel.action == "upside":
        if flow_negative or evidence.adverse_event_verified:
            return Decision(
                "observe",
                "Trend-channel upside region is active, but conflicting verified risk limits action to observation or a pre-sized probe.",
                "medium",
                tuple(reasons),
            )
        return Decision(
            "upside",
            "The best historical trend-channel upside region is active; proceed only with the pre-sized staged plan.",
            "high" if evidence.flow_verified else "medium",
            tuple(reasons),
        )
    if channel.sample_is_actionable and channel.action == "hold":
        return Decision(
            "hold",
            "Keep existing exposure and wait for the historical trend-channel exit trigger.",
            "medium",
            tuple(reasons),
        )

    if flow_negative or evidence.adverse_event_verified:
        return Decision(
            "observe",
            "Tighten risk and wait for trend-channel plus confirmation-indicator agreement.",
            "low",
            tuple(reasons),
        )
    return Decision(
        "observe",
        "No actionable trend-channel signal; keep the conclusion conditional.",
        "low",
        tuple(reasons),
    )


def channel_position_wording(position_pct: float) -> str:
    """Keep judgement wording consistent with the actual channel band position."""
    if position_pct > 100:
        return "above_upper_band_downside_region"
    if position_pct < 0:
        return "below_lower_band_upside_region"
    if position_pct <= 8:
        return "near_lower_band"
    if position_pct >= 92:
        return "near_upper_band"
    return "inside_band"
