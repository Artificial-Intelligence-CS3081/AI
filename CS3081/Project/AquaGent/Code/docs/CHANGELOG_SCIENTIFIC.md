# Changes relative to supplied AquaGent_Clean_Final_UI (3).zip

1. `src/csp.py`: remove unsupported MOF-303 60%-RH hard cutoff; require RH > 0 for the classroom scenario only. Do not interpret this as a validated MOF response curve.
2. `src/decision.py`: replace demo score liters − 0.8 × kWh (mixed units) with `liters / (1 + demo_kWh / demo_budget_kWh)`, a declared heuristic for **feasible** plans. No claim of optimal engineering design.
3. `src/model.py`: remove obsolete score coefficient; no other formulas or parameters changed.
4. Updated relevant unit tests, evidence/README and regenerated simulated CSV.
5. `app.py` intentionally left byte-for-byte untouched; the UI and approval remain as provided in the uploaded ZIP. If you have a newer locally fixed app.py, retain it and replace only `src` and `docs` from this ZIP.

**Outstanding scientific gaps:** MOF measured isotherm, regeneration and condenser efficiency, field energy requirements; site fog LWC and actual fog frequency; calibrated sensor probabilities; empirical comparison to measured liquid water.
