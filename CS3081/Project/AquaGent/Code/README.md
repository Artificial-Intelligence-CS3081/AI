# AquaGent — Uncertainty + CSP (CS3081)

Educational water-harvesting decision-support simulator comparing **Fog Collector** and **MOF Collector** (the selected Raschel-type mesh and MOF-303 material references).

## AI methods

- **2A Uncertainty / Bayesian inference:** one binary fog-sensor observation updates P(Fog) from a user-defined prior, sensitivity and specificity. Missing observation preserves the prior (no fabricated reading).
- **2B Constraint Satisfaction:** two decision variables (harvesting method and operating duration). Backtracking enumerates assignments that satisfy safety, available time, energy budget and simulated weather constraints.
- **Optimization:** among feasible plans only, maximize a *demonstration score* = illustrative liters / (1 + illustrative energy / available energy budget). Operator can approve/reject in UI; this never controls equipment.

## Important limitations

**No scientific validation has been performed.** Bayesian parameters are hypothetical; no actual calibration data were obtained. MOF suitability outside zero RH, fog LWC, mesh efficiency and all energy rates are **demonstration assumptions**, not verified equipment specifications. `water_liters_demo` and `energy_kwh_demo` may not be represented as measured field results. The probabilistic model treats fog presence as a binary event and one sensor observation; it does not yet infer fog from humidity or temperature. The independent sensor validation checks ranges, not plausibility of all physically possible failures. Do not use for real industrial decisions.

## Run on Windows (PowerShell)

```powershell
cd AquaGent_Uncertainty_CSP
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m experiments.run_simulation
python -m streamlit run app.py
```

Open the local Streamlit URL printed in the terminal (often http://localhost:8501).

## Workflow
1. Enter weather/plant data. The sidebar adjusts simulation assumptions for fog uncertainty.
2. Bayesian inference calculates posterior fog probability.
3. CSP enumerates feasible `(method, hours)` assignments.
4. Score ranks feasible plans and shows the rationale and exclusions.
5. Operator selects Approve or Reject (simulated only).
6. View results and download run history CSV. Clear history from the UI.

## Files
- `src/model.py`: input schema, validation, Raschel fog flux scenario and MOF-303 literature-reference scenario
- `src/uncertainty.py`: Bayesian update
- `src/csp.py`: constraint checks and backtracking CSP
- `src/decision.py`: integrated agent and scoring
- `app.py`: Streamlit dashboard, operator approval, CSV export
- `experiments/run_simulation.py`: reproducible simulated scenarios
- `tests/`: unit tests (including scientific-reference scenario checks)
- `docs/SCIENTIFIC_ASSUMPTIONS.md`: equations, citations, assumptions and limitations

## Existing project migration
This ZIP is a **separate V2 project**. Do not overwrite the current `Water-Harvesting-AI` folder until you back it up. Old modules such as `rules.py`, `sensor_guard.py`, and `decision.py` have different APIs and old tests should not be mixed into this project without porting. The current V2 doesn't claim to pass the old 32 tests; it has its own test suite.

## Before submission
- Confirm instructor approval for two students (official guidelines list 3–4).
- Obtain measured or published values for an *identified* MOF and fog net; define unit size, location and period.
- Calibrate sensor sensitivity/specificity and fog prior, and validate model vs held-out data.
- Evaluate decision safety, correct abstention, and sensitivity to uncertainty settings.
- Add project-specific research citations, GitHub link, ACL report, poster and portfolio site.
- Follow your instructor's academic integrity guidance on AI-generated code/content and attribute contributions appropriately.

## Scientific-reference update (November 2026)
The selected simulated materials are **Raschel-type polymer fog mesh** and **MOF-303**. The model uses an explicit fog flux scenario and a *daily literature observation* of 0.210 L/kg/day for MOF-303 (Death Valley). **Neither is a forecast for Jeddah.** The MOF daily observation is scaled to shorter durations as an explicitly fictional classroom simplification, and assumed energy rates are not calibrated. See `docs/SCIENTIFIC_ASSUMPTIONS.md`.

The `app.py` interface now includes editable mesh area, mesh efficiency, assumed fog liquid-water content and MOF mass; the existing Bayesian inference, CSP planning, operator approval, run history and CSV export remain intact.

## Scientific-model adjustment (November 2026)

- Removed unsupported 60% RH hard MOF cutoff. Only RH=0 excludes MOF in the simple reference scenario, with no claim of performance at low RH.
- Replaced subtraction of L and kWh with a *dimensionless, declared demonstration heuristic*; energy limits still act as CSP hard constraints.
- Literature MOF daily reference, fog-flux formula, and illustrative energy rates are unchanged; no field calibration is claimed.
- The Streamlit UI in `app.py` is **unchanged**.
