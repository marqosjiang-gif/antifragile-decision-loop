"""Regression locks for the Q4-2026 iteration primitives.

Each lock targets a failure that actually happened in the private loop:
- a refreshed source with a forgotten rebuild passing a freshness-only gate,
- a conventional threshold sitting at the wrong percentile,
- cautious copy becoming an absolute, unattributed claim after rendering,
- a machine inferring a support fact that only a human may register.
"""

from __future__ import annotations

import unittest
from datetime import date, timedelta

from antifragile.source_contract import (
    DEFAULT_MAX_AGE_DAYS,
    evaluate_source_contract,
    parse_as_of,
)
from antifragile.quantile_tiers import (
    TIER_NAMES,
    build_tiers,
    classify,
    legacy_percentile,
    quantile,
)
from antifragile.claim_audit import AuditReport, Claim, audit_claims
from antifragile.defer_gate import GateInput, SupportRecord, evaluate_defer


REPORT_DAY = date(2026, 11, 8)


class SourceContractTests(unittest.TestCase):
    def test_fresh_matching_pair_is_publishable(self):
        v = evaluate_source_contract("2026-11-06", "2026-11-06", REPORT_DAY)
        self.assertTrue(v.ok)
        self.assertEqual(v.code, "ok")
        self.assertEqual(v.exit_code, 0)

    def test_fresh_raw_with_stale_artifact_is_blocked(self):
        """The consistency sub-gate: refreshing the pull is not rebuilding the chart."""
        v = evaluate_source_contract("2026-11-06", "2026-10-01", REPORT_DAY)
        self.assertFalse(v.ok)
        self.assertEqual(v.code, "render_drift")
        self.assertEqual(v.exit_code, 2)
        self.assertIn("rebuild", v.message.lower())

    def test_stale_raw_is_blocked(self):
        v = evaluate_source_contract("2026-10-01", "2026-10-01", REPORT_DAY)
        self.assertEqual(v.code, "stale_raw")
        self.assertEqual(v.exit_code, 2)

    def test_future_raw_is_blocked(self):
        v = evaluate_source_contract("2026-11-10", "2026-11-10", REPORT_DAY)
        self.assertEqual(v.code, "stale_raw")

    def test_missing_inputs_are_explicit(self):
        self.assertEqual(evaluate_source_contract(None, "2026-11-06", REPORT_DAY).code, "missing_raw")
        self.assertEqual(evaluate_source_contract("2026-11-06", None, REPORT_DAY).code, "missing_rendered")

    def test_age_boundary_is_inclusive(self):
        raw = REPORT_DAY - timedelta(days=DEFAULT_MAX_AGE_DAYS)
        self.assertTrue(evaluate_source_contract(raw, raw, REPORT_DAY).ok)
        older = raw - timedelta(days=1)
        self.assertFalse(evaluate_source_contract(older, older, REPORT_DAY).ok)

    def test_iso_datetime_string_and_date_object_agree(self):
        self.assertEqual(
            evaluate_source_contract("2026-11-06T09:30:00+08:00", date(2026, 11, 6), REPORT_DAY).code,
            evaluate_source_contract(date(2026, 11, 6), "2026-11-06", REPORT_DAY).code,
        )

    def test_malformed_report_date_raises(self):
        with self.assertRaises(ValueError):
            evaluate_source_contract("2026-11-06", "2026-11-06", "not-a-date")
        self.assertIsNone(parse_as_of("not-a-date"))


class QuantileTierTests(unittest.TestCase):
    def setUp(self):
        self.series = list(range(101))
        self.scale = build_tiers(self.series)

    def test_boundaries_come_from_the_distribution(self):
        self.assertEqual(self.scale.boundaries, (10.0, 35.0, 65.0, 90.0))
        self.assertEqual(self.scale.sample_size, 101)

    def test_all_five_tiers_are_reachable(self):
        seen = {classify(v, self.scale) for v in self.series}
        self.assertEqual(seen, set(TIER_NAMES))

    def test_tiers_are_monotonic_non_decreasing(self):
        labels = [classify(v, self.scale) for v in self.series]
        rank = {name: i for i, name in enumerate(TIER_NAMES)}
        self.assertEqual(labels, sorted(labels, key=lambda n: rank[n]))

    def test_legacy_strong_threshold_can_be_falsified(self):
        """A cut-off sold as 'strong' landing near P12 is a scale error, not an opinion."""
        pct = legacy_percentile(12, self.series)
        self.assertAlmostEqual(pct, 1200 / 101, places=6)
        self.assertLess(pct, 35.0)

    def test_quantile_interpolation_and_validation(self):
        self.assertEqual(quantile([0, 10], 0.5), 5.0)
        with self.assertRaises(ValueError):
            quantile([], 0.5)
        with self.assertRaises(ValueError):
            quantile([1, 2], 1.5)
        with self.assertRaises(ValueError):
            build_tiers([1, 2, 3])
        with self.assertRaises(ValueError):
            build_tiers(self.series, (0.9, 0.35, 0.65, 0.10))

    def test_label_map_covers_five_bands(self):
        self.assertEqual(len(self.scale.label_map()), 5)


