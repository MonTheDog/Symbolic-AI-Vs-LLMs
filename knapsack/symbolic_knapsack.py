import utils
import random
import operator
from timeit import default_timer as timer


def inizialize_population(population_size, number_of_items, weights, values, capacity):
    """
        Initializes the population of the genetic algorithm.
        :param population_size: The size of the population
        :param number_of_items: The number of items to be considered
        :return: The population of the genetic algorithm
    """

    population = []

    # Each individual is a list of 0s and 1s, where 0 means that the item is not taken and 1 means that it is
    for i in range(population_size):
        individual = generate_valid_individual(number_of_items, weights, values, capacity)
        population.append(individual)

    return population


def calculate_fitness(individual, weights, values, capacity):
    """
        Calculates the fitness of each individual in the population.
        :param population: The population of the genetic algorithm
        :param weights: The weights of the items
        :param values: The values of the items
        :param capacity: The capacity of the knapsack
        :return: The fitness of the individual
    """

    total_weight = 0
    total_value = 0

    for i in range(len(individual)):
        if individual[i] == 1: # Only consider the items that are taken
            total_weight += weights[i]
            total_value += values[i]

    # If the total weight exceeds the capacity, the fitness is set to -1 (the individual is not valid)
    if total_weight > capacity:
        return -1

    return total_value


def selection(population, weights, values, capacity):
    """
        Selects the best individuals in the population.
        :param population: The population of the genetic algorithm
        :param weights: The weights of the items
        :param values: The values of the items
        :param capacity: The capacity of the knapsack
        :return: The best individuals in the population
    """

    best_individuals = []

    for individual in population:
        fitness = calculate_fitness(individual, weights, values, capacity)
        # Include only valid individuals in the selection
        if fitness != -1:
            best_individuals.append((fitness, individual))
        else:
            new_individual = generate_valid_individual(len(weights), weights, values, capacity)
            best_individuals.append((calculate_fitness(new_individual, weights, values, capacity), new_individual))

    best_individuals.sort(key=operator.itemgetter(0), reverse=True) # Sort the individuals by fitness
    best_individuals = best_individuals[:len(best_individuals) // 2] # Select the best half of the population
    best_individuals = [x[1] for x in best_individuals] # Get only the individuals, without the fitness

    return best_individuals


def crossover(parent1, parent2, weights, values, capacity):
    """
        Performs the crossover operation between two parents.
        :param parent1: The first parent
        :param parent2: The second parent
        :return: The offspring of the two parents
    """

    crossover_point = random.randint(1, len(parent1) - 1) # Randomly select the crossover point
    offspring = parent1[:crossover_point] + parent2[crossover_point:] # Create the offspring by combining the parents

    if calculate_fitness(offspring, weights, values, capacity) == -1:
        offspring = generate_valid_individual(len(weights), weights, values, capacity)

    return offspring


def mutation(individual):
    """
        Performs the mutation operation on an individual.
        :param individual: The individual to mutate
        :return: The mutated individual
    """

    for i in range(len(individual)): # Iterate over all the genes of the individual
        random_number = random.uniform(0, 1)
        if random_number > 0.2: # Randomly decide whether to mutate the gene or not (20% probability)
            # Flip the gene (0 -> 1, 1 -> 0)
            if individual[i] == 1:
                individual[i] = 0
            else:
                individual[i] = 1

    return individual


def generate_valid_individual(number_of_items, weights, values, capacity):
    """
    Generates a valid individual to replace invalid ones.
    :param number_of_items: The number of items to consider
    :param weights: The weights of the items
    :param values: The values of the items
    :param capacity: The capacity of the knapsack
    :return: A valid individual
    """

    while True:
        individual = [random.randint(0, 1) for _ in range(number_of_items)]
        if calculate_fitness(individual, weights, values, capacity) != -1:
            return individual


def run_ga(knapsack_instance):
    """
        Runs the genetic algorithm to solve the knapsack problem.
        :param knapsack_instance: The knapsack instance to solve
        :return: The result of the genetic algorithm
    """

    items = knapsack_instance["items"]
    weights = []
    values = []
    for item in items:
        weights.append(item["Weight"])
        values.append(item["Value"])
    capacity = knapsack_instance["capacity"]
    population_size = 50  # Number of individuals in the population

    start = timer()

    number_of_items = len(items)
    population = inizialize_population(population_size, number_of_items, weights, values, capacity)

    for generation in range(50): # Run the genetic algorithm for 50 generations
        best_individuals = selection(population, weights, values, capacity)
        new_population = []

        for i in range(population_size):
            # Randomly select two parents from the best individuals
            parent1 = random.choice(best_individuals)
            parent2 = random.choice(best_individuals)
            # Perform crossover and mutation to create the offspring
            offspring = crossover(parent1, parent2, weights, values, capacity)
            offspring = mutation(offspring)
            new_population.append(offspring)

        population = new_population # Update the population

    best_individuals = selection(population, weights, values, capacity)
    best_individual = max(best_individuals, key=lambda x: calculate_fitness(x, weights, values, capacity))

    end = timer()
    elapsed_time = utils.get_elapsed_time(start, end)

    best_items = []
    for i in range(0, len(best_individual)):
        if best_individual[i] == 1:
            best_items.append(items[i])

    return calculate_fitness(best_individual, weights, values, capacity), best_items, elapsed_time
