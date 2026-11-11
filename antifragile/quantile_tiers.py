"""Re-anchor conventional thresholds to the distribution they claim to describe.

A threshold inherited from habit can be off by nearly an order of magnitude.
Before labelling a reading "strong" or "weak", ask where that value actually
sits inside its own history. This module builds quantile bands from observed
samples and exposes a helper that reports the empirical percentile of a legacy
cut-off, so a scale mismatch can be demonstrated instead of asserted.

Higher values are assumed to mean stronger conditions. Callers with an inverted
semantic should negate or transform their series before building a scale.
"""

from __future__ import annotations

from dataclasses import dataclass
from bisect import bisect_left

# Ordered from the weakest to the strongest reading.
TIER_NAMES = ("panic", "weak", "neutral", "strong", "crowded_hot")
DEFAULT_CUTS = (0.10, 0.35, 0.65, 0.90)


def quantile(sorted_values: tuple[float, ...] | list[float], q: float) -> float:
    """Linear-interpolated quantile; q in [0, 1]."""
    if not sorted_values:
        raise ValueError("samples must not be empty")
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be within [0, 1]")
    values = sorted(sorted_values)
    if len(values) == 1:
        return float(values[0])
    pos = q * (len(values) - 1)
    lower = int(pos)
    upper = min(lower + 1, len(values) - 1)
    weight = pos - lower
    return float(values[lower] * (1 - weight) + values[upper] * weight)


@dataclass(frozen=True)
class TierScale:
    boundaries: tuple[float, float, float, float]
    sample_size: int
    cuts: tuple[float, float, float, float] = DEFAULT_CUTS

    def tier_for(self, value: float) -> str:
        """Left-closed, right-open bands: <P10 panic ... >=P90 crowded."""
        for boundary, name in zip(self.boundaries, TIER_NAMES[:-1]):
            if value < boundary:
                return name
        return TIER_NAMES[-1]

    def label_map(self) -> dict[str, str]:
        return {
            "below_p10": "panic / risk-off pricing",
            "p10_p35": "weak",
            "p35_p65": "neutral",
            "p65_p90": "strong",
            "above_p90": "crowded / overheated",
        }


def build_tiers(
    samples: tuple[float, ...] | list[float],
    cuts: tuple[float, float, float, float] = DEFAULT_CUTS,
) -> TierScale:
    """Build five bands from an observed series. Never hard-code the numbers."""
    if len(samples) < 5:
        raise ValueError("at least five observations are required")
    if not cuts == tuple(sorted(cuts)) or cuts[0] <= 0 or cuts[-1] >= 1:
        raise ValueError("cuts must be four increasing quantiles inside (0, 1)")
    ordered = tuple(float(v) for v in sorted(samples))
    boundaries = tuple(quantile(ordered, q) for q in cuts)
    return TierScale(boundaries, len(ordered), cuts)  # type: ignore[arg-type]


def classify(value: float, scale: TierScale) -> str:
    """Classify a reading against a distribution-derived scale."""
    return scale.tier_for(value)


def legacy_percentile(legacy_threshold: float, samples) -> float:
    """Return the empirical percentile (0-100) of an inherited cut-off.

    If a "strong" threshold lands near P15, the old scale was describing a
    different distribution. This is the evidence needed to retire it.
    """
    ordered = sorted(float(v) for v in samples)
    if not ordered:
        raise ValueError("samples must not be empty")
    below = bisect_left(ordered, legacy_threshold)
    return 100.0 * below / len(ordered)
