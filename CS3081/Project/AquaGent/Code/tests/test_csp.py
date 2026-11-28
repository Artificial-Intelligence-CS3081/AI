import unittest
from src.model import Inputs
from src.csp import solve_csp, failed_constraints
from src.uncertainty import fog_posterior

class CSPTests(unittest.TestCase):
    def d(self,**kwargs):
        params=dict(humidity=85,temperature_c=25,fog_observed=True,energy_budget_kwh=5)
        params.update(kwargs)
        return Inputs(**params)
    def solutions(self, **kwargs):
        data=self.d(**kwargs)
        return solve_csp(data,fog_posterior(data.fog_observed,data.prior_fog,data.sensor_sensitivity,data.sensor_specificity))
    def test_two_variables(self):
        self.assertTrue(all(set(s)=={'method','hours'} for s in self.solutions()))
    def test_both_methods_feasible(self):
        self.assertEqual({x['method'] for x in self.solutions()}, {'Fog Collector','MOF Collector'})
    def test_max_duration(self):
        self.assertTrue(all(s['hours']<=2 for s in self.solutions(max_hours=2)))
    def test_energy_budget(self):
        self.assertTrue(all(s['hours']*(.1 if s['method']=='Fog Collector' else 1.2)<=1 for s in self.solutions(energy_budget_kwh=1)))
    def test_no_energy(self):
        self.assertFalse(self.solutions(energy_budget_kwh=0))
    def test_no_safety(self):
        self.assertFalse(self.solutions(safety_ok=False))
    def test_dry_air_can_use_mof_in_reference_scenario(self):
        self.assertTrue(any(s['method']=='MOF Collector' for s in self.solutions(humidity=30,fog_observed=False)))
    def test_zero_humidity_excludes_mof(self):
        self.assertTrue(all(s['method']!='MOF Collector' for s in self.solutions(humidity=0)))
    def test_negative_fog_excludes_fog(self):
        self.assertTrue(all(s['method']!='Fog Collector' for s in self.solutions(fog_observed=False)))
    def test_missing_fog_excludes_fog_at_threshold(self):
        self.assertTrue(all(s['method']!='Fog Collector' for s in self.solutions(fog_observed=None)))
    def test_zero_wind(self):
        self.assertTrue(all(s['method']!='Fog Collector' for s in self.solutions(wind_m_s=0)))
    def test_constraint_explanation(self):
        self.assertIn('Safety inspection failed',failed_constraints('MOF Collector',1,self.d(safety_ok=False),.8))
