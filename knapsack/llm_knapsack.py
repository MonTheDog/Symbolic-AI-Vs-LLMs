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
import utils
from timeit import default_timer as timer



"""
Prompt templates and utility functions
"""
KNAPSACK_PROMPT_BASE_4O = """
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

MAPPING_MODEL_NAME_TO_BASE_PROMPT = {
    "4o": KNAPSACK_PROMPT_BASE_4O,
    "o1": KNAPSACK_PROMPT_BASE_O1
}



"""
Adapter functions (currently valid for 4o and o1)
"""
def knapsack_to_llm_adapter(prompt, instance):
    """
    Input: items of the instance of knapsack problem as defined in /utils.py
    Output: prompt formatted with the items converted to a json string and the capacity
    """
    return prompt.format(json.dumps(instance["items"]), instance["capacity"])


"""
Conversation builders
"""
KNAPSACK_4O_CONVERSATION = [
    {"role": "system", "content": "You have a set of items. Each item has a weight and a value. You have a knapsack that has a maximum capacity. Your goal is to maximize the value of the items you carry in the knapsack without exceeding the maximum capacity (the subset you select should be that with the maximum total value which is less than or equal to the maximum capacity). In the answer, include a string with the reasoning you used to find the solution and a json string with the solution in the form specified below."},
]

KNAPSACK_O1_CONVERSATION = [
]

MAPPING_MODEL_NAME_TO_CONVERSATION = {
    "4o": KNAPSACK_4O_CONVERSATION,
    "o1": KNAPSACK_O1_CONVERSATION
}


"""
Response schemas (currently valid for 4o)
"""
class KnapsackItemSchema(BaseModel):
    Name: str
    Weight: int
    Value: int

    def to_dict(self):
        return self.model_dump()
    

class KnapsackOutputSchema(BaseModel):
    reasoning: str
    solution: list[KnapsackItemSchema]
    


"""
Response checkers (currently necessary for o1)
"""
def knapsack_4o_internal_checking_schema(response, capacity):
    """
    Internal schema: the sum of the weights of the items in the solution is less than or equal to the maximum capacity
    """
    total_weight = sum(item.Weight for item in response.solution)
    if total_weight > capacity:
        return False, "The total weight of the items in the solution is greater than the maximum capacity. Please provide another solution."
    return json.dumps([item.to_dict() for item in response.solution]), ""


def knapsack_o1_internal_checking_schema(response, capacity):
    """
    Pre-processing step: everything which is not contained in the square brackets is removed.
    Internal schema: - String response can be converted to list of dictionaries with keys name, weight and value
    - the sum of the weights of the items in the solution is less than or equal to the maximum capacity
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
        return False, "The response cannot be converted to a list of dictionaries (JSON format). Please provide another response that adheres to the schema."
    if not isinstance(response, list):
        return False, "The response is not a list. Please provide a list of dictionaries that adheres to the schema."
    
    for item in response:
        if not isinstance(item, dict):
            return False, "An object in the response is not a dictionary. Please provide a list of dictionaries that adheres to the schema."
        if "Name" not in item or not isinstance(item["Name"], str):
            return False, "An object in the response does not have a key 'Name'. Please provide a list of dictionaries that adheres to the schema."
        if "Weight" not in item or not isinstance(item["Weight"], (int, float)):
            return False, "An object in the response does not have a key 'Weight'. Please provide a list of dictionaries that adheres to the schema."
        if "Value" not in item or not isinstance(item["Value"], (int, float)):
            return False, "An object in the response does not have a key 'Value'. Please provide a list of dictionaries that adheres to the schema."
         
    total_weight = sum(item["Weight"] for item in response)
    if total_weight > capacity:
        return False, "The total weight of the items in the solution is greater than the maximum capacity. Please provide another solution."
    return response, ""


MAPPING_MODEL_NAME_TO_INTERNAL_CHECKING_SCHEMA = {
    "4o": knapsack_4o_internal_checking_schema,
    "o1": knapsack_o1_internal_checking_schema
}



"""
LLM Agent   
"""
class KnapsackLLMAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = utils.get_openai_client()
        self.base_prompt = MAPPING_MODEL_NAME_TO_BASE_PROMPT[model_name]
        self.conversation = MAPPING_MODEL_NAME_TO_CONVERSATION[model_name]
        self.output_schema = KnapsackOutputSchema if model_name == "4o" else None
        self.internal_checking_schema = MAPPING_MODEL_NAME_TO_INTERNAL_CHECKING_SCHEMA[model_name]

        
    def update_conversation(self, role, content):
        self.conversation.append({"role": role, "content": content})


    def action(self, capacity):
        """
        Response generation, internal checking.
        """
        if self.model_name == "4o":
            response = utils.interrogate_4o(self.client, "mini", self.conversation, self.output_schema)
        elif self.model_name == "o1":
            response = utils.interrogate_o1(self.client, "mini", self.conversation)
        self.update_conversation("assistant", response)
        is_valid, feedback_message = self.internal_checking_schema(response, capacity)
        if self.model_name == "4o":
            return is_valid, feedback_message, response.reasoning
        elif self.model_name == "o1":
            return is_valid, feedback_message, "No reasoning available"

    
    def action_loop(self, knapsack_instance, max_moves=3):
        """
        Response generation, internal checking.
        """
        start = timer()
        prompt = knapsack_to_llm_adapter(self.base_prompt, knapsack_instance)
        self.update_conversation("user", prompt)
        i = 0
        while i < max_moves:
            is_valid, feedback_message, reasoning = self.action(knapsack_instance["capacity"])
            if is_valid:
                if self.model_name == "4o":
                    total_value = sum(item["Value"] for item in json.loads(is_valid))
                elif self.model_name == "o1":
                    total_value = sum(item["Value"] for item in is_valid)
                    is_valid = json.dumps(is_valid)
                end = timer()
                utils.print_elapsed_time(start, end)
                return True, is_valid, reasoning, total_value
            else:
                i+=1
                self.update_conversation("user", feedback_message)
        end = timer()
        utils.print_elapsed_time(start, end)
        return False, "No solution found", "No reasoning available", 0


















