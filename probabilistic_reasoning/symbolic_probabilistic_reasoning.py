import problog.logic
from problog.program import PrologString
from problog import get_evaluatable
from problog.tasks import sample
from timeit import default_timer as timer
import utils


def get_true_probability(prolog_string):
    start = timer()
    utils.print_probability_dict(get_evaluatable().create_from(prolog_string).evaluate())
    end = timer()
    utils.print_elapsed_time(start, end)


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
        result_dict[key] = count_dict[key]/num_samples

    utils.print_probability_dict(result_dict)
    end = timer()
    utils.print_elapsed_time(start, end)


if __name__ == '__main__':

    p_survey = utils.get_probabilistic_instance()

    get_true_probability(p_survey)

    get_probability_from_samples(p_survey,1000)

