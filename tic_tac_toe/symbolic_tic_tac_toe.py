from random import choice
from math import inf
import statistics
from timeit import default_timer as timer
from tic_tac_toe.llm_tic_tac_toe import TicTacToeLLMAgent
from utils import print_elapsed_time

moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
         4: [1, 0], 5: [1, 1], 6: [1, 2],
         7: [2, 0], 8: [2, 1], 9: [2, 2]}

gameboard = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]

llm_invalid_moves = 0

def get_string_gameboard(board):
    """
    Gets the gameboard in string format
    :param board: The current gameboard
    :return: The gameboard in string format
    """
    chars = {1: 'X', -1: 'O', 0: ' '}
    result = '---------------\n'
    for x in board:
        for y in x:
            ch = chars[y]
            result += f'| {ch} |'
        result += '\n---------------\n'
    return result


def print_gameboard(board, agent):
    """
    Prints the current gameboard and turn
    :param board: The gameboard
    :param agent: The agent which has to make a move
    """
    if agent == 1:
        print("=*= LLM Agent Turn (X) =*=")
    else:
        print("=*= Symbolic Agent Turn (O) =*=")
    print(get_string_gameboard(board))


def clear_gameboard(board):
    """
    Resets the current gameboard
    :param board: the gameboard to be reset
    """
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            board[x][y] = 0


def has_agent_won(board, agent):
    """
    Checks if an agent has won the game
    :param board: The current gameboard
    :param agent: The agent to check
    :return: True if agent has won the game, False otherwise
    """
    conditions = [[board[0][0], board[0][1], board[0][2]],
                     [board[1][0], board[1][1], board[1][2]],
                     [board[2][0], board[2][1], board[2][2]],
                     [board[0][0], board[1][0], board[2][0]],
                     [board[0][1], board[1][1], board[2][1]],
                     [board[0][2], board[1][2], board[2][2]],
                     [board[0][0], board[1][1], board[2][2]],
                     [board[0][2], board[1][1], board[2][0]]]

    if [agent, agent, agent] in conditions:
        return True

    return False


def is_game_won(board):
    """
    Checks if the game has been won by one of the two agents
    :param board: The gameboard
    :return: True if one agent has won the game, False otherwise
    """
    return has_agent_won(board, 1) or has_agent_won(board, -1)


def print_result(board):
    """
    Prints the result of the game
    :param board: The gameboard
    :return: 1 if the LLM agent has won the game, -1 if the Symbolic agent has won the game, 0 if the game is a draw
    """
    if has_agent_won(board, 1):
        print('LLM Agent has won this game! ' + '\n')
        return 1
    elif has_agent_won(board, -1):
        print('Symbolic Agent has won this game! ' + '\n')
        return -1
    else:
        print('Draw!' + '\n')
        return 0


def blanks(board):
    """
    Gets the available moves on the board
    :param board: The gameboard
    :return: A list of blank cells, the available moves
    """
    blank = []
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] == 0:
                blank.append([x, y])

    return blank


def is_board_full(board):
    """
    Checks if the board is full, to eventually call a draw
    :param board: The gameboard
    :return: True if board is full, False otherwise
    """
    if len(blanks(board)) == 0:
        return True
    return False


def set_move(board, x, y, agent):
    """
    Sets one of the cells to the given symbol (agent)
    :param board: The gameboard
    :param x: The x coordinate of the cell
    :param y: The y coordinate of the cell
    :param agent: The agent which has made a move
    """
    board[x][y] = agent


def llm_move(board, move, agent, reasoning):
    """
    Executes the LLM agent move
    :param board: The gameboard
    :param move: The move to execute (an integer between 1 and 9)
    :param agent: The llm agent in use
    :param reasoning: The reasoning behind the move
    :return: True if the move is not valid, False otherwise
    """
    global llm_invalid_moves

    # Check if the move is valid
    if move < 1 or move > 9:
        agent.update_conversation("user","Cell is out of range, please try again")
        llm_invalid_moves = llm_invalid_moves + 1
        return True
    elif not (moves[move] in blanks(board)):
        llm_invalid_moves = llm_invalid_moves + 1
        agent.update_conversation("user","Cell is already occupied, please try again")
        return True
    else:
        set_move(board, moves[move][0], moves[move][1], 1)
        print_gameboard(board, 1)
        print("Reasoning: " + reasoning)
        return False


def get_score(board):
    """
    Returns the score of the passed board (those boards are always in a final state)
    :param board: The gameboard
    :return: 10 if the LLM agent has won the game, -10 if the symbolic agent has won the game, 0 if the game is a draw
    """
    if has_agent_won(board, 1):
        return 10

    elif has_agent_won(board, -1):
        return -10

    else:
        return 0


