import logical_reasoning.llm_logical_reasoning as llml
import logical_reasoning.symbolic_logical_reasoning as sl
import utils

def logical_reasoning_runner(run_count):
    """
    The runner for the logical reasoning problem
    :param run_count: The number of runs for this problem
    """
    prolog_script = utils.get_logic_instance()
    knowledge_base = sl.get_knowledge_base(prolog_script)

    queries = utils.get_logic_queries()
    request_query = ""
    for query in queries:
        request_query += query + ".\n"

    llm_4o_agent = llml.LogicalReasoningPrologStyleLLMAgent("4o")
    llm_o1_agent = llml.LogicalReasoningPrologStyleLLMAgent("o1")

    time_symbolic = []

    matching_cases_4o = []
    mismatch_cases_4o = []
    missing_cases_4o = []
    added_cases_4o = []
    invalid_cases_4o = []
    time_4o = []

    matching_cases_o1 = []
    mismatch_cases_o1 = []
    missing_cases_o1 = []
    added_cases_o1 = []
    invalid_cases_o1 = []
    time_o1 = []

    for i in range(0, run_count):

        logic_result, symbolic_time = sl.solve_logic_problem(knowledge_base)
        time_symbolic.append(symbolic_time)

        llm_4o_result, llm_4o_time = llm_4o_agent.solve_logical_problem(prolog_script, request_query)
        llm_4o_agent.reset_conversation()

        matching_cases, mismatching_cases, missing_cases, added_cases, invalid_cases = utils.evaluate_llm_responses_logical_reasoning(logic_result, llm_4o_result)
        matching_cases_4o.append(matching_cases)
        mismatch_cases_4o.append(mismatching_cases)
        missing_cases_4o.append(missing_cases)
        added_cases_4o.append(added_cases)
        invalid_cases_4o.append(invalid_cases)
        time_4o.append(llm_4o_time)

        llm_o1_result, llm_o1_time = llm_o1_agent.solve_logical_problem(prolog_script, request_query)
        llm_o1_agent.reset_conversation()

        matching_cases, mismatching_cases, missing_cases, added_cases, invalid_cases = utils.evaluate_llm_responses_logical_reasoning(logic_result, llm_o1_result)
        matching_cases_o1.append(matching_cases)
        mismatch_cases_o1.append(mismatching_cases)
        missing_cases_o1.append(missing_cases)
        added_cases_o1.append(added_cases)
        invalid_cases_o1.append(invalid_cases)
        time_o1.append(llm_o1_time)

    average_symbolic_time = sum(time_symbolic) / len(time_symbolic)

    average_matching_cases_4o = sum(matching_cases_4o) / len(matching_cases_4o)
    average_mismatch_cases_4o = sum(mismatch_cases_4o) / len(mismatch_cases_4o)
    average_missing_cases_4o = sum(missing_cases_4o) / len(missing_cases_4o)
    average_added_cases_4o = sum(added_cases_4o) / len(added_cases_4o)
    average_invalid_cases_4o = sum(invalid_cases_4o) / len(invalid_cases_4o)
    average_time_4o = sum(time_4o) / len(time_4o)

    average_matching_cases_o1 = sum(matching_cases_o1) / len(matching_cases_o1)
    average_mismatch_cases_o1 = sum(mismatch_cases_o1) / len(mismatch_cases_o1)
    average_missing_cases_o1 = sum(missing_cases_o1) / len(missing_cases_o1)
    average_added_cases_o1 = sum(added_cases_o1) / len(added_cases_o1)
    average_invalid_cases_o1 = sum(invalid_cases_o1) / len(invalid_cases_o1)
    average_time_o1 = sum(time_o1) / len(time_o1)

    print("========================= Symbolic AI =========================")
    print("Average Elapsed Time: ", str("%.4f" % average_symbolic_time) + "ms")

    print("========================= 4o =========================")
    print("Average Matching Cases: ", str("%.2f" % average_matching_cases_4o))
    print("Average Mismatching Cases: ", str("%.2f" % average_mismatch_cases_4o))
    print("Average Missing Cases: ", str("%.2f" % average_missing_cases_4o))
    print("Average Added Cases: ", str("%.2f" % average_added_cases_4o))
    print("Average Invalid Cases: ", str("%.2f" % average_invalid_cases_4o))
    print("Average Elapsed Time: ", str("%.4f" % average_time_4o) + "ms")

    print("========================= o1 =========================")
    print("Average Matching Cases: ", str("%.2f" % average_matching_cases_o1))
    print("Average Mismatching Cases: ", str("%.2f" % average_mismatch_cases_o1))
    print("Average Missing Cases: ", str("%.2f" % average_missing_cases_o1))
    print("Average Added Cases: ", str("%.2f" % average_added_cases_o1))
    print("Average Invalid Cases: ", str("%.2f" % average_invalid_cases_o1))
    print("Average Elapsed Time: ", str("%.4f" % average_time_o1) + "ms")

if __name__ == "__main__":
    print("=================================================")
    print("LLMs vs Symbolic AI - Superhero Family")
    print("=================================================")
    print()

    logical_reasoning_runner(2)
