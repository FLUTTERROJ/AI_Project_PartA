# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from .core import CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction, PlayerColor
from .utils import render_board
import heapq

'''
define g(n), h(n) and f(n) where f(n) = g(n) + h(n):
g(n): cost from start node to current node
h(n): heuristic estimate from current node to goal
f(n): total estimated cost of the path through n to the goal
'''
    

def heuristic(board: dict[Coord, CellState]) -> int:
    """
    Heuristic function: Calculate the number of blue stacks remaining on the board. 

    Parameters:
    `board`: a dictionary representing the initial board state, mapping
        coordinates to `CellState` instances (each with a `.color` and `.height` attribute).

    Returns:
        The number of blue stacks remaining on the board.
    """

    blue_stacks = 0

    for state in board.values():
        if state.color == PlayerColor.BLUE:
            blue_stacks += 1
    return blue_stacks

def get_legal_actions(board, cord):
    '''
    Checks for all the actions that are possible for the Red stack in that coordinate
    '''

    actions = []
    for direction in Direction:
        target_cord = cord + direction

        if target_cord not in board:
            actions.append(MoveAction(cord, direction))
        elif board[target_cord].color == PlayerColor.BLUE and board[target_cord].height <= board[cord].height:
            actions.append(EatAction(cord, direction))
        else:
            if board[cord].height > 1:
                actions.append(CascadeAction(cord, direction))
    return actions

def apply_action(board, action):
    '''
    Applies the given action to the board and returns the new board state.
    '''
    board = board.copy()
    if isinstance(action, MoveAction):
        source_cord = action.cord
        target_cord = source_cord + action.direction
        board[target_cord] = board[source_cord]
        board[source_cord] = CellState()
    elif isinstance(action, EatAction):
        source_cord = action.cord
        target_cord = source_cord + action.direction
        board[target_cord] = CellState(color=PlayerColor.RED, height=board[source_cord].height)
        board[source_cord] = CellState()
    elif isinstance(action, CascadeAction):
        source_cord = action.cord
        i = 0
        while board[source_cord].height > 0:
            target_cord = source_cord + action.direction * i
            board[target_cord] = CellState(color=PlayerColor.RED, height=1)
            board[source_cord] = CellState(color=PlayerColor.RED, height=board[source_cord].height - 1)
            i += 1
        board[source_cord] = CellState()
    return board
    
def search(
    board: dict[Coord, CellState]
) -> list[Action] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to `CellState` instances (each with a `.color` and
            `.height` attribute).

    Returns:
        A list of actions (MoveAction, EatAction, or CascadeAction), or `None`
        if no solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))
    pq = []
    action_list = []
    
    h_value = heuristic(board)

    initial_node = (h_value, 0, board, [])
    heapq.heappush(pq, initial_node)

    state = frozenset(board.items())
    reached = {state : 0}

    while pq:
        f_value, g_value, board, action_list = heapq.heappop(pq)  
        
        if heuristic(board) == 0:
            return action_list
        
        for cord, state in board.items():
            if state.color == PlayerColor.RED:
                for action in get_legal_actions(board, cord):
                    new_board = apply_action(board, action)
                    state = frozenset(new_board.items())
                    g_value += 1
                    if state not in reached or g_value < reached[state]:
                        reached[state] = g_value
                        h_value = heuristic(new_board)
                        f_value = g_value + h_value
                        heapq.heappush(pq, (f_value, g_value, new_board, action_list + [action]))





    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return action_list if action_list else [
        MoveAction(Coord(3, 3), Direction.Down),
        EatAction(Coord(4, 3), Direction.Down),
        ]

