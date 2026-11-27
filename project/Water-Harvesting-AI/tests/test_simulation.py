
import unittest
from collections import Counter

from experiments.run_simulation import (
    SCENARIOS,
    run_simulation
)


class TestSimulation(unittest.TestCase):

    def test_scenario_count(self):
        self.assertEqual(len(SCENARIOS), 8)

    def test_expected_status_counts(self):
        results = run_simulation()

        counts = Counter(
            result["status"] for result in results
        )

        self.assertEqual(counts["SUCCESS"], 3)
        self.assertEqual(counts["SENSOR_WARNING"], 3)
        self.assertEqual(
            counts["NO_FEASIBLE_METHOD"], 2
        )

    def test_warning_has_no_recommendation(self):
        results = run_simulation()

        for result in results:
            if result["status"] == "SENSOR_WARNING":
                self.assertIsNone(
                    result["recommended"]
                )


if __name__ == "__main__":
    unittest.main()
