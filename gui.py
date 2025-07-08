import pygame
from time import time
from puzzle import N_Puzzle
import puzzle
from utils import solve_puzzle
from heuristics import manhattan_heuristic, misplaced_tiles_heuristic, euclidean_heuristic, custom_heuristic

class PuzzleGUI:
    def __init__(self, puzzle=None, is_menu=False):
        pygame.init()
        self.width = 600
        self.height = 700
        self.tile_size = 100
        self.margin = 5

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("N-Puzzle")
        self.font = pygame.font.Font(None, 50)

        self.puzzle = puzzle
        self.is_menu = is_menu
        self.is_choosing_heuristic = False  # Add this line
        self.running = True

        if not self.is_menu and self.puzzle is None:
            raise ValueError("A valid puzzle object must be provided if is_menu is False.")
    def draw_menu(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))  # White background

        # Draw the title
        title_text = self.font.render("N-Puzzle", True, (0, 0, 0))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # Draw "Play Manually" button
        play_manually_rect = pygame.Rect(100, 250, 400, 100)
        pygame.draw.rect(self.screen, (0, 128, 255), play_manually_rect)
        play_manually_text = self.font.render("Play Manually", True, (255, 255, 255))
        self.screen.blit(play_manually_text, (play_manually_rect.centerx - play_manually_text.get_width() // 2, play_manually_rect.centery - play_manually_text.get_height() // 2))

        # Draw "Solve Automatically" button
        solve_auto_rect = pygame.Rect(100, 400, 400, 100)
        pygame.draw.rect(self.screen, (0, 128, 0), solve_auto_rect)
        solve_auto_text = self.font.render("Solve Automatically", True, (255, 255, 255))
        self.screen.blit(solve_auto_text, (solve_auto_rect.centerx - solve_auto_text.get_width() // 2, solve_auto_rect.centery - solve_auto_text.get_height() // 2))
        
        pygame.display.update()

    def draw_puzzle(self):
        self.screen.fill((255, 255, 255))  # Clear the screen
        for i, tile in enumerate(self.puzzle.state):
            if tile == 0:  # Skip the blank tile
                continue
            row, col = divmod(i, self.puzzle.dimension)
            x = col * (self.tile_size + self.margin) + self.margin
            y = row * (self.tile_size + self.margin) + self.margin
            pygame.draw.rect(self.screen, (0, 0, 255), (x, y, self.tile_size, self.tile_size))
            text = self.font.render(str(tile), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
            self.screen.blit(text, text_rect)
        pygame.display.update()

    def handle_click(self, mouse_pos):
        """Handle mouse click events for moving tiles."""
        col, row = mouse_pos[0] // (self.tile_size + self.margin), mouse_pos[1] // (self.tile_size + self.margin)
        clicked_index = row * self.dimension + col

        zero_index = self.puzzle.state.index(0)
        possible_moves = self.puzzle.get_possible_moves()

        if clicked_index == zero_index - self.dimension and "up" in possible_moves:
            self.puzzle.move("up")
        elif clicked_index == zero_index + self.dimension and "down" in possible_moves:
            self.puzzle.move("down")
        elif clicked_index == zero_index - 1 and "left" in possible_moves:
            self.puzzle.move("left")
        elif clicked_index == zero_index + 1 and "right" in possible_moves:
            self.puzzle.move("right")
        if self.puzzle.is_goal():
            self.display_success_message()

    def run(self):
        """Run the main loop of the GUI."""
        running = True
        while running:
            if not pygame.get_init():  # Check if Pygame is initialized
                break

            self.screen.fill((255, 255, 255))  # Clear screen

            if self.is_menu:
                self.draw_menu()
            elif self.is_choosing_heuristic:
                self.choose_heuristic()  # Heuristic selection screen
            else:
                self.draw_puzzle()  # Puzzle screen

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.is_menu:  # In the menu screen
                        # Play Manually button
                        if 250 < y < 350:  # Play Manually button area
                            self.is_menu = False
                            puzzle = N_Puzzle(size=3)  # Create a new puzzle (size 3 for 8-puzzle)
                            self.puzzle = puzzle
                            self.dimension = puzzle.dimension
                        # Solve Automatically button
                        elif 400 < y < 500:  # Solve Automatically button area
                            self.is_menu = False
                            self.is_choosing_heuristic = True  # Show heuristic selection screen
                    elif self.is_choosing_heuristic:  # Handle clicks on the heuristic selection screen
                        heuristics = ["Misplaced Tiles", "Manhattan Distance", "Linear Conflict", "Euclidean Distance"]

                        for i, heuristic in enumerate(heuristics):
                            if 150 + i * 50 < y < 200 + i * 50:  # Check if a heuristic button is clicked
                                self.selected_heuristic = heuristic
                                print(f"Selected Heuristic: {self.selected_heuristic}")
                                self.is_choosing_heuristic = False
                                self.puzzle = N_Puzzle(size=3)  # Recreate the puzzle for now
                                self.dimension = self.puzzle.dimension
                                break
                    elif self.puzzle is not None:  # Handle puzzle clicks
                        self.handle_click(event.pos)
                        if self.puzzle.is_goal():
                            self.display_success_message()

        pygame.quit()    # pygame.quit()  # Make sure the pygame window is quit at the end 
    

    # def choose_heuristic(self):
    #     """Display the screen to choose a heuristic function."""
    #     self.screen.fill((255, 255, 255))  # White background
    #     title_text = self.font.render("Choose Heuristic", True, (0, 0, 0))
    #     self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

    #     heuristics = ["Misplaced Tiles", "Manhattan Distance", "Linear Conflict", "Euclidean Distance"]
    #     for i, heuristic in enumerate(heuristics):
    #         button = self.font.render(heuristic, True, (0, 0, 255))
    #         self.screen.blit(button, (self.width // 2 - button.get_width() // 2, 150 + i * 50))
    #     pygame.display.update()

    def display_success_message(self):
        """Display a success message when the puzzle is solved."""
        self.screen.fill((255, 255, 255))
        success_text = self.font.render("Puzzle Solved!", True, (0, 255, 0))
        self.screen.blit(success_text, (self.width // 2 - success_text.get_width() // 2, self.height // 2))
        pygame.display.update()
        pygame.time.wait(3000)  # Pause for 3 seconds

    def choose_heuristic(self):
        """Display the screen to choose a heuristic function."""
        self.screen.fill((255, 255, 255))  # White background
        title_text = self.font.render("Choose Heuristic", True, (0, 0, 0))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))
        # heuristic=self.selected_heuristic
        # self.puzzle=N_Puzzle(size=3)
        

        heuristics = {
            "Misplaced Tiles": misplaced_tiles_heuristic,
            "Manhattan Distance": manhattan_heuristic,
            "Linear Conflict": custom_heuristic,  # Replace with actual linear conflict if implemented
            "Euclidean Distance": euclidean_heuristic,
        }

        for i, heuristic_name in enumerate(heuristics.keys()):
            button = self.font.render(heuristic_name, True, (0, 0, 255))
            self.screen.blit(button, (self.width // 2 - button.get_width() // 2, 150 + i * 50))

        pygame.display.update()

        heuristic_selected = False
        while not heuristic_selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i, heuristic_name in enumerate(heuristics.keys()):
                        if 150 + i * 50 <= y <= 200 + i * 50:
                            heuristic_selected = True
                            heuristic = heuristics[heuristic_name]
                            if self.puzzle is None:
                                self.puzzle= N_Puzzle(size=3)
                            time_taken, num_moves = solve_puzzle(self.puzzle, heuristic)
                            print(f"Time Taken: {time_taken} seconds, Moves: {num_moves}")
                            self.display_results(heuristic_name, time_taken, num_moves)
                            return

    def solve_with_heuristic(self, heuristics, heuristic_name):
        """Solve the puzzle using the selected heuristic."""
        self.screen.fill((255, 255, 255))  # Clear screen
        heuristic_func = next(h[1] for h in heuristics if h[0] == heuristic_name)
        heuristic = getattr(__import__('heuristics'), heuristic_func)

        self.puzzle = N_Puzzle(size=3)  # Generate random puzzle of size 3 (8-puzzle)
        time_taken, num_moves = solve_puzzle(self.puzzle, heuristic)

        
    def display_results(self, heuristic_name, time_taken, num_moves):
        """Display results after solving the puzzle."""
        self.screen.fill((255, 255, 255))  # Clear screen
        heuristic_text = self.font.render(f"Heuristic: {heuristic_name}", True, (0, 0, 0))
        self.screen.blit(heuristic_text, (self.width // 2 - heuristic_text.get_width() // 2, 200))
        time_text = self.font.render(f"Time Taken: {time_taken:.2f}s", True, (0, 0, 0))
        self.screen.blit(time_text, (self.width // 2 - time_text.get_width() // 2, 300))
        moves_text = self.font.render(f"Moves: {num_moves}", True, (0, 0, 0))
        self.screen.blit(moves_text, (self.width // 2 - moves_text.get_width() // 2, 400))

        pygame.display.update()
        pygame.time.wait(5000)  # Wait for 5 seconds before returning to the menu


