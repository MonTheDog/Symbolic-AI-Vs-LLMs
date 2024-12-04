# File per eseguire il flusso di esecuzione del problema dello Zaino
import utils
import algorithm_knapsack as ak
import symbolic_knapsack as sk

print("=================================================")
print("LLMs vs Symbolic AI - Knapsack Problem")
print("=================================================")
print()

knapsack_instance = utils.get_knapsack_instance() # Obtain the knapsack instance
solution, best_items = ak.get_knapsack_optimal_solution(knapsack_instance) # Calculate the best solution

print("Optimal Subset: ", best_items)
print("Optimal Value: ", solution)
print()

print("================== Symbolic AI ==================")
sk_value, sk_items = sk.run_ga(knapsack_instance)
print("Items taken: " + str(sk_items))
print("Total value: " + str(sk_value))
print()

# ...
