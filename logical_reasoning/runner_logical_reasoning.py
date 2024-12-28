from operator import concat

import llm_logical_reasoning as llml
import symbolic_logical_reasoning as sl
import utils

print("=================================================")
print("LLMs vs Symbolic AI - Superhero Family")
print("=================================================")

prolog_script = utils.get_logic_instance()
knowledge_base = sl.get_knowledge_base(prolog_script)

queries = utils.get_logic_queries()
request_query = ""
for query in queries:
    request_query += query + ".\n"

llm_agent = llml.LogicalReasoningPrologStyleLLMAgent("o1")

print("Solved Logical Problem: ")
sl.solve_logic_problem(knowledge_base)
print()

print("LLM Solution: ")
response = llm_agent.solve_logical_problem(prolog_script, request_query)

