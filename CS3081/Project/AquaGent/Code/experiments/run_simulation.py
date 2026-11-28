"""Reproducible test scenarios; writes CSV of synthetic outcomes."""
import csv
from pathlib import Path
from src.model import Inputs
from src.decision import evaluate

CASES = [
    ('Fog detected', dict(humidity=85,temperature_c=22,fog_observed=True,energy_budget_kwh=8)),
    ('Fog absent', dict(humidity=85,temperature_c=22,fog_observed=False,energy_budget_kwh=8)),
    ('Fog sensor missing', dict(humidity=85,temperature_c=22,fog_observed=None,energy_budget_kwh=8)),
    ('Low humidity', dict(humidity=30,temperature_c=30,fog_observed=False,energy_budget_kwh=8)),
    ('No energy', dict(humidity=85,temperature_c=22,fog_observed=True,energy_budget_kwh=0)),
    ('Unsafe', dict(humidity=85,temperature_c=22,fog_observed=True,energy_budget_kwh=8,safety_ok=False)),
    ('Missing humidity', dict(humidity=None,temperature_c=22,fog_observed=True,energy_budget_kwh=8)),
    ('Invalid humidity', dict(humidity=120,temperature_c=22,fog_observed=True,energy_budget_kwh=8)),
    ('Low sensitivity', dict(humidity=85,temperature_c=22,fog_observed=True,energy_budget_kwh=8,sensor_sensitivity=0.55)),
    ('Tight energy', dict(humidity=85,temperature_c=22,fog_observed=True,energy_budget_kwh=0.2)),
]


def run(output='experiments/results.csv'):
    rows = []
    for name, values in CASES:
        result = evaluate(Inputs(**values))
        plan = result['recommended'] or {}
        rows.append({'scenario':name,'status':result['status'], 'p_fog':result['fog_probability'],
                     'method':plan.get('method',''), 'hours':plan.get('hours',''),
                     'water_demo_l':plan.get('water_liters_demo',''),
                     'energy_demo_kwh':plan.get('energy_kwh_demo',''),
                     'score_demo':plan.get('score_demo',''),
                     'warnings':' | '.join(result['warnings'])})
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w',encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for r in rows:
        print(r['scenario'], '->', r['status'], r['method'] or '(none)')
    print(f'Wrote {len(rows)} simulated cases to {path}')
    return rows

if __name__ == '__main__':
    run()
