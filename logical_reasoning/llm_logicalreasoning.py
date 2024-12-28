#  File per implementare l'agente llm per ragionamento logico stile Prolog


"""
External Dependencies:
"""
import json
import utils
from pydantic import BaseModel, ConfigDict
from typing import List

"""
Prompt templates and utility functions
"""

INSTRUCTION_PROMPT = """
Your goal is to solve the following logical inference problem. You will be provided with a knowledge base in Prolog format. The knowledge base can be composed by facts and rules. A fact is written in the format Functor(Name), which means that the property Functor is true for the object Name. A rule is written in the format Functor1(name1) :- Functor2(name2), which means that the property Functor1 is true for the object Name1 if the property Functor2 is true for the object Name2. Facts and rules can contain variables, which starts either with a capital letter or with an underscore.

You will be provided with a query written in the same format. If the query does not contain variables, your goal is to determine if it is true or false given the knowledge base. If the query contains variables, your goal is to find all the assignments of values to variables that make the query true. If there is no such assignment, tell that the query is false. In the answer, include a json string with the solution in the form specified below. Include only the json string in the form below, without any additional information. If the query does not contain variables, under the "Assignments" field, provide an empty list.
"""


LOGICAL_REASONING_PROLOG_STYLE_PROMPT_BASE_4O = """
Knowledge base: ###
{}
###

Query: ###
{}
###


Desired format: ###
reasoning: ....

answer: True or False

assignments:
[
    {{
        "X": "Value1",
        "Y": "Value2", (empty string if the variable is not present in the query),
        "Z": "Value3" (empty string if the variable is not present in the query),
    }},
    {{
        "X": "Value1",
        "Y": "Value2", (empty string if the variable is not present in the query),
        "Z": "Value3" (empty string if the variable is not present in the query),
    }},
    ....
]
###

"""


LOGICAL_REASONING_PROLOG_STYLE_PROMPT_BASE_O1 = """
Instructions: ###
{}
###


Knowledge base: ###
{}
###

Query: ###
{}
###

Desired format: ###
answer: True or False

assignments:
[
    {{
        "X": "Value1",
        "Y": "Value2", (empty string if the variable is not present in the query),
        "Z": "Value3" (empty string if the variable is not present in the query),
    }},
    {{
        "X": "Value1",
        "Y": "Value2", (empty string if the variable is not present in the query),
        "Z": "Value3" (empty string if the variable is not present in the query),
    }},
    ....
]
###
"""

MAPPING_MODEL_NAME_TO_BASE_PROMPT = {
    "4o": LOGICAL_REASONING_PROLOG_STYLE_PROMPT_BASE_4O,
    "o1": LOGICAL_REASONING_PROLOG_STYLE_PROMPT_BASE_O1
}

"""
Conversation builders
"""

LOGICAL_REASONING_PROLOG_STYLE_4O_CONVERSATION = [
    {
        "role": "system",
        "content": INSTRUCTION_PROMPT
    }
]

LOGICAL_REASONING_PROLOG_STYLE_O1_CONVERSATION = [
]

MAPPING_MODEL_NAME_TO_CONVERSATION = {
    "4o": LOGICAL_REASONING_PROLOG_STYLE_4O_CONVERSATION,
    "o1": LOGICAL_REASONING_PROLOG_STYLE_O1_CONVERSATION
}



"""Response schemas (currently valid for 4o)
Supports up to 3 variables in the query
"""

class LogicalReasoningPrologStyleResponseAssignments(BaseModel):
    X: str
    Y: str
    Z: str


class LogicalReasoningPrologStyleResponse(BaseModel):
    reasoning: str
    answer: str
    assignments: List[LogicalReasoningPrologStyleResponseAssignments]








"""
Response checkers 
"""

def logical_reasoning_prolog_style_4o_internal_checking_schema(response):
    """
    Dummy checker, since the output is structured
    """
    return response, "The response adheres to the schema."


def logical_reasoning_prolog_style_o1_internal_checking_schema(response):
    """
    Pre-processing step: everything which is not contained in the curly brackets is removed.
    Internal schema: - String response can be converted to a dictionary with keys "reasoning", "answer", "assignments".
    - "answer" is a string, either "True" or "False".
    - "assignments" is either an empty string or it can be converted to a dictionary with keys "Var1", "Var2", ... and values "Value1", "Value2", ...
    
    Input: string response provided by the LLM
    """
    first_bracket = response.find("{")
    last_bracket = response.rfind("}")
    if first_bracket == -1 or last_bracket == -1:
        return False, "The response does not match the expected structure with respect to the curly brackets. Please provide another response that adheres to the schema."
    response = response[first_bracket:last_bracket+1]
    try:
        response_dict = json.loads(response)
    except:
        return False, "The response is not a valid json string. Please provide another response that adheres to the schema."

    if not isinstance(response_dict, dict):
        return False, "The response cannot be converted to a dictionary. Please provide another response that adheres to the schema."

    if "answer" not in response_dict:
        return False, "The response does not contain the 'answer' field. Please provide another response that adheres to the schema."
    
    if not isinstance(response_dict["assignments"], list):
        return False, "The 'assignments' field is not a list. Please provide another response that adheres to the schema."
    
    for assignment in response_dict["assignments"]:
        if not isinstance(assignment, dict):
            return False, "An assignment is not a dictionary. Please provide another response that adheres to the schema."

    return response_dict, "The response adheres to the schema."


"""
LLM Agent
"""    
class LogicalReasoningPrologStyleLLMAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = utils.get_openai_client()
        self.base_prompt = MAPPING_MODEL_NAME_TO_BASE_PROMPT[model_name]
        self.conversation = MAPPING_MODEL_NAME_TO_CONVERSATION[model_name]
        self.output_schema = LogicalReasoningPrologStyleResponse if model_name == "4o" else None
        self.internal_checking_schema = logical_reasoning_prolog_style_4o_internal_checking_schema if model_name == "4o" else logical_reasoning_prolog_style_o1_internal_checking_schema

    def update_conversation(self, role, content):
        self.conversation.append({"role": role, "content": content})

    def action(self):
        """
        Response generation
        """
        if self.model_name == "4o":
            response = utils.interrogate_4o(self.client, "mini", self.conversation, self.output_schema)
        elif self.model_name == "o1":
            response = utils.interrogate_o1(self.client, "mini", self.conversation)
        self.update_conversation("assistant", response)
        is_valid, feedback_message = self.internal_checking_schema(response)
        return is_valid, feedback_message
    

    def action_loop(self, kb, query, max_moves=3):
        if self.model_name == "4o":
            self.update_conversation("user", self.base_prompt.format(kb, query))
        elif self.model_name == "o1":
            self.update_conversation("user", self.base_prompt.format(INSTRUCTION_PROMPT, kb, query))
        while max_moves > 0:
            is_valid, feedback_message = self.action()
            if is_valid:
                return is_valid
            else:
                self.update_conversation("user", feedback_message)
                max_moves -= 1
        return False

