# Evidence register and model boundaries

**Chosen demonstration materials (based on the AquaGent literature review):**

- **Fog Collector:** conventional **Raschel-type polymer mesh**. Its numerical forecast is a constant-fog flux *scenario*, requiring assumed fog liquid-water content, mesh area, wind speed and capture efficiency. The literature review calls for local Jeddah fog-frequency, geometry and wind measurement before any site-specific claims.
- **MOF Collector:** **MOF-303 sorbent bed**. Song et al., *Nature Water* (2023), DOI: 10.1038/s44221-023-00103-7 reports **210 g water/kg MOF/day** for the Death Valley field device and **285 g/kg/day** for a Berkeley field setting. This project uses the **Death Valley** figure as a *reference daily observation*, not a Jeddah prediction.

## Equations used

1. Fog: `L/hour = 3.6 × LWC(g/m³) × wind(m/s) × mesh_area(m²) × mesh_efficiency`.
   - For uncertain fog, simulation **weights the above rate by Bayesian P(fog)** as a scenario expected value. This is a simplified model, not a learned physical response function; wind alignment, fog droplet spectrum, time variability and wettability are unmodeled.
2. MOF-303: `scenario_liters = 0.210 × MOF_mass_kg × (hours / 24)`.
   - **Important:** a daily outdoor field observation is divided by 24 for a classroom scenario *only*. Real MOF uptake, regeneration, condensation efficiency and cycling are nonlinear. Do not interpret 1h/2h/4h estimates as measured device performance.
3. Energy: `assumed_electrical_kWh = operating_hours × selected_demo_rate_kWh_per_hour`, using illustrative **0.10 kWh/h Fog** and **1.20 kWh/h MOF**. These do **not** derive from literature field measurements and don't represent a validated MOF thermal-regeneration heat balance. The demo score is `scenario_liters / (1 + assumed_energy_kWh / available_energy_budget_kWh)` for feasible positive-energy-budget plans. This dimensionless **ranking heuristic** avoids subtracting unmatched L and kWh; it is not a validated scientific, financial, or energy-efficiency objective.

## CSP / Bayesian limitations

- The former **MOF minimum humidity = 60%** demonstration threshold was removed because it is unsupported as a material lower bound. In this classroom scenario only, MOF is blocked at **0% RH** (absence of atmospheric vapor), not at 30% or 40%; this is **not** a validated adsorption isotherm or evidence of physical device performance at each RH. The pro-rata MOF volume still uses the Death Valley daily reference at all RH > 0, without climate adaptation. Scientific calibration remains required.
- The prior fog probability, binary sensor sensitivity, specificity and `P(fog)` cutoff are user-selected assumptions. They are **not calibrated against Jeddah measurements**.
- Actual harvesting and potable-water safety require field testing, water quality testing, energy measurements, and qualified operational approval.

## Evidence and attribution

- User-provided *AquaGent Literature Review*, sections 4–7, 9; Song et al. 2023 listed as reference [8], Saudi fog feasibility as [5], material-screening reviews [2–3,9].
- Song et al., **MOF water harvester produces water from Death Valley desert air in ambient sunlight**, *Nature Water* (2023), https://doi.org/10.1038/s44221-023-00103-7.
- Alzahrani & Abdelbaki, **Fog harvesting implementation as a sustainable water source: a feasibility study in Al-Baha, Saudi Arabia** (2025), https://doi.org/10.1007/s43995-025-00250-w.

No coefficient in this code is claimed to be calibrated or independently verified for the proposed Jeddah pilot. The 0.210 value is traceable to a published field observation, not a transfer-validatable physical forecast.
