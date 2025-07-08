import random
from heuristics import manhattan_heuristic, misplaced_tiles_heuristic, euclidean_heuristic, custom_heuristic
from time import time


class N_Puzzle:
    def __init__(self, size=3, state=None, goal=None):
        self.size = size
        self.dimension = size
        # self.state = self.generate_random_state()
        # self.goal = self.generate_goal_state()
        self.state = state if state else self.generate_random_state()
        self.goal = goal if goal else self.generate_goal_state()

    def generate_random_state(self):
        """Generate a random puzzle state."""
        state = list(range(self.dimension*self.dimension))
        random.shuffle(state)
        while not self.is_solvable(state):
            random.shuffle(state)
        return state

    def generate_goal_state(self):
        """Generate the goal state."""
        goal= list(range(1, self.dimension*self.dimension)) + [0]
        return goal
    
    def move(self, direction):
        """Move the blank tile (0) in the specified direction."""
        zero_index = self.state.index(0)
        row, col = divmod(zero_index, self.dimension)
        if direction == "up" and row > 0:
            swap_index = zero_index - self.dimension
        elif direction == "down" and row < self.dimension - 1:
            swap_index = zero_index + self.dimension
        elif direction == "left" and col > 0:
            swap_index = zero_index - 1
        elif direction == "right" and col < self.dimension - 1:
            swap_index = zero_index + 1
        else:
            return False
        self.state[zero_index], self.state[swap_index] = self.state[swap_index], self.state[zero_index]
        return True

    def is_goal(self):
        """Check if the current state matches the goal state."""
        return self.state == list(range(1, self.dimension * self.dimension)) + [0]

    def get_possible_moves(self):
        """Get all possible moves for the blank tile (0)."""
        zero_index = self.state.index(0)
        row, col = divmod(zero_index, self.dimension)
        moves = []
        if row > 0: moves.append("up")
        if row < self.dimension - 1: moves.append("down")
        if col > 0: moves.append("left")
        if col < self.dimension - 1: moves.append("right")
        return moves

    def is_solvable(self, state):
        """Check if the given state is solvable."""
        inversions = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inversions += 1
        if self.dimension % 2 == 1:
            return inversions % 2 == 0
        zero_row = self.dimension - (state.index(0) // self.dimension)
        return (inversions + zero_row) % 2 == 0
    
    def from_state(cls, state, goal):
        """
        Create an N_Puzzle instance from a given state and goal.

        Parameters:
            state (list): The current state of the puzzle as a 1D list.
            goal (list): The goal state of the puzzle as a 1D list.

        Returns:
            N_Puzzle: A new puzzle instance with the provided state and goal.
        """
        dimension = int(len(state) ** 0.5)  # Calculate dimension from the state
        return cls(dimension, state=state, goal=goal)

    # def solve_with_heuristic(self, heuristic_name):
    #     """
    #     Solve the puzzle using the specified heuristic.

    #     Args:
    #         heuristic_name (str): Name of the heuristic to use.

    #     Returns:
    #         int: The number of moves to solve the puzzle.
    #     """
    #     heuristics = Heuristics(self.dimension)
    #     open_set = [(heuristics.evaluate(self.state, heuristic_name), self.state, 0)]  # (f_score, state, g_score)
    #     closed_set = set()

    #     while open_set:
    #         open_set.sort()  # Sort by f_score (lowest first)
    #         _, current_state, g_score = open_set.pop(0)

    #         if current_state == self.goal_state:
    #             return g_score  # Return the number of moves (g_score)

    #         closed_set.add(tuple(current_state))

    #         zero_index = current_state.index(0)
    #         row, col = divmod(zero_index, self.dimension)
    #         moves = self.get_possible_moves()

    #         for move in moves:
    #             new_state = current_state[:]
    #             if move == "up":
    #                 swap_index = zero_index - self.dimension
    #             elif move == "down":
    #                 swap_index = zero_index + self.dimension
    #             elif move == "left":
    #                 swap_index = zero_index - 1
    #             elif move == "right":
    #                 swap_index = zero_index + 1

    #             # Swap tiles
    #             new_state[zero_index], new_state[swap_index] = new_state[swap_index], new_state[zero_index]

    #             if tuple(new_state) in closed_set:
    #                 continue

    #             h_score = heuristics.evaluate(new_state, heuristic_name)
    #             f_score = g_score + 1 + h_score
    #             open_set.append((f_score, new_state, g_score + 1))

    #     return -1  # Return -1 if no solution is found