class ClaimAuditTests(unittest.TestCase):
    def clean_claim(self, **kwargs):
        base = dict(
            subject="SUBJECT-001",
            statement="A measured effect was observed in the review window.",
            anchor="12.4% as-of 2026-11-06",
            sources=("primary disclosure", "independent verification"),
        )
        base.update(kwargs)
        return Claim(**base)

    def test_complete_claim_is_clean(self):
        self.assertEqual(audit_claims([self.clean_claim()]).rc, 0)

    def test_unnamed_subject_is_a_hard_violation(self):
        report = audit_claims([self.clean_claim(subject="sector")])
        self.assertEqual(report.rc, 2)
        self.assertIn("unnamed_subject", [f.code for f in report.findings])

    def test_adjudicating_between_two_attributions_is_a_hard_violation(self):
        claim = self.clean_claim(attributions=("driver A", "driver B"), adjudicated=True)
        self.assertEqual(audit_claims([claim]).rc, 2)

    def test_presenting_two_attributions_in_parallel_is_allowed(self):
        claim = self.clean_claim(attributions=("driver A", "driver B"), adjudicated=False)
        self.assertEqual(audit_claims([claim]).rc, 0)

    def test_missing_anchor_is_fixable_not_fatal(self):
        report = audit_claims([self.clean_claim(anchor=None)])
        self.assertEqual(report.rc, 1)
        self.assertIn("missing_quantified_anchor", [f.code for f in report.findings])

    def test_absolute_wording_without_sources_is_flagged(self):
        claim = self.clean_claim(statement="This directly benefits the subject.", sources=())
        codes = [f.code for f in audit_claims([claim]).findings]
        self.assertIn("unverified_absolute_wording", codes)

    def test_a_number_without_a_source_label_is_flagged(self):
        claim = self.clean_claim(sources=())
        self.assertIn("missing_source_label", [f.code for f in audit_claims([claim]).findings])

    def test_auditor_is_read_only(self):
        report = audit_claims([self.clean_claim(anchor=None)])
        self.assertIsInstance(report, AuditReport)
        self.assertFalse(report.ok)
        self.assertEqual(report.findings[0].severity, "fixable")


class DeferGateTests(unittest.TestCase):
    def support(self, **kwargs):
        base = dict(subject="SUBJECT-001", basis="disclosed", as_of=date(2026, 11, 5), verified=True)
        base.update(kwargs)
        return SupportRecord(**base)

    def test_no_breach_or_out_of_scope_is_zero_intervention(self):
        self.assertEqual(evaluate_defer(GateInput(False, REPORT_DAY)).state, "NOT_APPLICABLE")
        self.assertEqual(evaluate_defer(GateInput(True, REPORT_DAY, subject_in_scope=False)).state, "NOT_APPLICABLE")

    def test_no_registered_support_keeps_the_pause(self):
        self.assertEqual(evaluate_defer(GateInput(True, REPORT_DAY)).state, "FORBID")

    def test_machine_inferred_support_is_rejected(self):
        g = GateInput(True, REPORT_DAY, support=self.support(inferred=True), next_checkpoint=date(2026, 12, 1))
        self.assertEqual(evaluate_defer(g).state, "INSUFFICIENT")

    def test_unverified_bad_basis_and_stale_records_degrade_conservatively(self):
        cases = [
            self.support(verified=False),
            self.support(basis="rumour"),
            self.support(as_of=date(2026, 9, 1)),
        ]
        for s in cases:
            g = GateInput(True, REPORT_DAY, support=s, next_checkpoint=date(2026, 12, 1))
            self.assertEqual(evaluate_defer(g).state, "INSUFFICIENT", msg=s)

    def test_checkpoint_must_be_forward_and_within_horizon(self):
        valid_support = self.support()
        for checkpoint in (None, REPORT_DAY, date(2026, 11, 1), date(2027, 12, 1)):
            g = GateInput(True, REPORT_DAY, support=valid_support, next_checkpoint=checkpoint)
            self.assertEqual(evaluate_defer(g).state, "INSUFFICIENT", msg=checkpoint)

    def test_allow_only_lifts_the_pause_and_still_defers_increases(self):
        g = GateInput(True, REPORT_DAY, support=self.support(), next_checkpoint=date(2026, 12, 1))
        verdict = evaluate_defer(g)
        self.assertEqual(verdict.state, "ALLOW")
        self.assertTrue(verdict.allows_new_additions)
        self.assertIn("deferred", verdict.action.lower())
        self.assertTrue(any("no automatic increase" in r for r in verdict.reasons))

    def test_forbid_never_authorises_new_additions(self):
        self.assertFalse(evaluate_defer(GateInput(True, REPORT_DAY)).allows_new_additions)


if __name__ == "__main__":
    unittest.main()
