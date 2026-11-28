"""AquaGent reference-scenario model, NOT calibrated for Jeddah.

Fog: liquid-water flux across a Raschel-type mesh (assumed LWC/efficiency).
MOF-303: illustrative pro-rata share of Song et al. 2023 Death Valley
outdoor daily observation, not a physically validated hourly production rate.
Energy: purely illustrative electrical equivalents; regeneration heat is not
measured and is not included as a validated thermodynamic estimate.
"""
from dataclasses import dataclass
import math

DURATIONS = (1, 2, 4, 8)
METHODS = ("Fog Collector", "MOF Collector")
MATERIALS = {"Fog Collector": "Raschel-type polymer mesh", "MOF Collector": "MOF-303 sorbent bed"}
ENERGY_RATE_KWH = {"Fog Collector": 0.10, "MOF Collector": 1.20}  # DEMO kWh/h

MOF_REFERENCE_L_KG_DAY = 0.210  # Song et al. 2023, outdoor device, Death Valley


@dataclass(frozen=True)
class Inputs:
    humidity: float | None
    temperature_c: float | None
    fog_observed: bool | None
    energy_budget_kwh: float | None
    max_hours: int = 4
    safety_ok: bool = True
    wind_m_s: float = 2.0
    prior_fog: float = 0.35
    sensor_sensitivity: float = 0.90
    sensor_specificity: float = 0.90
    min_fog_confidence: float = 0.75
    mesh_area_m2: float = 2.0
    mesh_efficiency: float = 0.30
    fog_lwc_g_m3: float = 0.20
    mof_mass_kg: float = 1.0


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate(data: Inputs):
    problems = []
    if not is_number(data.humidity) or not 0 <= data.humidity <= 100:
        problems.append("Humidity must be between 0 and 100%.")
    if not is_number(data.temperature_c) or not -30 <= data.temperature_c <= 65:
        problems.append("Temperature must be between -30 and 65 C.")
    if not is_number(data.energy_budget_kwh) or data.energy_budget_kwh < 0:
        problems.append("Energy budget must be nonnegative.")
    if not is_number(data.wind_m_s) or not 0 <= data.wind_m_s <= 30:
        problems.append("Wind speed must be between 0 and 30 m/s.")
    if data.fog_observed is not None and type(data.fog_observed) is not bool:
        problems.append("Fog reading must be True, False or None.")
    if type(data.max_hours) is not int or data.max_hours not in DURATIONS:
        problems.append("Maximum hours must be 1, 2, 4 or 8.")
    if type(data.safety_ok) is not bool:
        problems.append("Safety flag must be boolean.")
    for name, value in [("Prior fog", data.prior_fog), ("Sensitivity", data.sensor_sensitivity),
                        ("Specificity", data.sensor_specificity), ("Confidence threshold", data.min_fog_confidence)]:
        if not is_number(value) or not 0 < value < 1:
            problems.append(f"{name} must lie strictly between 0 and 1.")
    if not is_number(data.mesh_area_m2) or data.mesh_area_m2 <= 0:
        problems.append("Mesh area must be positive.")
    if not is_number(data.mesh_efficiency) or not 0 <= data.mesh_efficiency <= 1:
        problems.append("Mesh efficiency must be from 0 to 1.")
    if not is_number(data.fog_lwc_g_m3) or data.fog_lwc_g_m3 < 0:
        problems.append("Fog liquid-water content must be nonnegative.")
    if not is_number(data.mof_mass_kg) or data.mof_mass_kg <= 0:
        problems.append("MOF-303 mass must be positive.")
    return problems


def fog_water_liters(data: Inputs, hours: int, fog_probability: float):
    """Expected collected liters under a constant simulated fog flux.

    LWC(g/m3)*wind(m/s)*area(m2)*efficiency*3.6 = L/h.
    Bayesian P(fog) weights an uncertain state; not a direct RH conversion.
    """
    rate_l_h = (3.6 * data.fog_lwc_g_m3 * data.wind_m_s
                * data.mesh_area_m2 * data.mesh_efficiency)
    return round(rate_l_h * hours * fog_probability, 3)


def mof_water_liters(data: Inputs, hours: int):
    """Illustrative hours/24 fraction of outdoor DAILY literature observation.

    Not a calibrated short-cycle forecast, uptake isotherm, or Jeddah yield.
    """
    return round(MOF_REFERENCE_L_KG_DAY * data.mof_mass_kg * hours / 24, 3)


def predicted_water_liters(method: str, data: Inputs, hours: int, probability_fog: float):
    if method == "Fog Collector":
        return fog_water_liters(data, hours, probability_fog)
    if method == "MOF Collector":
        return mof_water_liters(data, hours)
    raise ValueError("Unknown harvesting method")
