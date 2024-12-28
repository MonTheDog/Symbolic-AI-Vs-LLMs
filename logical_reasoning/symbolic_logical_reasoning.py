from timeit import default_timer as timer
from pyswip import Prolog
import utils
from utils import print_elapsed_time

singleton_check = False

def get_knowledge_base(prolog_script):
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


# Prendere i risultati della symbolic AI e renderli una lista di frasi, ogni frase è composta da token (relazione, x, y ad es)
# Fare lo stesso procedimento con output di 4o e o1

# Per ogni frase, controllare se vi è un corrispondente in 4o e o1 (corrispondente varia da caso a caso, ci sono volte in cui
# relazioni come "cugino" hanno un termine extra ma sono giuste, oppure casi in cui non è importante l'ordine dei token, ecc)

# Se vi è corrispondenza, si conta come giusta e si elimina dalla lista di 4o e o1

# Se vi è la relazione ma i termini sono sbagliati (anche qui va capito cosa significa "sbagliato", perché varia da caso a caso,
# a volte sbagliato è se anche un solo termine non corrisponde, altre volte potrebbe essere solo se sono entrambi sbagliati, ecc)
# si conta come errata e si elimina dalla lista di 4o e o1

# Se non vi è la corrispondenza si conta come mancante e si passa alla prossima

# Alla fine si conta il numero di frasi rimanenti nella lista di 4o e o1 e sono contante come aggiunte
