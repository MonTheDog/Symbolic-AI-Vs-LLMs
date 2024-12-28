# File per esporre le funzioni da utilizzare nel notebook computazionale da consegnare a fine progetto
# (In questo file vi sarà molto copia-incolla di codice dagli altri file, serve solo per venir importato nel
# notebook per evitare codici troppo lunghi che fanno perdere molto spazio)

import knapsack.runner_knapsack as ks
import tic_tac_toe.runner_tic_tac_toe as ttt
import logical_reasoning.runner_logical_reasoning as logic
import probabilistic_reasoning.runner_probabilistic_reasoning as prob
import utils

def knapsack_problem(run_count):
    ks.knapsack_runner(run_count)

def tic_tac_toe(run_count):
    ttt.tic_tac_toe_runner(run_count)

def superhero_family():
    logic.logical_reasoning_runner()

def survey_problem(run_count):
    prob.probabilistic_reasoning_runner(run_count)

def load_openai_key(key):
    utils.openai_key = key

if __name__ == '__main__':
    load_openai_key("")
    #knapsack_problem(1)
    #tic_tac_toe(1)
    superhero_family()
    #survey_problem(1)