from timeit import default_timer as timer
from pyswip import Prolog
import utils
from utils import print_elapsed_time


def get_knoweldge_base(prolog_script):
    knoweldge_base = Prolog()

    # Split the script by '.' (Prolog facts and rules are terminated with '.')
    rules = prolog_script.strip().split('.')

    # Loop through the rules and assert them one by one
    for rule in rules:
        rule = rule.strip()
        if rule:
            knoweldge_base.assertz(rule)

    return knoweldge_base


def solve_logic_problem(kb):
    queries = utils.get_logic_queries()

    start = timer()

    print("Family Superpowers")
    query_superpowers = list(kb.query(queries[0]))
    for solution in query_superpowers:
        print(f"{solution['Y']}'s superpower is {solution['X']}")

    print("\nCeleste's family")
    query_father = list(kb.query(queries[1]))
    print(f"Celeste's father is {query_father[0]['X']}")
    query_mother = list(kb.query(queries[2]))
    print(f"Celeste's mother is {query_mother[0]['X']}")
    query_brother = list(kb.query(queries[3]))
    print(f"Celeste's brother is {query_brother[0]['X']}")
    query_sister = list(kb.query(queries[4]))
    print(f"Celeste's sister is {query_sister[0]['X']}")
    query_grandpa = list(kb.query(queries[5]))
    print(f"Celeste's grandpa is {query_grandpa[0]['X']}")
    query_grandma = list(kb.query(queries[6]))
    print(f"Celeste's grandma is {query_grandma[0]['X']}")
    query_cousin = list(kb.query(queries[7]))
    print(f"Celeste's cousin is {query_cousin[0]['X']}")

    end = timer()

    print_elapsed_time(start, end)


# Combine all facts and rules into a single string, including comments
prolog_script = utils.get_logic_instance()

kb = get_knoweldge_base(prolog_script)

solve_logic_problem(kb)
