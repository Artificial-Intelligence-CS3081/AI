
import math


def validate_sensor_data(humidity, fog_detected, energy):
    """
    Check sensor readings before AI decision-making.
    """

    errors = []

    # Humidity validation
    if humidity is None:
        errors.append("Missing humidity reading")
    elif (
        isinstance(humidity, bool)
        or not isinstance(humidity, (int, float))
        or not math.isfinite(humidity)
        or not 0 <= humidity <= 100
    ):
        errors.append("Invalid humidity reading")

    # Fog sensor validation
    if fog_detected is None:
        errors.append("Missing fog sensor reading")
    elif type(fog_detected) is not bool:
        errors.append("Invalid fog sensor reading")

    # Energy validation
    if energy is None:
        errors.append("Missing energy reading")
    elif (
        isinstance(energy, bool)
        or not isinstance(energy, (int, float))
        or not math.isfinite(energy)
        or energy < 0
    ):
        errors.append("Invalid energy reading")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
