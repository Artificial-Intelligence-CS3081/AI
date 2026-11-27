
from src.csp import solve_csp, ENERGY_REQUIREMENTS
from src.sensor_guard import validate_sensor_data


# Fictional simulation parameters
BASE_WATER = {
    "Fog Collector": 3.0,
    "Special Material": 4.0
}

ENERGY_WEIGHT = 0.05


def estimate_water(method, humidity):
    """
    Educational water yield model.
    NOT validated against physical equipment.
    """

    if method == "Fog Collector":
        factor = 0.5 + humidity / 200
    elif method == "Special Material":
        factor = humidity / 85
    else:
        raise ValueError("Unknown harvesting method")

    return round(BASE_WATER[method] * factor, 3)


def recommend_method(humidity, fog_detected, energy):
    methods = solve_csp(humidity, fog_detected, energy)

    if not methods:
        return {
            "recommended": None,
            "reason": "No feasible method or invalid sensor data.",
            "options": []
        }

    options = []

    for method in methods:
        water = estimate_water(method, humidity)
        energy_used = ENERGY_REQUIREMENTS[method]

        score = water - ENERGY_WEIGHT * energy_used

        options.append({
            "method": method,
            "water_liters": water,
            "energy_units": energy_used,
            "score": round(score, 3)
        })

    best = max(
        options,
        key=lambda option: option["score"]
    )

    return {
        "recommended": best["method"],
        "reason": (
            f"Highest experimental score: {best['score']}. "
            f"Estimated water: {best['water_liters']} L, "
            f"Energy: {best['energy_units']} units."
        ),
        "options": options
    }


def safe_recommend_method(humidity, fog_detected, energy):
    validation = validate_sensor_data(
        humidity, fog_detected, energy
    )

    if not validation["valid"]:
        return {
            "status": "SENSOR_WARNING",
            "recommended": None,
            "reason": "Sensor data requires operator review.",
            "warnings": validation["errors"],
            "options": []
        }

    result = recommend_method(
        humidity, fog_detected, energy
    )

    result["status"] = (
        "SUCCESS"
        if result["recommended"] is not None
        else "NO_FEASIBLE_METHOD"
    )
    result["warnings"] = []

    return result
