import unittest
from src.uncertainty import fog_posterior

class BayesianTests(unittest.TestCase):
    def test_positive_evidence(self):
        self.assertAlmostEqual(fog_posterior(True,.35,.9,.9),.315/.38)
    def test_negative_evidence(self):
        self.assertAlmostEqual(fog_posterior(False,.35,.9,.9),.035/.62)
    def test_missing_evidence_prior(self):
        self.assertEqual(fog_posterior(None,.35,.9,.9),.35)
    def test_positive_strengthens_prior(self):
        self.assertGreater(fog_posterior(True,.35,.9,.9), .35)
    def test_negative_weakens_prior(self):
        self.assertLess(fog_posterior(False,.35,.9,.9), .35)
    def test_invalid_observation(self):
        with self.assertRaises(ValueError):fog_posterior('yes',.35,.9,.9)
