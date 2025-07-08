import random
import time
from heuristics import manhattan_heuristic, misplaced_tiles_heuristic, euclidean_heuristic, custom_heuristic
from heapq import heappop, heappush

from puzzle import N_Puzzle

# Function to check if the puzzle is solvable
def is_solvable(state, dimension):
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                inversions += 1
    return inversions % 2 == 0

# Function to generate the goal state for any given puzzle size
def generate_goal_state(size):
    goal_state = list(range(1, size)) + [0]  # 0 represents the empty space
    return goal_state

# Function to shuffle the puzzle randomly
def generate_random_state(size):
    state = generate_goal_state(size)
    random.shuffle(state)
    while not is_solvable(state, int(len(state)**0.5)):  # Ensure the shuffled state is solvable
        random.shuffle(state)
    return state

# Function to solve the puzzle using a given heuristic
# def solve_puzzle(puzzle, heuristic):
#     start_time = time.time()
#     # Perform A* search or any other search algorithm (Best-First, etc.)
#     # Here we'll assume you have a function like A* search that uses the heuristic
#     moves, solved_state = a_star_search(puzzle, heuristic, puzzle.dimension)
#     end_time = time.time()
    
#     time_taken = end_time - start_time
#     return time_taken, len(moves)

def solve_puzzle(puzzle, heuristic):
    if puzzle is None:
        raise ValueError("puzzle not initialized")
    start_time = time.time()
    moves, solved_state = bestFirstSearch(puzzle, heuristic)
    end_time = time.time()

    time_taken = end_time - start_time
    num_moves = len(moves) if moves else 0  # If no solution, moves = 0
    return time_taken, num_moves

# A* search algorithm (simplified version, assuming you have a working implementation)
# def bestFirstSearch(puzzle, heuristic):
#     """
#     Perform Best-First Search to solve the N-Puzzle.
    
#     Parameters:
#         puzzle: The N_Puzzle instance.
#         heuristic: A function that estimates the cost to the goal (e.g., misplaced tiles, Manhattan distance).
    
#     Returns:
#         moves: A list of moves to reach the goal state.
#         solved_state: The final solved state (goal).
#     """
#     start_state = puzzle.state
#     goal_state = puzzle.goal
#     dimension = puzzle.dimension

#     # Priority queue for open list (stores: h_score, state, parent, move)
#     open_list = []
    

#     # Push the initial state into the open list
#     heappush(open_list, (heuristic(start_state), start_state, None, None))  # (h, state, parent, move)

#     closed_set = set()
#     # Map to reconstruct the path
#     came_from = {}

#     while open_list:
#         _, current_h, current_state, parent_state, move = heappop(open_list)

#         # Goal check
#         if current_state == goal_state:
#             return reconstruct_path(came_from, current_state), current_state

#         closed_set.add(tuple(current_state))

#         # Process neighbors
#         neighbors = generate_successors(current_state, dimension)
#         for neighbor_state, move in neighbors:
#             if tuple(neighbor_state) in closed_set:
#                 continue

#             if not any(neighbor_state == item[1] for item in open_list):
#                 heappush(open_list, (heuristic(N_Puzzle.from_state(neighbor_state, goal_state)), neighbor_state, current_state, move))
#                 came_from[tuple(neighbor_state)] = (parent_state, move)

#     raise ValueError("No solution found.")  # If the goal is not reachable

def bestFirstSearch(puzzle, heuristic):
    """
    Perform Best-First Search to solve the puzzle.
    Args:
        puzzle: An instance of the N_Puzzle class.
        heuristic: A heuristic function to evaluate states.
    Returns:
        moves (list): A list of moves to solve the puzzle.
        current_state: The final solved state.
    """
    start_state = puzzle.state  # Initial state of the puzzle
    goal_state = puzzle.goal  # Goal state of the puzzle
    dimension = puzzle.dimension  # Dimension of the puzzle

    # Priority queue (open list) initialized with the starting state
    open_list = []
    heappush(open_list, (heuristic(puzzle), start_state, None, None))  # (priority, state, parent, move)

    # Explored states (closed list)
    closed_list = set()

    # Stores parent-child relationships for reconstructing the solution
    parent_map = {}

    start_time = time.time()

    while open_list:
        # Get the state with the lowest heuristic value
        _, current_state, parent_state, move = heappop(open_list)
        current_state_tuple= tuple(current_state)

        # If we reach the goal state, reconstruct the solution
        if current_state == goal_state:
            end_time = time.time()
            moves = []
            while current_state_tuple in parent_map:
                current_state_tuple, move = parent_map[current_state_tuple]
                moves.append(move)
            moves.reverse()  # Reverse to get moves in the correct order
            return moves, (end_time - start_time)

        # Add the current state to the closed list
        closed_list.add(current_state_tuple)

        # Generate successors (neighbors)
        neighbors = generate_successors(current_state, dimension)

        for neighbor_state, move in neighbors:
            neighbor_state_tuple= tuple(neighbor_state)
            if neighbor_state_tuple not in closed_list:
                parent_map[neighbor_state_tuple] = (current_state_tuple, move)
                heappush(open_list, (heuristic(puzzle), neighbor_state, current_state, move))

    raise ValueError("No solution found!")

def reconstruct_path(came_from, current_state):
    total_path = [current_state]
    while current_state in came_from:
        current_state = came_from[current_state]
        total_path.append(current_state)
    total_path.reverse()
    return total_path[1:], total_path[-1]  # Return the path and the solved state

def generate_successors(state, dimension):
    """
    Generate all possible successors of the current state.
    
    Parameters:
        state (list): The current state of the puzzle (1D list).
        dimension (int): The dimension of the puzzle (e.g., 3 for 8-puzzle).
    
    Returns:
        List[Tuple[List[int], str]]: A list of tuples, where each tuple contains
                                     a new state (1D list) and the move as a string.
    """
    successors = []
    zero_index = state.index(0)  # Find the blank space (0)

    # Define possible moves (row_offset, col_offset, move_name)
    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    # Convert 1D index to 2D row and column
    row, col = divmod(zero_index, dimension)

    for move, (row_offset, col_offset) in moves.items():
        new_row, new_col = row + row_offset, col + col_offset

        # Check if the move is within bounds
        if 0 <= new_row < dimension and 0 <= new_col < dimension:
            # Calculate new 1D index for the blank space
            new_zero_index = new_row * dimension + new_col

            # Swap the blank space with the target tile to create a new state
            new_state = state[:]
            new_state[zero_index], new_state[new_zero_index] = new_state[new_zero_index], new_state[zero_index]

            # Append the new state and the move to successors
            successors.append((new_state, move))

    return successors

