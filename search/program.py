# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from .core import BOARD_N, CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction, PlayerColor
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

def move_stack(cord, direction, board):
    '''
    Moves the stack at the given coordinate to the next coordinate in the given direction, and returns the new board state.
    '''

    current_stack = board[cord]
    try:
        target_cord = cord + direction
        if target_cord in board:
            board = move_stack(target_cord, direction, board)
        board[target_cord] = CellState(color=current_stack.color, height=current_stack.height)
    except ValueError:
        pass
    if cord in board:
        del board[cord]
    return board

def apply_action(board, action):
    '''
    Applies the given action to the board and returns the new board state.
    '''

    board = board.copy()
    if isinstance(action, MoveAction):
        source_cord = action.coord
        target_cord = source_cord + action.direction
        if target_cord in board and board[target_cord].color == PlayerColor.RED:
            old_height = board[target_cord].height
            added_height = board[source_cord].height
            board[target_cord] = CellState(color=PlayerColor.RED, height=old_height + added_height)
        else:
            board[target_cord] = CellState(color=PlayerColor.RED, height=board[source_cord].height)
        del board[source_cord]
    elif isinstance(action, EatAction):
        source_cord = action.coord
        target_cord = source_cord + action.direction
        board[target_cord] = CellState(color=PlayerColor.RED, height=board[source_cord].height)
        del board[source_cord]
    elif isinstance(action, CascadeAction):
        source_cord = action.coord
        curr_cord = source_cord
        height = board[source_cord].height
        for i in range(0, height):
            try:
                target_cord = curr_cord + action.direction
            except ValueError:
                break
            curr_cord = target_cord
            if target_cord in board:
                board = move_stack(target_cord, action.direction, board)
            board[target_cord] = CellState(color=PlayerColor.RED, height=1)
        del board[source_cord]
    return board

def get_legal_actions(board, cord):
    '''
    Checks for all the actions that are possible for the Red stack in that coordinate
    '''

    actions = []
    for direction in Direction:
        try:
            target_cord = cord + direction
        except ValueError:
            continue
        if target_cord not in board or board[target_cord].color == PlayerColor.RED:
            actions.append(MoveAction(cord, direction))
        if target_cord and board[target_cord].color == PlayerColor.BLUE and board[target_cord].height <= board[cord].height:
            actions.append(EatAction(cord, direction))
        if board[cord].height > 1:
            actions.append(CascadeAction(cord, direction))
    return actions

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

    initial_node = (h_value,h_value, 0, 0, board, [])
    heapq.heappush(pq, initial_node)

    board_state = frozenset(board.items())
    reached = {board_state : 0}
    count = 0
    while pq:
        f_value, h_value, _, g_value, curr_board, action_list = heapq.heappop(pq)  
        
        if heuristic(curr_board) == 0:
            return action_list
        
        for cord, state in curr_board.items():
            if state.color == PlayerColor.RED:
                for action in get_legal_actions(curr_board, cord):
                    new_board = apply_action(curr_board, action)
                    board_state = frozenset(new_board.items())
                    new_g = g_value + 1
                    new_h = heuristic(new_board)
                    f_value = new_g + new_h

                    if new_h == 0:
                        return action_list + [action]

                    if board_state not in reached or new_g < reached[board_state]:
                        reached[board_state] = new_g
                        count += 1
                        heapq.heappush(pq, (f_value, new_h, count, new_g, new_board, action_list + [action]))

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return None
'''
MoveAction(Coord(3, 3), Direction.Down),
EatAction(Coord(4, 3), Direction.Down),
'''