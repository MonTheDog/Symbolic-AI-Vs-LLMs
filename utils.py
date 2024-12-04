# File per le funzioni utilizzate in tutto il progetto (inizializzazione delle istanze dei problemi come il knapsack
# o funzioni di valutazione sul tempo o sulla qualità delle soluzioni)

import json
import os
import matplotlib.pyplot as plt
from openai import OpenAI

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
    :return: The elapsed time in milliseconds
    """
    def truncate_float(float_number, decimal_places):
        multiplier = 10 ** decimal_places
        return int(float_number * multiplier) / multiplier

    elapsed_time = format(truncate_float((end - start) * 1000, 4), ".4f")
    print("Elapsed Time: " + elapsed_time + "ms")

    return float(elapsed_time)


def get_openai_client(api_key="API_KEY"):
    """
    Returns the OpenAI client (takes as input the api key).
    """
    return OpenAI(api_key=api_key)


def interrogate_4o(client, model, conversation, response_format):
    """
    Interrogates the 4o LLM with the given prompt.

    Args:
        client (OpenAI): The OpenAI client.
        model (str): if "mini" then gpt-4o-mini is used, otherwise gpt-4o.
        conversation (list): The conversation history.
        response_format (BaseModel): The response format (schema for structured output).
    """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini" if model == "mini" else "gpt-4o",
        messages=conversation,
        response_format=response_format,
    )
    return completion.choices[0].message.parsed


def interrogate_o1(client, model, conversation):
    """
    Interrogates the o1 LLM with the given prompt.

    Args:
        client (OpenAI): The OpenAI client.
        model (str): if "mini" then o1-mini is used, otherwise o1.
        conversation (list): The conversation history (includes only user and assistant messages).
        response_format (BaseModel): The response format (schema for structured output).
    """
    completion = client.chat.completions.create(
        model="o1-mini" if model == "mini" else "o1",
        messages=conversation,
    )
    return completion.choices[0].message.content


def plot_values(sk_values, llm_values):
    """
    Plots the values obtained by the Symbolic AI and the LLM.
    :param sk_values: The values obtained by the Symbolic AI.
    :param llm_values: The values obtained by the LLM.
    """
    bins = range(6000, 10500, 200)  # Intervals from 6000 to 10800 with a 200 step

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

    axes[0].hist(sk_values, bins=bins, edgecolor='black', alpha=0.7, color='red')
    axes[0].set_title("Symbolic AI")
    axes[0].set_xlabel("Valori")
    axes[0].set_ylabel("Frequenza")
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    axes[1].hist(llm_values, bins=bins, edgecolor='black', alpha=0.7, color='blue')
    axes[1].set_title("LLM")
    axes[1].set_xlabel("Valori")
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(os.path.join("..", "plots", "values_plot.png"))
    plt.show()
