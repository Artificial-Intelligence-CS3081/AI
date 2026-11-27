
def evaluate_rules(humidity, fog_detected, energy):
    """
    Evaluate preliminary water harvesting rules.
    Thresholds are illustrative, not scientific.
    """

    if humidity is None or fog_detected is None or energy is None:
        return "Sensor Warning"

    if fog_detected:
        return "Fog Collector"

    if humidity >= 60 and energy >= 20:
        return "Special Material"

    return "No Suitable Method"
