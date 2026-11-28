import unittest
import tempfile
from pathlib import Path
from experiments.run_simulation import run, CASES

class SimulationTests(unittest.TestCase):
    def test_scenarios(self):
        self.assertGreaterEqual(len(CASES),10)
    def test_csv_output(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'results.csv'
            rows=run(path)
            self.assertTrue(path.exists())
            self.assertEqual(len(rows),len(CASES))
    def test_warnings_present(self):
        with tempfile.TemporaryDirectory() as temp:
            rows=run(Path(temp)/'results.csv')
            self.assertTrue(any(r['status']=='SENSOR_WARNING' for r in rows))
