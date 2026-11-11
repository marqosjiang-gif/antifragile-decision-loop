"""Conservative defer gate: translate a business rule into an auditable decision.

Design intent, and the part worth reusing: the system *consumes* human-registered
support facts; it never infers them from unstructured text. Anything it cannot
verify degrades to INSUFFICIENT rather than ALLOW. An ALLOW verdict only lifts a
pause on new additions -- it never authorises an immediate increase.

Domain-neutral, standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

SUPPORT_BASES = ("disclosed", "in_transit", "analyst")
MAX_CHECKPOINT_DAYS = 180
DeferState = str  # NOT_APPLICABLE | FORBID | INSUFFICIENT | ALLOW


@dataclass(frozen=True)
class SupportRecord:
    """Human-registered, machine-consumed. `inferred=True` is always rejected."""
    subject: str
    basis: str
    as_of: date
    verified: bool = False
    inferred: bool = False


@dataclass(frozen=True)
class GateInput:
    breach: bool
    report_date: date
    subject_in_scope: bool = True
    support: SupportRecord | None = None
    next_checkpoint: date | None = None
    support_max_age_days: int = 30


@dataclass(frozen=True)
class DeferVerdict:
    state: DeferState
    action: str
    reasons: tuple[str, ...]

    @property
    def allows_new_additions(self) -> bool:
        return self.state == "ALLOW"


def evaluate_defer(g: GateInput) -> DeferVerdict:
    """Breach first, then registered support, then a forward checkpoint."""
    if not g.subject_in_scope or not g.breach:
        return DeferVerdict(
            "NOT_APPLICABLE", "No intervention; the normal decision path applies.",
            ("no confirmed breach or subject out of gate scope",),
        )
    base = ("confirmed breach: automatic new-addition trigger is void",)
    s = g.support
    if s is None:
        return DeferVerdict(
            "FORBID", "Keep the pause on new additions.",
            base + ("no registered support record",),
        )
    if s.inferred:
        return DeferVerdict(
            "INSUFFICIENT", "Keep the pause; ask a human to register the support fact.",
            base + ("machine-inferred support is not an acceptable basis",),
        )
    if not s.verified:
        return DeferVerdict(
            "INSUFFICIENT", "Keep the pause until the support record is verified.",
            base + ("support record unverified",),
        )
    if s.basis not in SUPPORT_BASES:
        return DeferVerdict(
            "INSUFFICIENT", "Keep the pause; register one of the accepted bases.",
            base + (f"unsupported basis: {s.basis}",),
        )
    age = (g.report_date - s.as_of).days
    if age < 0 or age > g.support_max_age_days:
        return DeferVerdict(
            "INSUFFICIENT", "Keep the pause; refresh the dated support record.",
            base + (f"support record is {age} days old",),
        )
    if g.next_checkpoint is None or g.next_checkpoint <= g.report_date:
        return DeferVerdict(
            "INSUFFICIENT", "Keep the pause; a forward checkpoint is required.",
            base + ("no forward verification checkpoint",),
        )
    horizon = (g.next_checkpoint - g.report_date).days
    if horizon > MAX_CHECKPOINT_DAYS:
        return DeferVerdict(
            "INSUFFICIENT", "Keep the pause; the checkpoint is beyond the approved horizon.",
            base + (f"checkpoint in {horizon} days",),
        )
    return DeferVerdict(
        "ALLOW",
        "Pause on new additions is lifted, but any increase is deferred until the "
        "checkpoint and must re-enter the normal trigger layer afterwards.",
        base + (
            f"registered basis: {s.basis}",
            f"checkpoint in {horizon} days",
            "no automatic increase is authorised by this verdict",
        ),
    )
