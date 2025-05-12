import random
import itertools
import statistics

def max_variance_parties(dict_list, k, seed = None):
    """
    Select k dictionaries from dict_list such that their values have maximum variance.
    If multiple combinations have the same maximum variance, randomly return one of them.
    """
    if seed is not None:
        random.seed(seed)

    if k > len(dict_list):
        raise ValueError("k cannot be greater than length of dict_list")

    # Enumerate all possible combinations of k dicts
    max_variance = -1
    best_combinations = []

    for combination in itertools.combinations(dict_list, k):
        values = [stance['choice'] for stance in combination]
        var = statistics.variance(values)
        if var > max_variance:
            max_variance = var
    
    for combination in itertools.combinations(dict_list, k):
        values = [stance['choice'] for stance in combination]
        var = statistics.variance(values)
        if var == max_variance:
            best_combinations.append(combination)

    # Randomly return one combination
    return list(random.choice(best_combinations))

