# File per implementare l'agente llm per risolvere il problema dello zaino

#  Possible TODOS:
#  - Introduce few-shot (fine-tuning?)

"""
External Dependencies
"""
import json
import sys
import os
import importlib
import re
from pydantic import BaseModel



"""
Internal Dependencies
"""
sys.path.append(os.path.abspath("C:/Users/paolo/Desktop/Symbolic-AI-Vs-LLMs"))
import utils



"""
Prompt variables
"""
KNAPSACK_PROMPT_BASE_4O = """
You have a set of items. Each item has a weight and a value. You have a knapsack that has a maximum capacity. Your goal is to maximize the value of the items you carry in the knapsack without exceeding the maximum capacity (the subset you select should be that with the maximum total value which is less than or equal to the maximum capacity). In the answer, include a string with the reasoning you used to find the solution and a json string with the solution in the form specified below.

Items: ###
{}
###

MaximumCapacity: ###
{}
###

Desired format: ###
Reasoning: ....

Solution: 
[
    {{
        "Name": "....",
        "Weight": ...,
        "Value": ...
    }},
    {{
        "Name": "....",
        "Weight": ...,
        "Value": ...
    }},
    ....
]
###
"""



KNAPSACK_PROMPT_BASE_O1 = """
You have a set of items. Each item has a weight and a value. You have a knapsack that has a maximum capacity. Your goal is to maximize the value of the items you carry in the knapsack without exceeding the maximum capacity. In the answer, include a json string with the solution in the form specified below. Include only the json string in the form below, without any additional information. 

Items: ###
{}
###

MaximumCapacity: ###
{}
###

Desired format: ###
[
    {{
        "Name": "....",
        "Weight": ...,
        "Value": ...
    }},
    {{
        "Name": "....",
        "Weight": ...,
        "Value": ...
    }},
]
###
"""



"""
Adapter functions (currently valid for 4o and o1)
"""
def knapsack_to_llm_adapter(prompt):
    """
    Input: items of the instance of knapsack problem as defined in /utils.py
    Output: prompt formatted with the items converted to a json string and the capacity
    """
    instance = utils.get_knapsack_instance()
    return prompt.format(json.dumps(instance["items"]), instance["capacity"])


"""
Conversation builders
"""
KNAPSACK_4O_CONVERSATION = [
    {"role": "system", "content": "You have to solve the knapsack problem."},
    {"role": "user", "content": knapsack_to_llm_adapter(KNAPSACK_PROMPT_BASE_4O)}
]

KNAPSACK_O1_CONVERSATION = [
    {"role": "user", "content": knapsack_to_llm_adapter(KNAPSACK_PROMPT_BASE_O1)}
]


"""
Response schemas (currently valid for 4o)
"""
class KnapsackItemSchema(BaseModel):
    name: str
    weight: int
    value: int

class KnapsackOutputSchema(BaseModel):
    reasoning: str
    solution: list[KnapsackItemSchema]


"""
Response checkers (currently necessary for o1)
"""
def knapsack_checking_schema(response):
    """
    Boolean function that checks if the response provided by a LLM without the response format feature adheres to the required schema.
    Includes a pre-processing step where everything which is not contained in the square brackets is removed.
    Such a pre-processing step has been derived from the observation that the LLM sometimes includes additional information in the response.
    
    If the check is successful, the function returns the response in the correct format.
    Otherwise, it returns False.

    Input: string response provided by the LLM
    """
    match = re.search(r'(\[.*\])', response, re.DOTALL)  #  pre-processing step
    if not match:
        return False
    response = match.group(1)
    
    try:
        response = json.loads(response)
    except:
        return False
    if not isinstance(response, list):
        return False
    
    for item in response:
        if not isinstance(item, dict):
            return False
        if "Name" not in item or not isinstance(item["Name"], str):
            return False
        if "Weight" not in item or not isinstance(item["Weight"], (int, float)):
            return False
        if "Value" not in item or not isinstance(item["Value"], (int, float)):
            return False
         
    return response



"""
Example usage
"""
if __name__ == "__main__":
    client = utils.get_openai_client()
    response = utils.interrogate_4o(client, "mini", KNAPSACK_4O_CONVERSATION, KnapsackOutputSchema)
    print("Response from 4o: ", response)
    response = utils.interrogate_o1(client, "mini", KNAPSACK_O1_CONVERSATION, knapsack_checking_schema)
    print("Response from o1: ", response)












