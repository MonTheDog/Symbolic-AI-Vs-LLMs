import json
import os
import matplotlib.pyplot as plt
from openai import OpenAI
from problog.logic import Term
from problog.program import PrologString


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


def get_probabilistic_instance(instance = 0):
    if instance == 0:
        return PrologString("""
        0.3::age(young); 0.5::age(adult); 0.2::age(old).
        
        0.6::sex(male); 0.4::sex(female).
        
        0.75::education(high) :- age(young), sex(male).
        0.72::education(high) :- age(adult), sex(male).
        0.88::education(high) :- age(old), sex(male).
        0.64::education(high) :- age(young), sex(female).
        0.70::education(high) :- age(adult), sex(female).
        0.90::education(high) :- age(old), sex(female).
        
        0.25::education(uni) :- age(young), sex(male).
        0.28::education(uni) :- age(adult), sex(male).
        0.12::education(uni) :- age(old), sex(male).
        0.36::education(uni) :- age(young), sex(female).
        0.30::education(uni) :- age(adult), sex(female).
        0.10::education(uni) :- age(old), sex(female).
        
        0.96::occupation(employed) :- education(high).
        0.92::occupation(employed) :- education(uni).
        
        0.04::occupation(self) :- education(high).
        0.08::occupation(self) :- education(uni).
        
        0.25::rent(small) :- education(high).
        0.20::rent(small) :- education(uni).
        
        0.75::rent(big) :- education(high).
        0.80::rent(big) :- education(uni).
        
        0.48::transport(car) :- occupation(employed), rent(small).
        0.56::transport(car) :- occupation(self), rent(small).
        0.58::transport(car) :- occupation(employed), rent(big).
        0.70::transport(car) :- occupation(self), rent(big).
        
        0.42::transport(train) :- occupation(employed), rent(small).
        0.36::transport(train) :- occupation(self), rent(small).
        0.24::transport(train) :- occupation(employed), rent(big).
        0.21::transport(train) :- occupation(self), rent(big).
    
        0.10::transport(other) :- occupation(employed), rent(small).
        0.08::transport(other) :- occupation(self), rent(small).
        0.18::transport(other) :- occupation(employed), rent(big).
        0.09::transport(other) :- occupation(self), rent(big).
        
        evidence(transport(car)).
        
        query(sex(male)).
        query(age(young)).
        query(education(uni)).
        """)
    if instance == 1:
        return PrologString("""
        0.90::pollution(high); 0.10::pollution(low).
        0.30::smoker(yes); 0.70::smoker(no).
        
        0.05::cancer(yes) :- pollution(high), smoker(yes).
        0.02::cancer(yes) :- pollution(high), smoker(no).
        0.03::cancer(yes) :- pollution(low), smoker(yes).
        0.001::cancer(yes) :- pollution(low), smoker(no).
        
        0.95::cancer(no) :- pollution(high), smoker(yes).
        0.98::cancer(no) :- pollution(high), smoker(no).
        0.97::cancer(no) :- pollution(low), smoker(yes).
        0.999::cancer(no) :- pollution(low), smoker(no).
        
        0.90::xray(yes) :- cancer(yes).
        0.20::xray(yes) :- cancer(no).
        
        0.10::xray(no) :- cancer(yes).
        0.80::xray(no) :- cancer(no).
        
        0.65::dyspnoea(yes) :- cancer(yes).
        0.30::dyspnoea(yes) :- cancer(no).
        
        0.35::dyspnoea(no) :- cancer(yes).
        0.70::dyspnoea(no) :- cancer(no).
        
        query(xray(yes)).
        query(dyspnoea(yes)).
    
        query(xray(no)).
        query(dyspnoea(no)).
        """)
    elif instance == 2:
        return PrologString("""
        0.01::burglary(yes); 0.99::burglary(no).
        
        0.02::earthquake(yes); 0.98::earthquake(no).
        
        0.95::alarm(yes) :- burglary(yes), earthquake(yes).
        0.29::alarm(yes) :- burglary(no), earthquake(yes).
        0.94::alarm(yes) :- burglary(yes), earthquake(no).
        0.001::alarm(yes) :- burglary(no), earthquake(no).
        
        0.05::alarm(no) :- burglary(yes), earthquake(yes).
        0.71::alarm(no) :- burglary(no), earthquake(yes).
        0.06::alarm(no) :- burglary(yes), earthquake(no).
        0.999::alarm(no) :- burglary(no), earthquake(no).
        
        0.90::johncalls(yes) :- alarm(yes).
        0.05::johncalls(yes) :- alarm(no).
        
        0.10::johncalls(no) :- alarm(yes).
        0.95::johncalls(no) :- alarm(no).
        
        0.70::marycalls(yes) :- alarm(yes).
        0.01::marycalls(yes) :- alarm(no).
        
        0.30::marycalls(no) :- alarm(yes).
        0.99::marycalls(no) :- alarm(no).
        
        query(johncalls(yes)).
        query(marycalls(yes)).
        
        query(johncalls(no)).
        query(marycalls(no)).
        """)


