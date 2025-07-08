# from puzzle import N_Puzzle
def misplaced_tiles_heuristic(puzzle):
    """Heuristic: Number of misplaced tiles."""
    misplaced = 0
    for i in range(len(puzzle.state)):
        if puzzle.state[i] != 0 and puzzle.state[i] != puzzle.goal[i]:
            misplaced += 1
    return misplaced

def manhattan_heuristic(puzzle):
    """Heuristic: Sum of Manhattan distances of tiles from their goal positions."""
    distance = 0
    for i in range(len(puzzle.state)):
        if puzzle.state[i] == 0:
            continue
        goal_index = puzzle.goal.index(puzzle.state[i])
        goal_row, goal_col = divmod(goal_index, puzzle.dimension)
        curr_row, curr_col = divmod(i, puzzle.dimension)
        distance += abs(goal_row - curr_row) + abs(goal_col - curr_col)
    return distance

def euclidean_heuristic(puzzle):
    """Heuristic: Sum of Euclidean distances of tiles from their goal positions."""
    distance = 0
    for i in range(len(puzzle.state)):
        if puzzle.state[i] == 0:
            continue
        goal_index = puzzle.goal.index(puzzle.state[i])
        goal_row, goal_col = divmod(goal_index, puzzle.dimension)
        curr_row, curr_col = divmod(i, puzzle.dimension)
        distance += ((goal_row - curr_row) * 2 + (goal_col - curr_col) * 2) ** 0.5
    return distance

def custom_heuristic(puzzle):
    """Heuristic: A custom heuristic (example: sum of row and column distances)."""
    distance = 0
    for i in range(len(puzzle.state)):
        if puzzle.state[i] == 0:
            continue
        goal_index = puzzle.goal.index(puzzle.state[i])
        goal_row, goal_col = divmod(goal_index, puzzle.dimension)
        curr_row, curr_col = divmod(i, puzzle.dimension)
        distance += (abs(goal_row - curr_row) + abs(goal_col - curr_col)) * 2  # Custom formula
    return distance