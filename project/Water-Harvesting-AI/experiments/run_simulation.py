
import csv
from pathlib import Path
from collections import Counter

from src.decision import safe_recommend_method


# Simulated test scenarios — not real sensor data.
SCENARIOS = [
    {
        "name": "High Humidity With Fog",
        "humidity": 85,
        "fog": True,
        "energy": 30
    },
    {
        "name": "Fog With Low Energy",
        "humidity": 40,
        "fog": True,
        "energy": 10
    },
    {
        "name": "Humid Without Fog",
        "humidity": 75,
        "fog": False,
        "energy": 40
    },
    {
        "name": "Dry Weather",
        "humidity": 30,
        "fog": False,
        "energy": 10
    },
    {
        "name": "No Energy Available",
        "humidity": 85,
        "fog": True,
        "energy": 0
    },
    {
        "name": "Invalid Humidity",
        "humidity": 120,
        "fog": True,
        "energy": 30
    },
    {
        "name": "Missing Humidity",
        "humidity": None,
        "fog": True,
        "energy": 30
    },
    {
        "name": "Invalid Fog Reading",
        "humidity": 85,
        "fog": "yes",
        "energy": 30
    }
]


def run_simulation():
    results = []

    for scenario in SCENARIOS:
        decision = safe_recommend_method(
            scenario["humidity"],
            scenario["fog"],
            scenario["energy"]
        )

        result = {
            "scenario": scenario["name"],
            "humidity": scenario["humidity"],
            "fog": scenario["fog"],
            "energy": scenario["energy"],
            "status": decision["status"],
            "recommended": decision["recommended"],
            "reason": decision["reason"],
            "warnings": "; ".join(decision["warnings"])
        }

        results.append(result)

    # Save experiment results
    output_path = Path("experiments/results.csv")
    output_path.parent.mkdir(
        parents=True, exist_ok=True
    )

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    # Summarize decisions
    counts = Counter(
        result["status"] for result in results
    )

    print("\n=== WATER HARVESTING AI SIMULATION ===")

    for result in results:
        print(
            f"{result['scenario']}: "
            f"{result['status']} -> "
            f"{result['recommended']}"
        )

    print("\n=== SUMMARY ===")
    print("Total scenarios:", len(results))
    print("Successful recommendations:",
          counts["SUCCESS"])
    print("Sensor warnings:",
          counts["SENSOR_WARNING"])
    print("No feasible method:",
          counts["NO_FEASIBLE_METHOD"])

    print("\nResults saved to:", output_path)

    return results


if __name__ == "__main__":
    run_simulation()
