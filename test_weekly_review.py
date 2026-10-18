import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from weekly_review import build_report, load_focus_list


class WeeklyReviewTests(unittest.TestCase):
    def test_local_focus_list_rejects_exposure_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "focus_list.local.json"
            path.write_text(json.dumps({"subjects": [{
                "code": "EXAMPLE-001", "exchange": "DEMO", "name": "Example", "shares": 100
            }]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_focus_list(path)

    def test_report_records_time_boundaries(self):
        report = build_report(date(2026, 8, 2), [{
            "code": "EXAMPLE-001", "exchange": "DEMO", "name": "Example"
        }], Path("focus_list.local.json"))
        self.assertIn("evidence_cutoff:", report)
        self.assertIn("validation_window: 2026-08-03 open", report)
        self.assertIn("decision_status: research_only", report)

    def test_report_records_market_profile_without_exposure_data(self):
        report = build_report(
            date(2026, 8, 2),
            [{"code": "EXAMPLE-001", "exchange": "DEMO", "name": "Example instrument"}],
            Path("focus_list.local.json"),
            market_profile="demo",
        )
        self.assertIn("market_profile: demo", report)
        self.assertNotIn("shares:", report)
        self.assertNotIn("cost:", report)


if __name__ == "__main__":
    unittest.main()
