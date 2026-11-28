"""Reference scenario tests; do not imply field validation."""
import unittest
from src.model import Inputs, validate, predicted_water_liters, MOF_REFERENCE_L_KG_DAY
from src.decision import evaluate


class ReferenceModelTests(unittest.TestCase):
    def setup_data(self, **overrides):
        values = dict(humidity=85, temperature_c=25, fog_observed=True,
                      energy_budget_kwh=6, max_hours=4, wind_m_s=2.0)
        values.update(overrides)
        return Inputs(**values)

    def test_fog_flux_expected_volume(self):
        data = self.setup_data()
        # 3.6 * 0.2 * 2 * 2 * .3 * 4 * .8 = 2.7648
        self.assertEqual(predicted_water_liters('Fog Collector', data, 4, .8), 2.765)

    def test_fog_zero_lwc(self):
        data = self.setup_data(fog_lwc_g_m3=0)
        self.assertEqual(predicted_water_liters('Fog Collector', data, 4, .8), 0)
        self.assertNotEqual(evaluate(data)['recommended']['method'], 'Fog Collector')

    def test_fog_area_effect(self):
        small = predicted_water_liters('Fog Collector', self.setup_data(), 4, .8)
        large = predicted_water_liters('Fog Collector', self.setup_data(mesh_area_m2=4), 4, .8)
        self.assertGreater(large, small)

    def test_mof_reference_scenario(self):
        data = self.setup_data()
        self.assertEqual(MOF_REFERENCE_L_KG_DAY, 0.210)
        self.assertEqual(predicted_water_liters('MOF Collector', data, 4, .8), .035)

    def test_mof_mass_effect(self):
        a = predicted_water_liters('MOF Collector', self.setup_data(), 8, .8)
        b = predicted_water_liters('MOF Collector', self.setup_data(mof_mass_kg=2), 8, .8)
        self.assertEqual(round(b, 3), round(2*a, 3))

    def test_invalid_material_parameter(self):
        self.assertTrue(validate(self.setup_data(mesh_efficiency=1.4)))
        self.assertEqual(evaluate(self.setup_data(mof_mass_kg=0))['status'], 'SENSOR_WARNING')

    def test_uncertainty_modifies_fog_estimate(self):
        d = self.setup_data()
        low = predicted_water_liters('Fog Collector', d, 4, .2)
        high = predicted_water_liters('Fog Collector', d, 4, .8)
        self.assertGreater(high, low)


if __name__ == '__main__':
    unittest.main()
