from timeit import default_timer as timer
from pyswip import Prolog
import utils

singleton_check = False

def get_knowledge_base(prolog_script):
    """
    This function returns the knowledge base object from a valid prolog script
    :param prolog_script: The prolog script to generate the knoweldge base
    :return: The knowledge base object
    """
    global singleton_check
    if singleton_check:
        return Prolog()
    else:
        singleton_check = True
    knowledge_base = Prolog()

    # Split the script by '.' (Prolog facts and rules are terminated with '.')
    rules = prolog_script.strip().split('.')

    # Loop through the rules and assert them one by one
    for rule in rules:
        rule = rule.strip()
        if rule:
            knowledge_base.assertz(rule)

    return knowledge_base


def solve_logic_problem(kb):
    queries = utils.get_logic_queries()

    result = []

    start = timer()

    #print("Family Superpowers")
    query_superpowers = list(kb.query(queries[0]))
    for solution in query_superpowers:
        #print(f"{solution['Y']}'s superpower is {solution['X']}")
        result.append("family_superpower " + solution['X'] + " " + solution['Y'])

    #print("\nCeleste's family")
    query_father = list(kb.query(queries[1]))
    #print(f"Celeste's father is {query_father[0]['X']}")
    result.append("father " + query_father[0]['X'])

    query_mother = list(kb.query(queries[2]))
    #print(f"Celeste's mother is {query_mother[0]['X']}")
    result.append("mother " + query_mother[0]['X'])

    query_brother = list(kb.query(queries[3]))
    #print(f"Celeste's brother is {query_brother[0]['X']}")
    result.append("brother " + query_brother[0]['X'])

    query_sister = list(kb.query(queries[4]))
    #print(f"Celeste's sister is {query_sister[0]['X']}")
    result.append("sister " + query_sister[0]['X'])

    query_grandpa = list(kb.query(queries[5]))
    #print(f"Celeste's grandfather is {query_grandpa[0]['X']}")
    result.append("grandfather " + query_grandpa[0]['X'])

    query_grandma = list(kb.query(queries[6]))
    #print(f"Celeste's grandmother is {query_grandma[0]['X']}")
    result.append("grandmother " + query_grandma[0]['X'])

    query_cousin = list(kb.query(queries[7]))
    #print(f"Celeste's cousin is {query_cousin[0]['X']}")
    result.append("cousin " + query_cousin[0]['X'])

    end = timer()

    time = utils.get_elapsed_time(start, end)

    return result, time