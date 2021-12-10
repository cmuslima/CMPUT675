
from docplex.mp.model import Model
import numpy as np

def CPLEX(weight_matrix, value_matrix, dimension): 
    
    C = 1
    knapsack_model = Model('knapsack')
    
    if dimension == 1:
        N = len(weight_matrix)
        x = knapsack_model.binary_var_list(N, name="x")
        knapsack_model.add_constraint(sum(weight_matrix[i]*x[i] for i in range(N)) <= C)
        
    else:
        N = np.shape(weight_matrix)[1]
     
        x = knapsack_model.binary_var_list(N, name="x")
        for num in range(dimension): 
            knapsack_model.add_constraint(sum(weight_matrix[num][i]*x[i] for i in range(N)) <= C)
       


    obj_fn = sum(value_matrix[i]*x[i] for i in range(N))
    knapsack_model.set_objective("max", obj_fn)
    #knapsack_model.print_information()
    knapsack_model.float_precision
    sol = knapsack_model.solve()


    sol = str(sol)

    print(sol)
    try:
        sol = sol[34:41]
        sol = float(sol)
        print("SOL", sol)
    except:
        try:
            sol = sol[0:6]
            sol = float(sol)
            print("SOL", sol)
        except:
            sol = sol[0:4]
            sol = float(sol)
            print("SOL", sol)
       
    if sol is None:
        print("Infeasible")
        return None
    return sol