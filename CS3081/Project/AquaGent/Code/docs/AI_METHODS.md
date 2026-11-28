# Architecture overview

Inputs (humidity, temperature, fog sensor, wind, energy budget, duration, safety)

-> sensor validation -> **Bayesian posterior** P(Fog | sensor evidence)

-> **CSP backtracking** variables Method ∈ {Fog, MOF}, Hours ∈ {1,2,4,8}

-> reject assignments breaking hard constraints (fog posterior threshold, humidity, energy, time, safety)

-> score feasible candidates (illustrative water − 0.8 × illustrative energy)

-> ranked recommendation -> operator approves/rejects (simulation only)

## Why the methods are separate
Bayes quantifies uncertainty and CSP checks feasibility. The CSP consumes the posterior via a **risk threshold**; a probability is never treated as certain observation. The agent intentionally abstains when no safe feasible option exists. Sensor validation is not the same as probabilistic uncertainty handling.

## Experimental design
Compare baseline: direct Boolean fog sensor vs Bayesian posterior threshold across synthetic sensor scenarios. Report abstention rate, infeasible-case detection and recommendation stability under altered sensitivity, specificity and prior. Do not describe simulated values as field accuracy.
