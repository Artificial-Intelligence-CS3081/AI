"""Uncertainty -> CSP -> scoring -> operator decision (UI)."""
from .model import Inputs, validate, ENERGY_RATE_KWH, METHODS, predicted_water_liters
from .uncertainty import fog_posterior
from .csp import solve_csp, failed_constraints


def evaluate(data: Inputs):
    issues = validate(data)
    if issues:
        return {'status':'SENSOR_WARNING','warnings':issues,'fog_probability':None,
                'recommended':None,'candidates':[],'excluded':{},'explanation':'Invalid or missing required inputs.'}

    p_fog = fog_posterior(data.fog_observed, data.prior_fog,
                          data.sensor_sensitivity, data.sensor_specificity)
    warnings = []
    if data.fog_observed is None:
        warnings.append('Fog sensor missing: using prior probability; no false certainty assumed.')

    assignments = solve_csp(data, p_fog)
    candidates = []
    for candidate in assignments:
        method, hours = candidate['method'], candidate['hours']
        water = predicted_water_liters(method, data, hours, p_fog)
        energy = round(hours * ENERGY_RATE_KWH[method], 3)
        # Heuristic: maximize modeled collection while softly discounting
        # use of the *available* demo energy budget. The ratio is dimensionless.
        # Not a financial/thermodynamic efficiency measure.
        score = round(water / (1 + energy / data.energy_budget_kwh), 6)
        candidates.append({'method': method, 'hours': hours,
                           'water_liters_demo': water, 'energy_kwh_demo': energy, 'score_demo': score})

    # Explain excluded methods using their lowest-duration assignment.
    excluded = {}
    for method in METHODS:
        if not any(c['method'] == method for c in candidates):
            excluded[method] = failed_constraints(method, 1, data, p_fog)

    if not candidates:
        return {'status':'NO_FEASIBLE_METHOD','warnings':warnings,'fog_probability':round(p_fog,4),
                'recommended':None,'candidates':[],'excluded':excluded,
                'explanation':'No plan passes the safety, energy, time and weather constraints.'}

    # Deterministic tie breaking, choose lower energy first.
    candidates.sort(key=lambda x: (-x['score_demo'], x['energy_kwh_demo'], x['method'], x['hours']))
    top = candidates[0]
    return {'status':'SUCCESS','warnings':warnings,'fog_probability':round(p_fog,4),
            'recommended':top,'candidates':candidates,'excluded':excluded,
            'explanation':f"The highest demo score is {top['score_demo']} for {top['method']} over {top['hours']} h. "
                          'The CSP filters infeasible plans; a demo water/relative-energy heuristic ranks the rest.'}
