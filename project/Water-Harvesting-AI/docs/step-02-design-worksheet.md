# Step 2 — Knowledge Base + CSP Design Worksheet

Complete this *before* implementing the agent.

1. **Specify the sorbent:** name/material and sources describing operating conditions.
2. **Define outputs:** estimated water (L/day), energy (Wh/day), constraints and safety warnings.
3. **Rules (your own):** write 3–5 IF/THEN rules and explain their evidence.
4. **CSP variables:** for example `method ∈ {fog, sorbent, none}` and `operating_period ∈ {morning, evening}` if scheduling is part of your scenario.
5. **Domains and constraints:** which combinations are allowed? Which measurements are missing or unreliable?
6. **Optimization:** define ranking of *feasible* options separately from the CSP feasibility test.
7. **Cases:** normal weather, low energy, missing humidity, inconsistent sensor values, no feasible method.

Do **not** treat arbitrary thresholds or illustrative energy units as scientifically verified values.
