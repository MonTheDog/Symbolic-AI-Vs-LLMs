import tic_tac_toe.symbolic_tic_tac_toe as sttt

def tic_tac_toe_runner(run_count):
    sttt.run_games(run_count, "4o")
    sttt.run_games(run_count, "o1")

if __name__ == "__main__":
    print("=================================================")
    print("LLMs vs Symbolic AI - Tic Tac Toe")
    print("=================================================")
    print()

    tic_tac_toe_runner(1)