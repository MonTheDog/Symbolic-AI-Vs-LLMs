import utils
from timeit import default_timer as timer

def knapsack_algorithm(maximum_weight, items_weights, items_values, num_items):
    """
    Solve the knapsack problem using dynamic programming.
    :param maximum_weight: the maximum weight of the knapsack
    :param items_weights: the list of weights of the items
    :param items_values: the list of values of the items
    :param num_items: the number of items
    :return: The optimal value of the knapsack and the dynamic programming table
    """
    # We initialize the empty table
    table = []
    for i in range(num_items + 1):
        table.append([0] * (maximum_weight + 1))

    # We execute the knapsack algorithm
    # We skip the first column and the first row as intended by the algorithm
    for i in range(1, num_items + 1):
        for w in range(1, maximum_weight + 1):
            if items_weights[i - 1] <= w:
                table[i][w] = max(items_values[i - 1] + table[i - 1][w - items_weights[i - 1]], table[i - 1][w])
            else:
                table[i][w] = table[i - 1][w]

    # We return both the optimal value and the table
    return table[num_items][maximum_weight], table


def construct_optimal_set(table, items_weights, i, j, optimal_set):
    """
    Recursively reconstructs the optimal subsets given the knapsack solution table.
    :param table: The filled dynamic programming table
    :param items_weights: The weights of the items
    :param i: Index of the item under consideration
    :param j: Current possible maximum weight
    :param optimal_set: The optimal subset so far. This will be modified during the execution
    """

    # For the current item i at a maximum weight j to be part of an optimal subset,
    # the optimal value at (i, j) must be greater than the optimal value at (i-1, j).
    # where i - 1 means considering only the previous items at the given maximum weight
    if i > 0 and j > 0:
        if table[i - 1][j] == table[i][j]:
            construct_optimal_set(table, items_weights, i - 1, j, optimal_set)
        else:
            optimal_set.add(i)
            construct_optimal_set(table, items_weights, i - 1, j - items_weights[i - 1], optimal_set)


def knapsack_with_best_subset(knapsack_weight, items_weights, items_value):
    """
    Solves the knapsack problem and returns the optimal subset of the knapsack.
    :param knapsack_weight: The weight of the knapsack
    :param items_weights: The weights of the items
    :param items_value: The values of the items
    :return: The optimal value of the knapsack and the subset of items of the optimal solution
    """
    start = timer()
    num_items = len(items_weights)

    # Solve the knapsack problem
    optimal_val, dp_table = knapsack_algorithm(knapsack_weight, items_weights, items_value, num_items)

    # Get the optimal set
    optimal_items = set()
    construct_optimal_set(dp_table, items_weights, num_items, knapsack_weight, optimal_items)
    end = timer()

    # Prints the time elapsed to run the algorithm
    utils.print_elapsed_time(start, end)

    return optimal_val, optimal_items


def get_knapsack_optimal_solution(instance):
    """
    Solves the knapsack problem from an instance
    :param instance: The knapsack instance
    :return: The optimal value of the knapsack and the subset of items of the optimal solution
    """

    # Change the instance format to run the algorithms
    items = instance["items"]
    items_values = []
    items_weights = []

    for item in items:
        items_values.append(item["Value"])
        items_weights.append(item["Weight"])

    knapsack_capacity = instance["capacity"]

    # Solve the problem
    optimal_solution, optimal_subset = knapsack_with_best_subset(knapsack_capacity, items_weights, items_values)

    # Create the best subset of items with names
    best_subset = []
    for i in optimal_subset:
        best_subset.append(items[i-1])

    return optimal_solution, best_subset

# TODO: Remove and paste in runner_knapsack
if __name__ == "__main__":

    solution, best_items = get_knapsack_optimal_solution(utils.get_knapsack_instance())

    print("Optimal Value: ", solution)
    print("Optimal Subset: ", best_items)