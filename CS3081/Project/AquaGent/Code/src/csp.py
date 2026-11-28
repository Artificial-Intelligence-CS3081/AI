"""Backtracking CSP over two variables: METHOD and DURATION.
Hard constraints: safety, available time, energy and weather suitability.
"""
from .model import METHODS, DURATIONS, ENERGY_RATE_KWH


def failed_constraints(method, hours, data, fog_probability):
    reasons = []
    if not data.safety_ok:
        reasons.append('Safety inspection failed')
    if hours > data.max_hours:
        reasons.append('Exceeds allowed operating duration')
    if hours * ENERGY_RATE_KWH[method] > data.energy_budget_kwh + 1e-9:
        reasons.append('Insufficient energy budget')
    if method == 'Fog Collector':
        if fog_probability < data.min_fog_confidence:
            reasons.append('Fog probability below confidence threshold')
        if data.wind_m_s <= 0:
            reasons.append('No simulated wind for fog collection')
        if data.fog_lwc_g_m3 <= 0:
            reasons.append('No assumed liquid-water content in fog')
    else:
        # A universal 60% RH cutoff is not supported by the MOF-303
        # literature. Only zero atmospheric humidity is excluded in this
        # toy reference scenario; actual suitability needs a device isotherm.
        if data.humidity <= 0:
            reasons.append('Zero humidity: no atmospheric water vapor available')
    return reasons


def solve_csp(data, fog_probability):
    """Enumerate all valid (method, duration) assignments using backtracking."""
    solutions = []
    domains = {'method': METHODS, 'hours': DURATIONS}

    def backtrack(assignment):
        if len(assignment) == len(domains):
            if not failed_constraints(assignment['method'], assignment['hours'], data, fog_probability):
                solutions.append(assignment.copy())
            return
        variable = next(v for v in domains if v not in assignment)
        for value in domains[variable]:
            if variable == 'hours' and value > data.max_hours:
                continue
            assignment[variable] = value
            if variable == 'method' or not failed_constraints(assignment['method'], assignment['hours'], data, fog_probability):
                backtrack(assignment)
            del assignment[variable]

    backtrack({})
    return solutions
