import llm_probabilistic_reasoning as llmr
import symbolic_probabilistic_reasoning as sr
import utils

print("=================================================")
print("LLMs vs Symbolic AI - Survey Problem")
print("=================================================")

network, evidence, queries = utils.get_probabilistic_instance()
problog_string = sr.convert_string_to_problog(network, evidence, queries)
llm_agent = llmr.ProbabilisticReasoningProblogStyleLLMAgent("o1")

print("True Probabilities: ")
sr.get_true_probability(problog_string)
print()

print("Sampled Probabilities: ")
sr.get_probability_from_samples(problog_string, 100)
print()

print("LLM Probabilities: ")
llm_agent.calculate_probability(network, evidence, queries)


