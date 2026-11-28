import unittest
from src.model import Inputs
from src.decision import evaluate

class DecisionTests(unittest.TestCase):
    def run_case(self,**kwargs):
        p=dict(humidity=85,temperature_c=25,fog_observed=True,energy_budget_kwh=5)
        p.update(kwargs)
        return evaluate(Inputs(**p))
    def test_happy_path(self):
        self.assertEqual(self.run_case()['status'],'SUCCESS')
    def test_plan_exists(self):
        self.assertIsNotNone(self.run_case()['recommended'])
    def test_no_solution(self):
        self.assertEqual(self.run_case(energy_budget_kwh=0)['status'],'NO_FEASIBLE_METHOD')
    def test_missing_humidity(self):
        self.assertEqual(self.run_case(humidity=None)['status'],'SENSOR_WARNING')
    def test_invalid_humidity(self):
        self.assertEqual(self.run_case(humidity=120)['status'],'SENSOR_WARNING')
    def test_missing_temperature(self):
        self.assertEqual(self.run_case(temperature_c=None)['status'],'SENSOR_WARNING')
    def test_bad_energy(self):
        self.assertEqual(self.run_case(energy_budget_kwh=-5)['status'],'SENSOR_WARNING')
    def test_missing_fog_does_not_claim_certain(self):
        r=self.run_case(fog_observed=None)
        self.assertEqual(r['fog_probability'],.35)
        self.assertTrue(r['warnings'])
    def test_negative_fog_exclusion_reason(self):
        r=self.run_case(fog_observed=False)
        self.assertIn('Fog probability below confidence threshold',r['excluded']['Fog Collector'])
    def test_dry_air_mof_not_arbitrarily_blocked(self):
        r=self.run_case(humidity=30, fog_observed=False)
        self.assertEqual(r['recommended']['method'], 'MOF Collector')
    def test_zero_humidity_excludes_mof(self):
        r=self.run_case(humidity=0, fog_observed=False)
        self.assertIn('Zero humidity: no atmospheric water vapor available',r['excluded']['MOF Collector'])
    def test_highest_score_selected(self):
        r=self.run_case()
        self.assertEqual(r['recommended']['score_demo'],max(x['score_demo'] for x in r['candidates']))
    def test_plan_under_budget(self):
        r=self.run_case(energy_budget_kwh=2)
        self.assertLessEqual(r['recommended']['energy_kwh_demo'],2)
    def test_invalid_fog_type(self):
        self.assertEqual(self.run_case(fog_observed='yes')['status'],'SENSOR_WARNING')
    def test_nan_input(self):
        self.assertEqual(self.run_case(humidity=float('nan'))['status'],'SENSOR_WARNING')
    def test_bad_model_probability(self):
        self.assertEqual(self.run_case(prior_fog=1.0)['status'],'SENSOR_WARNING')
    def test_unsafe_has_no_recommendation(self):
        self.assertIsNone(self.run_case(safety_ok=False)['recommended'])
