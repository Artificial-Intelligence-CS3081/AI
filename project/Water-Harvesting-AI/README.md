# Water Harvesting AI — Learning Scaffold

CS3081 student project: decision-support agent comparing **fog collection** with a **sorbent-based atmospheric water harvesting method**.

> **Status:** Step 1 only: simulated input validation. This project **does not yet contain a functioning AI agent, logic knowledge base, CSP solver, or physically validated yield/energy model**.

## Run (Python 3.10+)

```bash
python main.py
python -m unittest discover -s tests -v
```

No external libraries required yet.

## Intended inputs

- `temperature_c`: numeric temperature in degrees Celsius
- `humidity_pct`: numeric relative humidity (0–100)
- `fog_detected`: Boolean flag, `True` or `False`
- `energy_units`: nonnegative *placeholder* budget. Define physical energy units and real equipment properties before scientific comparison.

## Milestones (student-authored development)

- [x] Folder structure, basic input validation, tests
- [ ] Design and implement rule-based knowledge base
- [ ] Formulate CSP variables, domains, and constraints; implement solver
- [ ] Define grounded equipment assumptions and yield/energy models with references
- [ ] Handle contradictory/noisy sensor measurements
- [ ] Compare alternatives, explain recommendations, and evaluate performance
- [ ] Build optional interactive UI, report, portfolio, poster, and slides

## Academic integrity

This scaffold is for guided learning. Students must author and document their own project work and follow their instructor's stated limit on AI-generated submitted content (25%).