def alphabeta_minimax(board, depth, alpha, beta, agent):
    """
    Runs the minimax algorithm with alphabeta pruning
    :param board: The gameboard (current node of the algorithm)
    :param depth: The depth of the game tree (0 is maximum depth)
    :param alpha: The alpha value
    :param beta: The beta value
    :param agent: The current agent
    :return: A list containing: the x coordinate of the best move, the y coordinate of the best move, the score of the move
    """
    # We set row and col to -1, but we will never use them with those values as those variables
    # get changed during the execution before they get read
    row = -1
    col = -1
    # As the algorithm is recursive this is the stopping condition.
    # If we are at the bottom of the tree (the depth is counted backwards) or if the board is in a winning state
    # we can stop the search of this particular branch of the game tree and return the evaluation function value.
    if depth == 0 or is_game_won(board):
        return [row, col, get_score(board)]
    else:
        # We execute an extensive search on the current game tree (we only search the blank cells)
        for cell in blanks(board):
            # As we need to search the whole game tree, we set the first cell to the current agent symbol (this will be
            # later changed back) and then we go deeper by calling the algorithm recursively. We do this until we reach
            # the stopping condition at the start as the minimax algorithm needs to reach the leaves of the tree.
            set_move(board, cell[0], cell[1], agent)
            score = alphabeta_minimax(board, depth - 1, alpha, beta, -agent)

            # When we evaluate an end state we check who is the current agent, and we update alpha or beta
            # if it is needed. We also save the row and col of the current cell to reset it
            if agent == 1:
                if score[2] > alpha:
                    alpha = score[2]
                    row = cell[0]
                    col = cell[1]

            else:
                if score[2] < beta:
                    beta = score[2]
                    row = cell[0]
                    col = cell[1]

            # Resets the current cell to blank
            set_move(board, cell[0], cell[1], 0)

            # If alpha is greater than or equal to beta, we can stop the search as we can prune the following subtree
            if alpha >= beta:
                break

        # We return the best move for the agent
        if agent == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]


def symbolic_move(board):
    """
    Computes the best move for the symbolic agent
    :param board: The gameboard
    """
    if len(blanks(board)) == 9:
        # If it is the first move, we place the O in a corner as it is the proven best move.
        # Reference to: https://www.youtube.com/watch?v=QNFQvX-MQgI (06:05 mark)
        set_move(board, 0, 0, -1)
        print_gameboard(board, -1)

    else:
        # Get the best move and execute it
        result = alphabeta_minimax(board, len(blanks(board)), -inf, inf, -1)
        set_move(board, result[0], result[1], -1)
        print_gameboard(board, -1)


def get_llm_move(llm_agent, current_turn, string_gameboard):
    """
    Returns the selected move for the llm agent
    :param llm_agent: the agent to be used
    :param current_turn: the current turn
    :param string_gameboard: the gameboard in string form
    :return: The chosen move and the reasoning for that
    """
    return llm_agent.action_loop(current_turn, string_gameboard)


def get_random_move(board):
    """
    Executes a random move
    :param board: the gameboard
    :return: the random move
    """
    chosen_move = 0
    e = True
    while e:
        chosen_move = choice([0,1,2,3,4,5,6,7,8,9])
        if moves[chosen_move] not in blanks(board):
            e = True
        else:
            e = False
    return chosen_move


def make_move(board, current_agent, current_turn, llm_agent):
    """
    Makes the next move and shows the time elapsed
    :param board: The gameboard
    :param current_agent: The current agent
    :param current_turn: the current turn of the game
    :param llm_agent: the llm agent in use
    :return: the elapsed time in milliseconds
    """
    start = timer()
    if current_agent == 1:
        e = True
        while e:
            move, reasoning = get_llm_move(llm_agent, current_turn, get_string_gameboard(board))
            # If the model couldn't answer we execute a random move
            if move == 0:
                move = get_random_move(board)
                reasoning = "Random Move, model couldn't answer"
            e = llm_move(board, move, llm_agent, reasoning)
    else:
        symbolic_move(board)
    end = timer()
    elapsed_time = print_elapsed_time(start, end)

    return elapsed_time


def run_games(games, llm_model):
    """
    Runner function. LLM agent is 1 (X), Symbolic agent is -1 (O)
    :param games: The number of games to play
    :param llm_model: the llm model to use, either "4o" or "o1"
    """
    llm_wins = 0
    symbolic_wins = 0
    draws = 0
    current_turn = 1
    llm_agent_times = []
    symbolic_agent_times = []

    # The first turn of the first game is always for the LLM Agent
    starting_agent = 1
    llm_agent = TicTacToeLLMAgent(llm_model)

    for i in range(games):
        # Reset the board
        clear_gameboard(gameboard)
        current_agent = starting_agent

        # Execute the game
        while not (is_board_full(gameboard) or is_game_won(gameboard)):
            elapsed_time = make_move(gameboard, current_agent, current_turn, llm_agent)
            if current_agent == 1:
                llm_agent_times.append(elapsed_time)
            elif current_agent == -1:
                symbolic_agent_times.append(elapsed_time)
            current_agent *= -1
            current_turn = current_turn + 1

        # Print the result for this game
        result = print_result(gameboard)
        if result == 1:
            llm_wins += 1
        elif result == -1:
            symbolic_wins += 1
        elif result == 0:
            draws += 1

        # Resets the turn count
        current_turn = 1

        # Resets the conversation
        llm_agent.reset_conversation()

        # Change the starting agent in the next game
        starting_agent *= -1

    # Print the result for the test
    print("===== Final Result =====")
    print("LLM Agent " + str(llm_wins) + " - " + str(symbolic_wins) + " Symbolic Agent")
    print("Number of draws: " + str(draws))
    print("Number of invalid moves for the LLM Agent: " + str(llm_invalid_moves))
    print("Average response time for LLM Agent: " + format(statistics.mean(llm_agent_times),".4f") + "ms")
    print("Average response time for Symbolic Agent: " + format(statistics.mean(symbolic_agent_times),".4f") + "ms" + "\n")
    if llm_wins > symbolic_wins:
        print("The winner is... the LLM Agent!")
    elif symbolic_wins > llm_wins:
        print("The winner is... the Symbolic Agent!")
    else:
        print("The winner is... oh... it's a Draw!")