"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count == o_count:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions: set[tuple[int, int]] = set()

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board: list[list[str | None]] = copy.deepcopy(board)

    try:
        i, j = action
        new_board[i][j] = player(board)
    except:
        raise Exception("Action not valid")

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def lines(board: list[list[str | None]]):
        """
        Generator for all rows, columns, and diagonals.
        """
        for row in board:
            yield row

        for col in ([row[col_idx] for row in board] for col_idx in range(3)):
            yield col

        # Yields diagonals
        yield [board[i][i] for i in range(3)]
        yield [board[i][(i * -1) - 1] for i in range(3)]


    for line in lines(board):
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If no empty spaces
    if not any(EMPTY in row for row in board):
        return True
    return bool(winner(board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    user = winner(board)

    if user == X:
        return 1
    if user == O:
        return -1
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def min_max_value(board):
        """
        Returns the min/max value using a board that results from an action.
        """
        if terminal(board):
            return utility(board)

        user_val = 1 if player(board) == X else -1

        optimal_action_val = user_val * -1
        for action in actions(board):
            action_val = min_max_value(result(board, action))

            if action_val == user_val:
                return action_val
            if optimal_action_val != 0:
                optimal_action_val = action_val

        return optimal_action_val


    if terminal(board):
        return None

    user_val = 1 if player(board) == X else -1

    optimal_action: tuple[int, int] = ()
    for action in actions(board):
        action_val = min_max_value(result(board, action))

        if action_val == user_val:
            return action
        if action_val == 0:
            optimal_action = action

    return optimal_action
