# File per implementare l'agente che utilizza minmax e alfabeta pruning per il tris
from random import choice
from math import inf

board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Prints the current gameboard and turn
def gameboard(board, player):
    chars = {1: 'X', -1: 'O', 0: ' '}
    if player == 1:
        print("=*= LLM Agent Turn (X) =*=")
    else:
        print("=*= Symbolic Agent Turn (O) =*=")
    print('---------------')
    for x in board:
        for y in x:
            ch = chars[y]
            print(f'| {ch} |', end='')
        print('\n' + '---------------')

# Resets the gameboard
def clearboard(board):
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            board[x][y] = 0

# Checks if a player has won the game
def winningPlayer(board, player):
    conditions = [[board[0][0], board[0][1], board[0][2]],
                     [board[1][0], board[1][1], board[1][2]],
                     [board[2][0], board[2][1], board[2][2]],
                     [board[0][0], board[1][0], board[2][0]],
                     [board[0][1], board[1][1], board[2][1]],
                     [board[0][2], board[1][2], board[2][2]],
                     [board[0][0], board[1][1], board[2][2]],
                     [board[0][2], board[1][1], board[2][0]]]

    if [player, player, player] in conditions:
        return True

    return False

# Checks if the game has been won by one of the two agents
def gameWon(board):
    return winningPlayer(board, 1) or winningPlayer(board, -1)

# Prints the winning agent
def printResult(board):
    if winningPlayer(board, 1):
        print('LLM Agent has won this game! ' + '\n')
        return 1
    elif winningPlayer(board, -1):
        print('Symbolic Agent has won this game! ' + '\n')
        return -1
    else:
        print('Draw!' + '\n')

# Gets the available moves on the board
def blanks(board):
    blank = []
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] == 0:
                blank.append([x, y])

    return blank

# Checks if the board is full, to eventually call a draw
def boardFull(board):
    if len(blanks(board)) == 0:
        return True
    return False

# Sets one of the cells to the given symbol (player)
def setMove(board, x, y, player):
    board[x][y] = player

# Executes the LLM Move
def LLMMove(board, move):
    moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
             4: [1, 0], 5: [1, 1], 6: [1, 2],
             7: [2, 0], 8: [2, 1], 9: [2, 2]}

    # Check if the move is valid
    if move < 1 or move > 9:
        # TODO: Tell the LLM to retry
        return True
    elif not (moves[move] in blanks(board)):
        # TODO: Tell the LLM to retry
        return True
    else:
        setMove(board, moves[move][0], moves[move][1], 1)
        gameboard(board, 1)
        return False

# Returns the score of the passed board. Those boards are always in a final state, so if
# player 1 (X) won, we return 10, if player 2 (O) won we return -10 or if it's a draw we return 0
def getScore(board):
    if winningPlayer(board, 1):
        return 10

    elif winningPlayer(board, -1):
        return -10

    else:
        return 0

# Runs the minimax algorithm with alphabeta pruning
def abminimax(board, depth, alpha, beta, player):
    # We set row and col to -1, but we will never use them with those values as those variables
    # get changed during the execution before they get read
    row = -1
    col = -1
    # As the algorithm is recursive this is the stopping condition.
    # If we are at the bottom of the tree (the depth is counted backwards) or if the board is in a winning state
    # we can stop the search of this particular branch of the game tree and return the evaluation function value.
    if depth == 0 or gameWon(board):
        return [row, col, getScore(board)]
    else:
        # We execute an extensive search on the current game tree (we only search the blank cells)
        for cell in blanks(board):
            # As we need to search the whole game tree, we set the first cell to the current player symbol (this will be
            # later changed back) and then we go deeper by calling the algorithm recursively. We do this until we reach
            # the stopping condition at the start as the minimax algorithm needs to reach the leaves of the tree.
            setMove(board, cell[0], cell[1], player)
            score = abminimax(board, depth - 1, alpha, beta, -player)

            # When we evaluate an end state we check who is the current player, and we update alpha or beta
            # if it is needed. We also save the row and col of the current cell to reset it
            if player == 1:
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
            setMove(board, cell[0], cell[1], 0)

            # If alpha is greater than or equal to beta, we can stop the search as we can prune the following subtree
            if alpha >= beta:
                break

        # We return the best move for the player
        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]

# Computes the best move for the symbolic agent
def symbolicMove(board):
    if len(blanks(board)) == 9:
        # If it is the first move, we place the O in a corner as it is the proven best move.
        # Reference to: https://www.youtube.com/watch?v=QNFQvX-MQgI (06:05 mark)
        setMove(board, 0, 0, -1)
        gameboard(board, -1)

    else:
        # Get the best move and execute it
        result = abminimax(board, len(blanks(board)), -inf, inf, -1)
        setMove(board, result[0], result[1], -1)
        gameboard(board, -1)

# TODO: Mock method, to be changed to the LLM logic (right now it's a random move)
def getLLMMove():
    return choice([1, 2, 3, 4, 5, 6, 7, 8, 9])

# TODO: Adapt to LLM when the Mock is removed
# Makes the next move
def makeMove(board, player):
    if player == 1:
        e = True
        while e:
            move = getLLMMove()
            e = LLMMove(board, move)
    else:
        symbolicMove(board)


# Runner function. LLM agent is 1 (X), Symbolic agent is -1 (O)
def runGames(games):
    LLMWins = 0
    symbolicWins = 0

    # The first turn of the first game is always for the LLM Agent
    currentPlayer = 1

    for i in range(games):
        # Reset the board
        clearboard(board)

        # Execute the game
        while not (boardFull(board) or gameWon(board)):
            makeMove(board, currentPlayer)
            currentPlayer *= -1

        # Print the result for this game
        result = printResult(board)
        if result == 1:
            LLMWins += 1
        else:
            symbolicWins += 1

        # Change the first player in the next game
        currentPlayer *= -1

    # Print the result for the test
    print("===== Final Result =====")
    print("LLM Agent " + str(LLMWins) + " - " + str(symbolicWins) + " Symbolic Agent" + "\n")
    if LLMWins > symbolicWins:
        print("The winner is... the LLM Agent!")
    elif symbolicWins > LLMWins:
        print("The winner is... the Symbolic Agent!")
    else:
        print("The winner is... oh... it's a Draw!")