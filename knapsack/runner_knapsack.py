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

sk_values = []
sk_elapsed_times = []
sk_opt_distances = []
llm_values = []
llm_elapsed_times = []
llm_opt_distances = []
for i in range(0, 100):
    # Symbolic AI
    sk_value, sk_items, elapsed_time = sk.run_ga(knapsack_instance)
    print("Items taken: " + str(sk_items))
    print("Total value: " + str(sk_value))
    sk_values.append(sk_value)
    sk_elapsed_times.append(elapsed_time)
    sk_opt_distances.append(solution - sk_value)
    print()

    # LLM
    # ...

sk_average_value = sum(sk_values) / len(sk_values)
sk_average_elapsed_time = sum(sk_elapsed_times) / len(sk_elapsed_times)
sk_average_opt_distance = sum(sk_opt_distances) / len(sk_opt_distances)
# llm_average_value = sum(llm_values) / len(llm_values)
# llm_average_elapsed_time = sum(llm_elapsed_times) / len(llm_elapsed_times)
# llm_average_opt_distance = sum(llm_opt_distances) / len(llm_opt_distances)

print("==================== Symbolic AI ====================")
print("Average Value: ", sk_average_value)
print("Average Elapsed Time: " + str("%.4f" % sk_average_elapsed_time) + "ms")
print("Average Distance from Optimal Solution: ", sk_average_opt_distance)
# print("======================== LLM ========================")
# print("Average Value: ", llm_average_value)
# print("Average Elapsed Time: ", llm_average_elapsed_time)
# print("Average Distance from Optimal Solution: ", llm_average_opt_distance)
