import random

def allocate_weights(input_list):
    # Calculate number of elements
    n = len(input_list)
    
    # Generate random weights that sum to 10 (since we want 0.1 precision)
    weights = []
    remaining = 10
    for i in range(n-1):
        # Ensure minimum weight of 1 (0.1) and leave enough for remaining elements
        max_weight = remaining - (n-i-1)
        weight = random.randint(1, max_weight)
        weights.append(weight)
        remaining -= weight
    
    # Add final weight
    weights.append(remaining)
    
    # Convert to decimals that sum to 1
    weights = [w/10 for w in weights]
    
    # Shuffle the weights
    random.shuffle(weights)
    
    return weights
