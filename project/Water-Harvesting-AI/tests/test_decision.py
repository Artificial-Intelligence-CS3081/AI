
import unittest
from src.decision import recommend_method


class TestDecision(unittest.TestCase):

    def test_both_methods(self):
        result = recommend_method(85, True, 30)
        self.assertEqual(
            result["recommended"],
            "Special Material"
        )
        self.assertEqual(len(result["options"]), 2)

    def test_fog_only(self):
        result = recommend_method(40, True, 10)
        self.assertEqual(
            result["recommended"],
            "Fog Collector"
        )

    def test_material_only(self):
        result = recommend_method(75, False, 40)
        self.assertEqual(
            result["recommended"],
            "Special Material"
        )

    def test_no_solution(self):
        result = recommend_method(30, False, 10)
        self.assertIsNone(result["recommended"])

    def test_missing_sensor(self):
        result = recommend_method(None, True, 30)
        self.assertIsNone(result["recommended"])

    def test_insufficient_energy(self):
        result = recommend_method(85, True, 0)
        self.assertIsNone(result["recommended"])


if __name__ == "__main__":
    unittest.main()