def get_logic_instance():
    return """
    parent(tobia, asia).
    parent(marta, asia).
    parent(domenico, giuseppe).
    parent(carmela, giuseppe).
    parent(domenico, gerardo).
    parent(carmela, gerardo).
    parent(giuseppe, franco).
    parent(asia, franco).
    parent(giuseppe, caterina).
    parent(asia, caterina).
    parent(caterina, antonio).
    parent(vincenzo, antonio).
    parent(gerardo, alfredo).
    parent(sara, alfredo).
    parent(gerardo, angela).
    parent(sara, angela).
    parent(alessia, celeste).
    parent(franco, celeste).
    parent(alessia, vittoria).
    parent(franco, vittoria).
    parent(alessia, leonardo).
    parent(franco, leonardo).
    parent(alfredo, andrea).
    parent(bianca, andrea).
    
    family_superpower(tobia, superstrength).
    family_superpower(marta, clairvoyance).
    family_superpower(domenico, fire).
    family_superpower(carmela, invisibility).
    family_superpower(sara, poison).
    family_superpower(alessia, wind).
    family_superpower(bianca, frost).
    family_superpower(vincenzo, healing).
    
    gender(tobia, male).
    gender(marta, female).
    gender(asia, female).
    gender(domenico, male).
    gender(carmela, female).
    gender(giuseppe, male).
    gender(gerardo, male).
    gender(sara, female).
    gender(alessia, female).
    gender(franco, male).
    gender(celeste, female).
    gender(caterina, female).
    gender(alfredo, male).
    gender(angela, female).
    gender(bianca, female).
    gender(andrea, male).
    gender(vincenzo, male).
    gender(antonio, male).
    gender(vittoria, female).
    gender(leonardo, male).
    
    father(X, Y) :- parent(X, Y), gender(X, male).
    mother(X, Y) :- parent(X, Y), gender(X, female).
    
    grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
    grandfather(X, Y) :- grandparent(X, Y), gender(X, male).
    grandmother(X, Y) :- grandparent(X, Y), gender(X, female).
    
    sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
    brother(X, Y) :- sibling(X, Y), gender(X, male).
    sister(X, Y) :- sibling(X, Y), gender(X, female).
    
    cousin(X, Y) :- parent(P1, X), parent(P2, Y), sibling(P1, P2), X \= Y.
    
    family_superpower(X, P) :- gender(X, male), father(F, X), F \= X, family_superpower(F, P).
    family_superpower(X, P) :- gender(X, female), mother(M, X), M \= X, family_superpower(M, P).
    """


def get_logic_queries():
    return ["family_superpower(Y, X)","father(X, celeste)", "mother(X, celeste)", "brother(X, celeste)", "sister(X, celeste)","grandfather(X, celeste)", "grandmother(X, celeste)","cousin(celeste, X)"]


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


def print_probability_dict(result):
    """
    Prints the probability dict for the given result.
    :param result: the dict for the probabilistic reasoning computation.
    """
    result_string = ""

    for key in result.keys():
        result_string += str(key) + ": " + str(format(round(result[key], 6), ".6f")) + "\n"

    result_string = result_string[:-1]

    print(result_string)


def plot_values(sk_values, llm_values, model_name):
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
    axes[1].set_title(model_name)
    axes[1].set_xlabel("Valori")
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    #plt.savefig(os.path.join("..", "plots", "values-plot-SAI-vs-" + model_name + ".png"))
    plt.show()
