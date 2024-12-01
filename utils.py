# File per le funzioni utilizzate in tutto il progetto (inizializzazione delle istanze dei problemi come il knapsack
# o funzioni di valutazione sul tempo o sulla qualità delle soluzioni)

def get_knapsack_instance():
    """
    Returns the knapsack instance to be solved by the agents.

    :return: A dictionary containing:
            'items': the list of items, each with the attributes 'Name', 'Weight', and 'Value'.
            'capacity': the maximum capacity of the knapsack.
    """
    items = [
        {"Name": "Golden Watch", "Weight": 1, "Value": 500},
        {"Name": "Diamond Necklace", "Weight": 2, "Value": 1200},
        {"Name": "First Edition Charizard Card", "Weight": 1, "Value": 1500},
        {"Name": "Infinity Gauntlet Replica", "Weight": 5, "Value": 1000},
        {"Name": "Laptop", "Weight": 3, "Value": 900},
        {"Name": "Master Sword Replica", "Weight": 4, "Value": 800},
        {"Name": "Rare Wine Bottle", "Weight": 4, "Value": 600},
        {"Name": "Vault-Tec Lunchbox", "Weight": 1, "Value": 200},
        {"Name": "Silver Coins", "Weight": 6, "Value": 400},
        {"Name": "Crystal Chandelier", "Weight": 8, "Value": 1500},
        {"Name": "Vintage Guitar", "Weight": 5, "Value": 1100},
        {"Name": "Gold Bar", "Weight": 10, "Value": 2500},
        {"Name": "Silk Tapestry", "Weight": 3, "Value": 600},
        {"Name": "Lightsaber Replica", "Weight": 3, "Value": 1200},
        {"Name": "Designer Sunglasses", "Weight": 1, "Value": 400},
        {"Name": "Rare Book", "Weight": 2, "Value": 500},
        {"Name": "Antique Clock", "Weight": 5, "Value": 1200},
        {"Name": "Vault Key", "Weight": 1, "Value": 1000},
        {"Name": "Luxury Perfume", "Weight": 1, "Value": 200},
        {"Name": "Artistic Sculpture", "Weight": 6, "Value": 1300},
        {"Name": "Emerald Ring", "Weight": 1, "Value": 700},
        {"Name": "Pokéball Collector's Edition", "Weight": 1, "Value": 600},
        {"Name": "Gold Chain", "Weight": 2, "Value": 600},
        {"Name": "Fancy Hat", "Weight": 1, "Value": 150},
        {"Name": "Wedding Crown", "Weight": 3, "Value": 2000},
    ]
    capacity = 20

    return {
        'items': items,
        'capacity': capacity
    }


def print_elapsed_time(start, end):
    """
    Prints and formats the elapsed time from start to end.\n
    To get start and end add the following import\n
    "from timeit import default_timer as timer"\n
    and call start = timer() at the start and end = timer() at the end
    :param start: The starting time
    :param end: The end time
    """
    def truncate_float(float_number, decimal_places):
        multiplier = 10 ** decimal_places
        return int(float_number * multiplier) / multiplier
    print("Elapsed Time: " + format(truncate_float((end - start) * 1000, 4), ".4f") + "ms")
