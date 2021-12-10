import random
import math
import numpy as np
debug = False
multiD = True
def generate_random_weights(num_knapsack,epilson, decay):
    weights = []
    for i in range(0, num_knapsack):
        weights.append(random.uniform(0, epilson))
        epilson*=decay
    return weights
def generate_random_values(num_knapsack, upper_bound_value, lower_bound_value):
    values = []

    for i in range(0, num_knapsack):
        values.append(random.uniform(lower_bound_value, upper_bound_value))
    
    return values

def simulate_data(epilson, num_knapsack, upper_bound_value,lower_bound_value, decay, dimension):
    weights = generate_random_weights(num_knapsack, epilson, decay)
    if multiD:
        weights2 = generate_random_weights(num_knapsack, epilson, decay)
        weights = [weights, weights2]
        weights = np.array(weights)
        weights.reshape((dimension, num_knapsack))

    values =generate_random_values(num_knapsack, upper_bound_value, lower_bound_value)
    value_densities, max_vd, min_vd = generate_value_denisty(weights, values)

    if debug:
        print(f'weights {weights}')
        print(f'values {values}')
        print(f'value_densities {value_densities}')
        print(f'max_vd {max_vd}')
        print(f'min_vd {min_vd}')
    return weights, values, value_densities, max_vd, min_vd
def calculate_value_density(weights, values):
    value_densities = []
    for weight, value in zip(weights, values):
        if debug:
            print(f'weight = {weight}, value = {value}, VD = {value/weight}')
        value_densities.append(value/weight)
    return value_densities
def generate_value_denisty(weights, values):
   
    if multiD:
        weights = sum_weight_per_item(weights)
        print('summed weights', weights)
    
    value_densities = calculate_value_density(weights, values)

    max_vd = max(value_densities)
    min_vd = min(value_densities)
    return value_densities, max_vd, min_vd

def sum_weight_per_item(weights):
    weights = weights.sum(axis=0)
    return weights
def sum_weight_across_items(weights):
    weights = weights.sum(axis=1)
    return weights

def calculate_capacity_filled_so_far(weights, indicators):
    
    if len(indicators) == 0 and multiD:
        print('This is the step 0. The knapsack is empty')
        return [0]*len(weights)
    if len(indicators) == 0 and multiD == False:
        return 0 
    if multiD:
        
        num_items = len(indicators)
        num_weights = np.shape(weights)[0]
        capacity = [0]*num_weights

        for r in range(0, num_weights):
            for c in range(0, num_items):
                capacity[r]+=weights[r][c]*(indicators[c])
        
    else:
        capacity = 0
        for i in range(0, len(indicators)):
            capacity+=(weights[i]*indicators[i])
    #if debug:
    
    return capacity #capacity is a list in the multiD case
        
#function from Online Knapsack Problems paper (Chakrabarty, Zhou, Lukose 2008)
def get_pt(max_vd, min_vd, capacity):  
    pt = (max_vd*math.exp(1))/(min_vd)
    if multiD:
      
        pt = pt**sum(capacity)
    else:
        pt = pt**capacity
    pt = pt*(min_vd/math.exp(1))

    if debug:
        print(f'pt = {pt}')
    return pt

def determine_overall_score(indicators, values):
    score_array = np.multiply(indicators, values)
    score = np.sum(score_array)
    return score
    
def knapack_decision(value, weight, max_vd, min_vd, capacity, c): #have to edit this
    pt =get_pt(max_vd, min_vd, capacity)
    print('ppint', pt)
    try:
        value_density = value/sum(weight)
    except:
        value_density = value/weight
    #print(f'value {value}, weight {weight} value den {value_density} pt {pt} capacity {capacity}')
    # if capacity <= c and capacity >=  0:
        
    #     assert pt <= min_vd
    print('value_density', value_density)
    if value_density >= pt:
        if multiD:
            if np.add(weight, capacity)[0] <=1 and np.add(weight, capacity)[1] <=1:
                x_t = 1
            else:
                x_t = 0
        else:
            if (weight+capacity)<= 1:
                x_t = 1
            else:
                x_t = 0
    else:
        x_t = 0
    #if debug:
    #print(f'decision = {x_t}')
    return x_t
