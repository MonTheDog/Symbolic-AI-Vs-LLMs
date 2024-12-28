import llm_logicalreasoning


print("======================== LLM ========================")

kb = """
woman(mia).
woman(jody).
woman(yolanda).
playsAirGuitar(jody).
party.
"""

query = """
woman(X).
"""

llm_agent = llm_logicalreasoning.LogicalReasoningPrologStyleLLMAgent("o1")

response = llm_agent.action_loop(kb, query)

print(response)

