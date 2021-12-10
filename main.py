import sys
import argparse
from incremental_alg import incremental_alg
parser = argparse.ArgumentParser()

#Put the env name as the roordir

parser.add_argument('--num_knapsack', type=int, default= 3)
parser.add_argument('--num_runs', type=int, default= 9)
parser.add_argument('--dimension', type=int, default= 2)

parser.add_argument('--infinitesimal', type=bool, default= False)



args = parser.parse_args()

incremental_algorithm = incremental_alg(args)
incremental_algorithm.run(args)

#https://www.geeksforgeeks.org/implementation-of-0-1-knapsack-using-branch-and-bound/