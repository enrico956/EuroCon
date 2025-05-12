def social_welfare_function(utilities, alpha):
    """
    Calculate the social welfare function (SWF) for a given set of utilities and a parameter alpha.
    
    :param utilities: List of utilities for each individual.
    :param alpha: The degree of inequality aversion.
    :return: The calculated social welfare.

    alpha is the degree of inequality aversion. 
    For alpha = 0, the SWF is the sum of utilities (max-mean or Utilitarian).
    For alpha = 1, the SWF is the geometric mean of utilities (max-product or Bernoulli-Nash).
    For alpha = inf, the SWF is the max-min utility (Rawlsian).
    """
    n = len(utilities)

    if alpha > 100:
        return min(utilities)
    
    if alpha >= 0 and alpha != 1:
        # Compute the SWF for alpha >= 0 and alpha != 1
        welfare = (sum(u**(1 - alpha) for u in utilities) / n)**(1 / (1 - alpha))
    elif alpha == 1:
        # Compute the SWF for alpha = 1
        welfare = 1
        for u in utilities:
            welfare *= u
        welfare = welfare**(1 / n)
    else:
        raise ValueError("Alpha must be >= 0.")
    
    return welfare

# # Example usage:
# utilities = [1, 2, 3, 4, 5]
# alpha = 0.5
# welfare = social_welfare_function(utilities, alpha)
# print(f"Social Welfare for alpha = {alpha}: {welfare}")

# alpha = 1
# welfare = social_welfare_function(utilities, alpha)
# print(f"Social Welfare for alpha = {alpha}: {welfare}")
