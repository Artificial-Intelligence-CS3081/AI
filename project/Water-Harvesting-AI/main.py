"""Step 1 demo: input validation, NOT yet an AI recommendation agent."""
from src.validation import validate_inputs

# Simulated inputs; not a real sensor feed.
reading = {
    "temperature_c": 28,
    "humidity_pct": 78,
    "fog_detected": True,
    "energy_units": 30,  # Arbitrary demo units; define physical units later.
}

if __name__ == "__main__":
    issues = validate_inputs(reading)
    if issues:
        print("WARNING: Input problems detected:")
        for issue in issues:
            print("-", issue)
    else:
        print("Input validation passed. Next: implement rules and CSP.")
