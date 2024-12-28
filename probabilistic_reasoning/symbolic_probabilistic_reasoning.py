import problog.logic
from problog.program import PrologString
from problog import get_evaluatable
from problog.tasks import sample
from timeit import default_timer as timer
import utils


def get_true_probability(prolog_string):
    result = get_evaluatable().create_from(prolog_string).evaluate()
    utils.print_probability_dict(result)
    result_dict = dict()
    for key in result.keys():
        result_dict[str(key)] = result[key]
    return result_dict


def get_probability_from_samples(prolog_string, num_samples):
    start = timer()
    sample_list = list(sample.sample(prolog_string, n=num_samples, format='dict'))

    count_dict = dict()

    for s in sample_list:
        for key in s.keys():
            if s[key]:
                count_dict[key] = count_dict.get(key, 0) + 1

    result_dict = dict()

    for key in count_dict.keys():
        result_dict[str(key)] = count_dict[key]/num_samples

    #utils.print_probability_dict(result_dict)
    end = timer()
    time = utils.get_elapsed_time(start, end)
    return result_dict["age(young)"], result_dict["education(uni)"], result_dict["sex(male)"], time


def convert_string_to_problog(network, evidence, queries):
    problog_string = network + evidence + queries
    return PrologString(problog_string)

