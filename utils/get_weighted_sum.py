def get_weighted_sum(weights, values):
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    return sum(w * v for w, v in zip(weights, values))
