"""Post-render claim audit: run it AFTER output exists, not only before generation.

Templates drift. A claim that was cautious at generation time can become an
absolute, unattributed statement after formatting. This auditor is read-only:
it reports findings and a rewrite hint; it never silently edits the copy.

Exit codes: 0 = clean, 1 = fixable findings, 2 = hard violation.
"""

from __future__ import annotations

from dataclasses import dataclass

ABSOLUTE_WORDS = ("guaranteed", "definitely", "clearly", "always", "directly")
GENERIC_SUBJECTS = ("", "market", "sector", "industry", "the market", "the sector")


@dataclass(frozen=True)
class Claim:
    subject: str
    statement: str
    anchor: str | None = None          # quantified anchor, with its as-of
    sources: tuple[str, ...] = ()      # named, independently reachable sources
    attributions: tuple[str, ...] = ()  # competing explanations, when they exist
    adjudicated: bool = False          # did the copy pick a winner anyway?


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str                      # "hard" | "fixable"
    subject: str
    hint: str


@dataclass(frozen=True)
class AuditReport:
    findings: tuple[Finding, ...]

    @property
    def rc(self) -> int:
        if any(f.severity == "hard" for f in self.findings):
            return 2
        return 1 if self.findings else 0

    @property
    def ok(self) -> bool:
        return self.rc == 0


def audit_claims(claims) -> AuditReport:
    """Check attribution, quantification and honesty about conflicting drivers."""
    findings: list[Finding] = []
    for claim in claims:
        subject = (claim.subject or "").strip()
        if subject.lower() in GENERIC_SUBJECTS:
            findings.append(Finding(
                "unnamed_subject", "hard", subject or "(blank)",
                "Name the affected subject explicitly; a broad label is not an impact claim.",
            ))
        if len(claim.attributions) >= 2 and claim.adjudicated:
            findings.append(Finding(
                "conflict_adjudicated_without_evidence", "hard", subject,
                "Present competing attributions side by side and leave the call to a human; do not adjudicate in generated copy.",
            ))
        if not (claim.anchor or "").strip():
            findings.append(Finding(
                "missing_quantified_anchor", "fixable", subject,
                "Attach a quantified anchor with an as-of date, or write 'not quantified, no claim made'.",
            ))
        statement = (claim.statement or "").lower()
        if any(word in statement for word in ABSOLUTE_WORDS) and not claim.sources:
            findings.append(Finding(
                "unverified_absolute_wording", "fixable", subject,
                "Soften the absolute wording or attach a dated, verifiable source.",
            ))
        if (claim.anchor or "").strip() and not claim.sources:
            findings.append(Finding(
                "missing_source_label", "fixable", subject,
                "Every number needs a source label and an as-of; an unlabelled number is not evidence.",
            ))
    return AuditReport(tuple(findings))
