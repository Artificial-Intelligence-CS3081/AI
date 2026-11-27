
METHODS = ["Fog Collector", "Special Material"]

# Experimental requirements, not real equipment data
ENERGY_REQUIREMENTS = {
    "Fog Collector": 5.0,
    "Special Material": 20.0
}


def check_constraints(method, humidity, fog_detected, energy):
    """Check weather and energy constraints."""

    if method not in METHODS:
        return False

    if energy < ENERGY_REQUIREMENTS[method]:
        return False

    if method == "Fog Collector":
        return fog_detected is True

    if method == "Special Material":
        return humidity >= 60

    return False


def solve_csp(humidity, fog_detected, energy):
    """Return all feasible water harvesting methods."""

    import math

    if (
        isinstance(humidity, bool)
        or not isinstance(humidity, (int, float))
        or not math.isfinite(humidity)
        or not 0 <= humidity <= 100
        or type(fog_detected) is not bool
        or isinstance(energy, bool)
        or not isinstance(energy, (int, float))
        or not math.isfinite(energy)
        or energy < 0
    ):
        return []

    solutions = []

    for method in METHODS:
        if check_constraints(
            method, humidity, fog_detected, energy
        ):
            solutions.append(method)

    return solutions

def explain_constraints(method, humidity, fog_detected, energy):
    """Explain why a method is not feasible."""

    reasons = []

    if method not in METHODS:
        return ["Unknown harvesting method"]

    if (
        humidity is None
        or fog_detected is None
        or energy is None
    ):
        return ["Missing sensor data"]

    if method == "Fog Collector":
        if fog_detected is not True:
            reasons.append("Fog is not detected")

    if method == "Special Material":
        if humidity < 60:
            reasons.append("Humidity is below 60%")

    if energy < ENERGY_REQUIREMENTS[method]:
        reasons.append("Insufficient available energy")

    return reasons
