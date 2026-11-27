
import unittest

from src.sensor_guard import validate_sensor_data
from src.decision import safe_recommend_method


class TestSensorGuard(unittest.TestCase):

    def test_valid_readings(self):
        result = validate_sensor_data(85, True, 30)
        self.assertTrue(result["valid"])

    def test_missing_humidity(self):
        result = validate_sensor_data(None, True, 30)
        self.assertFalse(result["valid"])

    def test_invalid_humidity(self):
        result = validate_sensor_data(120, True, 30)
        self.assertIn(
            "Invalid humidity reading",
            result["errors"]
        )

    def test_invalid_energy(self):
        result = validate_sensor_data(85, True, -5)
        self.assertFalse(result["valid"])

    def test_invalid_fog_sensor(self):
        result = validate_sensor_data(85, "yes", 30)
        self.assertFalse(result["valid"])

    def test_agent_stops_on_bad_data(self):
        result = safe_recommend_method(120, True, 30)
        self.assertEqual(
            result["status"],
            "SENSOR_WARNING"
        )
        self.assertIsNone(result["recommended"])


if __name__ == "__main__":
    unittest.main()
