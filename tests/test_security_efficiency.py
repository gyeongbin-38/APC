import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "benchmarks/security-efficiency/results.json"


class SecurityEfficiencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RESULTS.read_text(encoding="utf-8"))

    def test_strict_coverage_prefers_always_short_guard(self):
        winners = self.data["winners_by_minimum_guard_coverage"]
        for noise, thresholds in winners.items():
            self.assertEqual(
                thresholds["0.99"],
                "always_short_guard",
                f"99% guard-presence target regressed at routing noise {noise}",
            )

    def test_full_policy_is_materially_more_expensive(self):
        payload = self.data["policy_token_proxy"]
        self.assertGreater(
            payload["always_full_policy"],
            10 * payload["always_short_guard"],
        )

    def test_lazy_guard_is_routing_dependent(self):
        noise = self.data["routing_noise"]
        self.assertLess(noise["0.05"]["lazy_risky_recall"], 0.95)
        self.assertLess(noise["0.1"]["lazy_risky_recall"], noise["0.05"]["lazy_risky_recall"])


if __name__ == "__main__":
    unittest.main()
