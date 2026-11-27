"""Run with: python -m unittest discover -s tests -v"""
import unittest
from src.validation import validate_inputs


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.sample = {"temperature_c": 28, "humidity_pct": 78,
                       "fog_detected": True, "energy_units": 30}

    def test_valid_input(self):
        self.assertEqual(validate_inputs(self.sample), [])

    def test_missing_humidity(self):
        reading = {**self.sample, "humidity_pct": None}
        self.assertTrue(any("humidity_pct" in e for e in validate_inputs(reading)))

    def test_impossible_humidity(self):
        reading = {**self.sample, "humidity_pct": 120}
        self.assertTrue(any("humidity_pct" in e for e in validate_inputs(reading)))


if __name__ == "__main__":
    unittest.main()
