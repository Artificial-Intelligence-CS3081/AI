"""Step 1: Validate simulated weather and equipment inputs.

Learning scaffold. Complete the AI rules and CSP yourself in later stages.
"""


def validate_inputs(reading: dict) -> list[str]:
    """Return human-readable issues. Empty list means basic checks passed."""
    errors = []
    required = ["temperature_c", "humidity_pct", "fog_detected", "energy_units"]
    for key in required:
        if key not in reading or reading[key] is None:
            errors.append(f"Missing input: {key}")
    if errors:
        return errors

    humidity = reading["humidity_pct"]
    temperature = reading["temperature_c"]
    energy = reading["energy_units"]
    fog = reading["fog_detected"]

    if isinstance(humidity, bool) or not isinstance(humidity, (int, float)) or not 0 <= humidity <= 100:
        errors.append("humidity_pct must be a number between 0 and 100")
    if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
        errors.append("temperature_c must be a number")
    if isinstance(energy, bool) or not isinstance(energy, (int, float)) or energy < 0:
        errors.append("energy_units must be a non-negative number")
    if not isinstance(fog, bool):
        errors.append("fog_detected must be True or False")
    return errors
