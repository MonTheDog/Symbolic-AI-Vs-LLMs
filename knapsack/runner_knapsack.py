import utils
import knapsack.algorithm_knapsack as ak
import knapsack.symbolic_knapsack as sk
from knapsack.llm_knapsack import KnapsackLLMAgent

def knapsack_runner(run_count):
    knapsack_instance = utils.get_knapsack_instance()  # Obtain the knapsack instance
    print("==================== Optimal Value ====================")
    solution, best_items = ak.get_knapsack_optimal_solution(knapsack_instance)  # Calculate the best solution
    #print("Optimal Subset: ", best_items)
    print("Optimal Value: ", solution)

    sk_values = []
    sk_elapsed_times = []
    sk_opt_distances = []

    llm_4o_values = []
    llm_4o_elapsed_times = []
    llm_4o_opt_distances = []
    llm_4o_total_invalid_solutions = 0

    llm_o1_values = []
    llm_o1_elapsed_times = []
    llm_o1_opt_distances = []
    llm_o1_total_invalid_solutions = 0

    for i in range(0, run_count):
        # Symbolic AI
        sk_value, sk_items, sk_elapsed_time = sk.run_ga(knapsack_instance)
        #print("Items taken: " + str(sk_items))
        #print("Total value: " + str(sk_value))
        sk_values.append(sk_value)
        sk_elapsed_times.append(sk_elapsed_time)
        sk_opt_distances.append(solution - sk_value)

        # LLM 4o
        llm_4o_knapsack_agent = KnapsackLLMAgent("4o")
        _, llm_4o_items, llm_4o_reasoning, llm_4o_value, llm_4o_invalid_solutions, llm_4o_elapsed_time = (llm_4o_knapsack_agent.
                                                                                       action_loop(knapsack_instance))
        llm_4o_knapsack_agent.reset_conversation()
        #print("Items taken: " + str(llm_4o_items))
        #print("Reasoning: " + llm_4o_reasoning)
        #print("Total value: " + str(llm_4o_value))
        #print("Invalid solutions (max 3): " + str(llm_4o_invalid_solutions))
        llm_4o_values.append(llm_4o_value)
        llm_4o_elapsed_times.append(llm_4o_elapsed_time)
        llm_4o_opt_distances.append(solution - llm_4o_value)
        llm_4o_total_invalid_solutions += llm_4o_invalid_solutions

        # LLM o1
        llm_o1_knapsack_agent = KnapsackLLMAgent("o1")
        _, llm_o1_items, llm_o1_reasoning, llm_o1_value, llm_o1_invalid_solutions, llm_o1_elapsed_time = (
            llm_o1_knapsack_agent.
            action_loop(knapsack_instance))
        llm_o1_knapsack_agent.reset_conversation()
        # print("Items taken: " + str(llm_o1_items))
        # print("Reasoning: " + llm_o1_reasoning)
        # print("Total value: " + str(llm_o1_value))
        # print("Invalid solutions (max 3): " + str(llm_o1_invalid_solutions))
        llm_o1_values.append(llm_o1_value)
        llm_o1_elapsed_times.append(llm_o1_elapsed_time)
        llm_o1_opt_distances.append(solution - llm_o1_value)
        llm_o1_total_invalid_solutions += llm_o1_invalid_solutions

    # We compute the average values and print them
    sk_average_value = sum(sk_values) / len(sk_values)
    sk_average_elapsed_time = sum(sk_elapsed_times) / len(sk_elapsed_times)
    sk_average_opt_distance = sum(sk_opt_distances) / len(sk_opt_distances)

    llm_4o_average_value = sum(llm_4o_values) / len(llm_4o_values)
    llm_4o_average_elapsed_time = sum(llm_4o_elapsed_times) / len(llm_4o_elapsed_times)
    llm_4o_average_opt_distance = sum(llm_4o_opt_distances) / len(llm_4o_opt_distances)

    llm_o1_average_value = sum(llm_o1_values) / len(llm_o1_values)
    llm_o1_average_elapsed_time = sum(llm_o1_elapsed_times) / len(llm_o1_elapsed_times)
    llm_o1_average_opt_distance = sum(llm_o1_opt_distances) / len(llm_o1_opt_distances)

    print("==================== Symbolic AI ====================")
    print("Average Value: ", sk_average_value)
    print("Average Elapsed Time: " + str("%.4f" % sk_average_elapsed_time) + "ms")
    print("Average Distance from Optimal Solution: ", sk_average_opt_distance)
    print("========================= 4o =========================")
    print("Average Value: ", llm_4o_average_value)
    print("Average Elapsed Time: " + str("%.4f" % llm_4o_average_elapsed_time) + "ms")
    print("Average Distance from Optimal Solution: ", llm_4o_average_opt_distance)
    print("Total Invalid Solutions: ", llm_4o_total_invalid_solutions)
    print("========================= o1 =========================")
    print("Average Value: ", llm_o1_average_value)
    print("Average Elapsed Time: " + str("%.4f" % llm_o1_average_elapsed_time) + "ms")
    print("Average Distance from Optimal Solution: ", llm_o1_average_opt_distance)
    print("Total Invalid Solutions: ", llm_o1_total_invalid_solutions)

    # utils.plot_values(sk_values, llm_4o_values, "4o")
    # utils.plot_values(sk_values, llm_o1_values, "o1")


if __name__ == '__main__':
    print("=================================================")
    print("LLMs vs Symbolic AI - Knapsack Problem")
    print("=================================================")
    print()

    knapsack_runner(2)
