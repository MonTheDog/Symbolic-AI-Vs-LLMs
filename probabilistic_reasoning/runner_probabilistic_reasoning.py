import probabilistic_reasoning.llm_probabilistic_reasoning as llmr
import probabilistic_reasoning.symbolic_probabilistic_reasoning as sr
import utils


def probabilistic_reasoning_runner(run_count):
    network, evidence, queries = utils.get_probabilistic_instance()
    problog_string = sr.convert_string_to_problog(network, evidence, queries)
    llm_4o_agent = llmr.ProbabilisticReasoningProblogStyleLLMAgent("4o")
    llm_o1_agent = llmr.ProbabilisticReasoningProblogStyleLLMAgent("o1")

    print("==================== True Probabilities ====================")
    true_probabilities = sr.get_true_probability(problog_string)

    symbolic_age = []
    symbolic_education = []
    symbolic_sex = []
    symbolic_time = []

    llm_4o_age = []
    llm_4o_education = []
    llm_4o_sex = []
    llm_4o_time = []

    llm_o1_age = []
    llm_o1_education = []
    llm_o1_sex = []
    llm_o1_time = []

    for i in range(0, run_count):
        age, education, sex, time = sr.get_probability_from_samples(problog_string, 100)
        symbolic_age.append(age)
        symbolic_education.append(education)
        symbolic_sex.append(sex)
        symbolic_time.append(time)

        llm_4o_result, time_4o = llm_4o_agent.calculate_probability(network, evidence, queries)
        llm_4o_agent.reset_conversation()
        llm_4o_age.append(llm_4o_result["age(young)"])
        llm_4o_education.append(llm_4o_result["education(uni)"])
        llm_4o_sex.append(llm_4o_result["sex(male)"])
        llm_4o_time.append(time_4o)

        llm_o1_result, time_o1 = llm_o1_agent.calculate_probability(network, evidence, queries)
        llm_o1_agent.reset_conversation()
        llm_o1_age.append(llm_o1_result["age(young)"])
        llm_o1_education.append(llm_o1_result["education(uni)"])
        llm_o1_sex.append(llm_o1_result["sex(male)"])
        llm_o1_time.append(time_o1)

    average_symbolic_age = sum(symbolic_age) / len(symbolic_age)
    average_symbolic_education = sum(symbolic_education) / len(symbolic_education)
    average_symbolic_sex = sum(symbolic_sex) / len(symbolic_sex)
    average_symbolic_time = sum(symbolic_time) / len(symbolic_time)
    distance_symbolic_age = abs(average_symbolic_age - true_probabilities["age(young)"])
    distance_symbolic_education = abs(average_symbolic_education - true_probabilities["education(uni)"])
    distance_symbolic_sex = abs(average_symbolic_sex - true_probabilities["sex(male)"])

    print("==================== Symbolic AI ====================")
    print("age(young): ", str("%.4f" % average_symbolic_age), " Distance from opt: ", str("%.4f" % distance_symbolic_age))
    print("education(uni): ", str("%.4f" % average_symbolic_education), " Distance from opt: ", str("%.4f" % distance_symbolic_education))
    print("sex(male): ", str("%.4f" % average_symbolic_sex), " Distance from opt: ", str("%.4f" % distance_symbolic_sex))
    print("Average Elapsed Time: ", str("%.4f" % average_symbolic_time) + "ms")

    average_llm_4o_age = sum(llm_4o_age) / len(llm_4o_age)
    average_llm_4o_education = sum(llm_4o_education) / len(llm_4o_education)
    average_llm_4o_sex = sum(llm_4o_sex) / len(llm_4o_sex)
    average_llm_4o_time = sum(llm_4o_time) / len(llm_4o_time)
    distance_llm_4o_age = abs(average_llm_4o_age - true_probabilities["age(young)"])
    distance_llm_4o_education = abs(average_llm_4o_education - true_probabilities["education(uni)"])
    distance_llm_4o_sex = abs(average_llm_4o_sex - true_probabilities["sex(male)"])

    print("==================== 4o ====================")
    print("age(young): ", str("%.4f" % average_llm_4o_age), " Distance from opt: ", str("%.4f" % distance_llm_4o_age))
    print("education(uni): ", str("%.4f" % average_llm_4o_education), " Distance from opt: ", str("%.4f" % distance_llm_4o_education))
    print("sex(male): ", str("%.4f" % average_llm_4o_sex), " Distance from opt: ", str("%.4f" % distance_llm_4o_sex))
    print("Average Elapsed Time: ", str("%.4f" % average_llm_4o_time) + "ms")

    average_llm_o1_age = sum(llm_o1_age) / len(llm_o1_age)
    average_llm_o1_education = sum(llm_o1_education) / len(llm_o1_education)
    average_llm_o1_sex = sum(llm_o1_sex) / len(llm_o1_sex)
    average_llm_o1_time = sum(llm_o1_time) / len(llm_o1_time)
    distance_llm_o1_age = abs(average_llm_o1_age - true_probabilities["age(young)"])
    distance_llm_o1_education = abs(average_llm_o1_education - true_probabilities["education(uni)"])
    distance_llm_o1_sex = abs(average_llm_o1_sex - true_probabilities["sex(male)"])

    print("==================== o1 ====================")
    print("age(young): ", str("%.4f" % average_llm_o1_age), " Distance from opt: ", str("%.4f" % distance_llm_o1_age))
    print("education(uni): ", str("%.4f" % average_llm_o1_education), " Distance from opt: ", str("%.4f" % distance_llm_o1_education))
    print("sex(male): ", str("%.4f" % average_llm_o1_sex), " Distance from opt: ", str("%.4f" % distance_llm_o1_sex))
    print("Average Elapsed Time: ", str("%.4f" % average_llm_o1_time) + "ms")


if __name__ == "__main__":
    print("=================================================")
    print("LLMs vs Symbolic AI - Survey Problem")
    print("=================================================")
    print()

    probabilistic_reasoning_runner(2)


