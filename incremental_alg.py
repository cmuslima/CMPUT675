import incremental_alg_basics
import random
import numpy as np
import math
from CPLEX import CPLEX
import pickle
random.seed(0)
multiD = True
class incremental_alg(): 
    def __init__(self, args):        
        self.num_knapsack = None #This says how many items will go into the knapsack
        self.upper_bound_value = 5000 #This is the upper bound for the value of an item
        self.lower_bound_value = 0 #This is the lower bound for the value of an item
        self.scores = []
        self.all_errors = []
        
    

    def reset(self, args):
        if args.infinitesimal:
            self.epilson = .1
            self.decay  = .999
        else:
            self.epilson = .99
            self.decay  = 1
        self.num_knapsack = None
        self.weights = []
        self.values = []
        self.max_vd = None
        self.min_vd = None
        self.value_densities = []
        self.indicators = []
        self.current_capacity = None
       
        self.num_error = 0

    def main_loop(self, args):
        decision_times = []
        print('knapasck', self.num_knapsack)
        self.weights, self.values, self.value_densities, self.max_vd, self.min_vd = incremental_alg_basics.simulate_data(self.epilson, self.num_knapsack, self.upper_bound_value, self.lower_bound_value, self.decay,1)
        
        self.c = 1/(1+np.log(self.max_vd/self.min_vd))
        print(f'c = {self.c}')
        print(f'max vd = {self.max_vd} min vd = {self.min_vd}')
        for i in range(0, self.num_knapsack):
            value_density = self.value_densities[i]
            value = self.values[i]
            weight = self.weights[i]
            #print(f'value = {value}, weight = {weight}')
            self.current_capacity = incremental_alg_basics.calculate_capacity_filled_so_far(self.weights,self.indicators)
            if i == 0:
                assert self.current_capacity == 0
            
            decision = incremental_alg_basics.knapack_decision(value, weight, self.max_vd, self.min_vd, self.current_capacity, self.c)
            self.indicators.append(decision)

            capacity_after_decision = incremental_alg_basics.calculate_capacity_filled_so_far(self.weights,self.indicators)

            if capacity_after_decision > 1 and decision:
                self.num_error+=1

            
            decision_times.append(capacity_after_decision)

        
        score = incremental_alg_basics.determine_overall_score(self.indicators, self.values)
        return score, self.num_error,  self.weights, self.values, decision_times

    def main_loop_multi_dimensional(self, args):
        decision_times = []

        self.weights, self.values, self.value_densities, self.max_vd, self.min_vd = incremental_alg_basics.simulate_data(self.epilson, self.num_knapsack, self.upper_bound_value, self.lower_bound_value, self.decay, 2)
        print(f'weights {self.weights} values {self.values}, VD {self.value_densities}')
        print(np.shape(self.weights))
        self.c = 1/(1+np.log(self.max_vd/self.min_vd))
        #print(f'c = {self.c}')
        #print(f'max vd = {self.max_vd} min vd = {self.min_vd}')
        for i in range(0, self.num_knapsack):
            value_density = self.value_densities[i]
            print(f'value density {value_density}')
            value = self.values[i]
            print(f'value  {value}')
            if multiD:
                weight = self.weights[:,i] #this gets the entire column
                print(f'weight {weight}')

            #print(f'value = {value}, weight = {weight}')
            else:
                weight = self.weights[i]
            self.current_capacity = incremental_alg_basics.calculate_capacity_filled_so_far(self.weights,self.indicators)
 
            
            decision = incremental_alg_basics.knapack_decision(value, weight, self.max_vd, self.min_vd, self.current_capacity, self.c)
            #print('decision', decision)
            self.indicators.append(decision)

            capacity_after_decision = incremental_alg_basics.calculate_capacity_filled_so_far(self.weights,self.indicators)
            #print('capacity after decision', capacity_after_decision)
        

            
            decision_times.append(capacity_after_decision)

        
        score = incremental_alg_basics.determine_overall_score(self.indicators, self.values)
        return score, self.num_error,  self.weights, self.values, decision_times

    def run(self,args):
    
        ub_lists = [2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7, 2**8]
        decision_history = dict()
        for ub in ub_lists:
            empirical_ratio = []
      
            for i in range(1, args.num_runs):
              
                self.reset(args)
                self.num_knapsack =2**(i)
                self.upper_bound_value = ub
                # #print('lower bound', self.lower_bound_value, 'upper bound', self.upper_bound_value)
                score, error, weights, values, decision_times = self.main_loop_multi_dimensional(args)
                # print('score', score, 'decisoin time', decision_times)
                key = f'{self.num_knapsack}_{ub}'
                decision_history[key] = decision_times
            
                optimal_score = CPLEX(weights, values, args.dimension)
                
                print(f'score from threshold algorithm = {score}, optimal score = {optimal_score}')
                self.scores.append(score)
                empirical_ratio.append(optimal_score/score)
                print('decision_times', decision_times)
            print('empirical_ratio', empirical_ratio)
            model_name = f'comparing_num_items_{self.upper_bound_value}_{self.lower_bound_value}_{self.epilson}_{self.decay}_multi_non0'
            with open(model_name, 'wb') as output:
                pickle.dump(empirical_ratio, output)


        # print('all scores', self.scores)
        model_name = f'infinitesimal_decision_history_multi_non0'
        with open(model_name, 'wb') as output:
            pickle.dump(decision_history, output)

        print('empirical_ratio', empirical_ratio)
        #print(decision_history)





            

#In the non infnitesimal setting, the algorithm can make a mistake and choose an item
#that yeilds the weight to exceed the max weight of 1 (at least using the function in the paper)