#  File per implementare l'agente llm per ragionamento probabilistico stile Prolog

"""
External Dependencies:
"""

import json
from pydantic import BaseModel
from typing import Dict, Any, List


"""
Internal Dependencies:
"""

import utils

"""
Prompt templates and utility functions
"""
INSTRUCTION_PROMPT = """
You will be provided with a Bayesian network and values for a set of evidence variables. Your task is to compute the posterior probability of one or more query variables that will be specified in the problem.
The Bayesian network and the evidence and query variables are in Problog format. X::Var(Y) means that the prior probability that Var has value Y is X. X::Var1(Y) :- Var2(Z), Var3(W) means that X is the probability that Var1 has value Y conditioned on Var2 and Var3 having values Z and W respectively. 
Evidence(Var(X)) means that the evidence is that Var has value X. Query(Var) means that your goal is to compute the posterior probability of Var given the evidence. Please, generate the answer in the format specified below.
"""

PROBABILISTIC_REASONING_PROBLOG_STYLE_PROMPT_BASE_4O = """
Bayesian network: ###
{}
###

Evidence: ###
{}
###

Query: ###
{}
###

Desired format: ###
[
    {{
        "variable": "Var",
        "value": "Value1",
        "probability": "Probability1"
    }},
    {{
        "variable": "Var",
        "value": "Value2",
        "probability": "Probability2"
    }},
    ....
]
###
"""

PROBABILISTIC_REASONING_PROBLOG_STYLE_PROMPT_BASE_O1 = """
Instructions: ###
{}
###

Bayesian network: ###
{}
###

Evidence: ###
{}
###

Query: ###
{}
###

Desired format: ###
[
    {{
        "variable": "Var",
        "value": "Value1",
        "probability": "Probability1"
    }},
    {{
        "variable": "Var",
        "value": "Value2",
        "probability": "Probability2"
    }},
    ....
]
###
"""

MAPPING_MODEL_NAME_TO_BASE_PROMPT = {
    "4o": PROBABILISTIC_REASONING_PROBLOG_STYLE_PROMPT_BASE_4O,
    "o1": PROBABILISTIC_REASONING_PROBLOG_STYLE_PROMPT_BASE_O1
}

"""
Conversation builders
"""

PROBABILISTIC_REASONING_PROBLOG_STYLE_4O_CONVERSATION = [
    {
        "role": "system",
        "content": INSTRUCTION_PROMPT
    }
]

PROBABILISTIC_REASONING_PROBLOG_STYLE_O1_CONVERSATION = [
]

MAPPING_MODEL_NAME_TO_CONVERSATION = {
    "4o": PROBABILISTIC_REASONING_PROBLOG_STYLE_4O_CONVERSATION,
    "o1": PROBABILISTIC_REASONING_PROBLOG_STYLE_O1_CONVERSATION
}



"""Response schemas (currently valid for 4o)"""

class ProbabilisticReasoningProblogStyleProbability(BaseModel):
    variable: str
    value: str
    probability: float

class ProbabilisticReasoningProblogStyleResponse(BaseModel):
    result: List[ProbabilisticReasoningProblogStyleProbability]

"""
Response checkers (not necessary since responses will be analyzed manually at this stage)
"""
def probabilistic_reasoning_problog_style_4o_internal_checking_schema(response):
    """
    Dummy checker, since the output is structured
    """
    return response, "The response adheres to the schema."

def probabilistic_reasoning_problog_style_o1_internal_checking_schema(response):
    """
    Pre-processing step: everything which is not contained in the square brackets is removed.
    Internal schema: - String response can be converted to a list of dictionaries with keys "Variable", "Value", "PosteriorProbability".
    - "Variable" is a string.
    - "Value" is a string.
    - "PosteriorProbability" is a float.
    Input: string response provided by the LLM
    """
    first_bracket = response.find("[")
    last_bracket = response.find("]")
    if first_bracket == -1 or last_bracket == -1:
        return False, "The response does not match the expected structure with respect to the square brackets. Please provide another response that adheres to the schema."
    response = response[first_bracket:last_bracket+1]
    try:
        response_list = json.loads(response)
    except:
        return False, "The response is not a valid json string. Please provide another response that adheres to the schema."

    if not isinstance(response_list, list):
        return False, "The response cannot be converted to a list. Please provide another response that adheres to the schema."

    for item in response_list:
        if not isinstance(item, dict):
            return False, "The response cannot be converted to a list of dictionaries. Please provide another response that adheres to the schema."
        if "variable" not in item or "value" not in item or "probability" not in item:
            return False, "The response does not contain the required fields. Please provide another response that adheres to the schema."
        if not isinstance(item["variable"], str) or not isinstance(item["value"], str):
            return False, "The response does not contain the required fields with the correct type. Please provide another response that adheres to the schema."

    return response, "The response adheres to the schema."


"""
LLM Agent
"""    
class ProbabilisticReasoningProblogStyleLLMAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = utils.get_openai_client()
        self.base_prompt = MAPPING_MODEL_NAME_TO_BASE_PROMPT[model_name]
        self.conversation = MAPPING_MODEL_NAME_TO_CONVERSATION[model_name]
        self.output_schema = ProbabilisticReasoningProblogStyleResponse if model_name == "4o" else None
        self.internal_checking_schema = probabilistic_reasoning_problog_style_4o_internal_checking_schema if model_name == "4o" else probabilistic_reasoning_problog_style_o1_internal_checking_schema

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
    
    def action_loop(self, bn, evidence, query, max_moves=3):
        if self.model_name == "4o":
            self.update_conversation("user", self.base_prompt.format(bn, evidence, query))
        elif self.model_name == "o1":
            self.update_conversation("user", self.base_prompt.format(INSTRUCTION_PROMPT, bn, evidence, query))
        while max_moves > 0:
            print(self.conversation)
            is_valid, feedback_message = self.action()
            if is_valid:
                return is_valid
            else:
                self.update_conversation("user", feedback_message)
                max_moves -= 1
        return False, "The response does not adhere to the schema after 3 attempts. Please provide another response that adheres to the schema."
