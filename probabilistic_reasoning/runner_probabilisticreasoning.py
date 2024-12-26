print("--------LLM---------------")

import llm_probabilisticreasoning

bn = """
0.7::tempo(piove). 
0.5::tempo(bagnato).
0.9::tempo(piove) :- tempo(bagnato).
0.1::tempo(piove) :- \+ tempo(bagnato).
"""

evidence = """
Evidence(tempo(piove)).
"""

query = """
Query(tempo(bagnato)).
"""

llm_agent = llm_probabilisticreasoning.ProbabilisticReasoningProblogStyleLLMAgent("o1")

print(llm_agent.action_loop(bn, evidence, query))


