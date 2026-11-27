
import unittest
from src.csp import solve_csp


class TestCSP(unittest.TestCase):

    def test_both_methods(self):
        self.assertEqual(
            solve_csp(85, True, 30),
            ["Fog Collector", "Special Material"]
        )

    def test_special_material(self):
        self.assertEqual(
            solve_csp(75, False, 40),
            ["Special Material"]
        )

    def test_no_solution(self):
        self.assertEqual(
            solve_csp(30, False, 10),
            []
        )

    def test_missing_data(self):
        self.assertEqual(
            solve_csp(None, True, 30),
            []
        )

    def test_invalid_humidity(self):
        self.assertEqual(
            solve_csp(120, True, 30),
            []
        )


if __name__ == "__main__":
    unittest.main()
