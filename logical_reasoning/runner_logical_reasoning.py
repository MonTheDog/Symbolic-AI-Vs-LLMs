import logical_reasoning.llm_logical_reasoning as llml
import logical_reasoning.symbolic_logical_reasoning as sl
import utils

def logical_reasoning_runner():
    prolog_script = utils.get_logic_instance()
    knowledge_base = sl.get_knowledge_base(prolog_script)

    queries = utils.get_logic_queries()
    request_query = ""
    for query in queries:
        request_query += query + ".\n"

    llm_4o_agent = llml.LogicalReasoningPrologStyleLLMAgent("4o")
    llm_o1_agent = llml.LogicalReasoningPrologStyleLLMAgent("o1")


    print("==================== Symbolic AI ====================")
    sl.solve_logic_problem(knowledge_base)

    print("========================= 4o =========================")
    llm_4o_agent.solve_logical_problem(prolog_script, request_query)

    print("========================= o1 =========================")
    llm_o1_agent.solve_logical_problem(prolog_script, request_query)



if __name__ == "__main__":
    print("=================================================")
    print("LLMs vs Symbolic AI - Superhero Family")
    print("=================================================")
    print()

    logical_reasoning_runner()
