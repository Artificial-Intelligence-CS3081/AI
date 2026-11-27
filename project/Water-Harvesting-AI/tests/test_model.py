
import unittest

from src.csp import solve_csp
from src.decision import estimate_water, safe_recommend_method


class TestImprovedModel(unittest.TestCase):

    def test_fog_requires_energy(self):
        self.assertEqual(solve_csp(85, True, 4), [])

    def test_material_requires_energy(self):
        self.assertEqual(solve_csp(85, False, 19), [])

    def test_water_changes_with_humidity(self):
        low = estimate_water("Special Material", 60)
        high = estimate_water("Special Material", 90)

        self.assertGreater(high, low)

    def test_fog_yield_changes_with_humidity(self):
        low = estimate_water("Fog Collector", 40)
        high = estimate_water("Fog Collector", 85)

        self.assertGreater(high, low)

    def test_agent_recommendation(self):
        result = safe_recommend_method(85, True, 30)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(
            result["recommended"],
            "Special Material"
        )


if __name__ == "__main__":
    unittest.main()
