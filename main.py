from puzzle import N_Puzzle
# from heuristics import Heuristics
from gui import PuzzleGUI
# from utils import solve_puzzle
# import pygame

def main():
    # Create a temporary dummy puzzle object for the menu
    # dummy_puzzle = Puzzle(size=8)  # Default 8-puzzle
    menu_gui = PuzzleGUI(is_menu=True)  # Pass the dummy puzzle
    menu_gui.run()

if __name__ == "__main__":
    main()