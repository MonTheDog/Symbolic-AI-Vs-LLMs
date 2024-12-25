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

    p_cancer = PrologString("""
    0.90::pollution(high); 0.10::pollution(low).
    0.30::smoker(yes); 0.70::smoker(no).
    
    0.05::cancer(yes) :- pollution(high), smoker(yes).
    0.02::cancer(yes) :- pollution(high), smoker(no).
    0.03::cancer(yes) :- pollution(low), smoker(yes).
    0.001::cancer(yes) :- pollution(low), smoker(no).
    
    0.95::cancer(no) :- pollution(high), smoker(yes).
    0.98::cancer(no) :- pollution(high), smoker(no).
    0.97::cancer(no) :- pollution(low), smoker(yes).
    0.999::cancer(no) :- pollution(low), smoker(no).
    
    0.90::xray(yes) :- cancer(yes).
    0.20::xray(yes) :- cancer(no).
    
    0.10::xray(no) :- cancer(yes).
    0.80::xray(no) :- cancer(no).
    
    0.65::dyspnoea(yes) :- cancer(yes).
    0.30::dyspnoea(yes) :- cancer(no).
    
    0.35::dyspnoea(no) :- cancer(yes).
    0.70::dyspnoea(no) :- cancer(no).
    
    query(xray(yes)).
    query(dyspnoea(yes)).
    
    query(xray(no)).
    query(dyspnoea(no)).
    """)

    p_earthquake = PrologString("""
    0.01::burglary(yes); 0.99::burglary(no).
    
    0.02::earthquake(yes); 0.98::earthquake(no).
    
    0.95::alarm(yes) :- burglary(yes), earthquake(yes).
    0.29::alarm(yes) :- burglary(no), earthquake(yes).
    0.94::alarm(yes) :- burglary(yes), earthquake(no).
    0.001::alarm(yes) :- burglary(no), earthquake(no).
    
    0.05::alarm(no) :- burglary(yes), earthquake(yes).
    0.71::alarm(no) :- burglary(no), earthquake(yes).
    0.06::alarm(no) :- burglary(yes), earthquake(no).
    0.999::alarm(no) :- burglary(no), earthquake(no).
    
    0.90::johncalls(yes) :- alarm(yes).
    0.05::johncalls(yes) :- alarm(no).
    
    0.10::johncalls(no) :- alarm(yes).
    0.95::johncalls(no) :- alarm(no).
    
    0.70::marycalls(yes) :- alarm(yes).
    0.01::marycalls(yes) :- alarm(no).
    
    0.30::marycalls(no) :- alarm(yes).
    0.99::marycalls(no) :- alarm(no).
    
    query(johncalls(yes)).
    query(marycalls(yes)).
    
    query(johncalls(no)).
    query(marycalls(no)).
    """)

    p_survey = PrologString("""
    0.3::age(young); 0.5::age(adult); 0.2::age(old).
    
    0.6::sex(male); 0.4::sex(female).
    
    0.75::education(high) :- age(young), sex(male).
    0.72::education(high) :- age(adult), sex(male).
    0.88::education(high) :- age(old), sex(male).
    0.64::education(high) :- age(young), sex(female).
    0.70::education(high) :- age(adult), sex(female).
    0.90::education(high) :- age(old), sex(female).
    
    0.25::education(uni) :- age(young), sex(male).
    0.28::education(uni) :- age(adult), sex(male).
    0.12::education(uni) :- age(old), sex(male).
    0.36::education(uni) :- age(young), sex(female).
    0.30::education(uni) :- age(adult), sex(female).
    0.10::education(uni) :- age(old), sex(female).
    
    0.96::occupation(employed) :- education(high).
    0.92::occupation(employed) :- education(uni).
    
    0.04::occupation(self) :- education(high).
    0.08::occupation(self) :- education(uni).
    
    0.25::rent(small) :- education(high).
    0.20::rent(small) :- education(uni).
    
    0.75::rent(big) :- education(high).
    0.80::rent(big) :- education(uni).
    
    0.48::transport(car) :- occupation(employed), rent(small).
    0.56::transport(car) :- occupation(self), rent(small).
    0.58::transport(car) :- occupation(employed), rent(big).
    0.70::transport(car) :- occupation(self), rent(big).
    
    0.42::transport(train) :- occupation(employed), rent(small).
    0.36::transport(train) :- occupation(self), rent(small).
    0.24::transport(train) :- occupation(employed), rent(big).
    0.21::transport(train) :- occupation(self), rent(big).

    0.10::transport(other) :- occupation(employed), rent(small).
    0.08::transport(other) :- occupation(self), rent(small).
    0.18::transport(other) :- occupation(employed), rent(big).
    0.09::transport(other) :- occupation(self), rent(big).
    
    evidence(transport(car)).
    
    query(sex(male)).
    """)

    get_true_probability(p_survey)

    get_probability_from_samples(p_survey,1000)

