"""One-step Bayesian inference with an explicit prior and binary sensor likelihoods.
The probabilities are configurable ASSUMPTIONS, not measured sensor properties.
"""

def fog_posterior(observation: bool | None, prior: float, sensitivity: float, specificity: float):
    if observation is None:
        return prior
    if observation is True:
        numerator = sensitivity * prior
        denominator = numerator + (1 - specificity) * (1 - prior)
    elif observation is False:
        numerator = (1 - sensitivity) * prior
        denominator = numerator + specificity * (1 - prior)
    else:
        raise ValueError('Observation must be True, False or None')
    return numerator / denominator
