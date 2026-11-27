
import unittest
from src.rules import evaluate_rules


class TestRules(unittest.TestCase):

    def test_fog_collector(self):
        result = evaluate_rules(85, True, 30)
        self.assertEqual(result, "Fog Collector")

    def test_special_material(self):
        result = evaluate_rules(75, False, 40)
        self.assertEqual(result, "Special Material")

    def test_missing_sensor(self):
        result = evaluate_rules(None, True, 30)
        self.assertEqual(result, "Sensor Warning")

    def test_no_suitable_method(self):
        result = evaluate_rules(30, False, 10)
        self.assertEqual(result, "No Suitable Method")


if __name__ == "__main__":
    unittest.main()
