import time
from enum import Enum
from typing import Tuple

import pygame
import pygame.freetype

from sudoku.models.board import Board, Coordinates
from sudoku.solver.solver import SudokuSolver
from sudoku.config import GameConfig, Color
from sudoku.ui.components import Button, Grid

pygame.init()
pygame.display.set_caption("Sudoku")


class GameState:
    PLAYING = "playing"
    SOLVING = "solving"
    GAME_OVER = "game_over"


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Sudoku")
        
        self.state = GameState.PLAYING
        self.clock = pygame.time.Clock()
        self._resolution = GameConfig.WINDOW_SIZE  # Ajout de l'attribut manquant
        self._padding = GameConfig.PADDING
        self._button_height = GameConfig.BUTTON_HEIGHT
        self._stats_padding = self._button_height + self._padding * 2
        self._total_height = self._resolution[1] + self._stats_padding + self._padding
        self._time = time.time()
        self.screen = pygame.display.set_mode(self._calculate_window_size())
        
        # Game state
        self.board = Board()
        self.solve_button = Button(
            GameConfig.PADDING, 
            GameConfig.PADDING, 
            "Solve"
        )
        self.grid = Grid(
            self.board,
            GameConfig.PADDING,
            GameConfig.BUTTON_HEIGHT + GameConfig.PADDING * 2
        )
        self.rects = {}  # Pour stocker les rectangles de la grille
        self._selected_cell = None
        self._button_rect = None
        self._button_hovered = False

    def _calculate_window_size(self) -> tuple[int, int]:
        total_height = (
            GameConfig.WINDOW_SIZE[1] + 
            GameConfig.BUTTON_HEIGHT + 
            GameConfig.PADDING * 3
        )
        return (
            GameConfig.WINDOW_SIZE[0] + GameConfig.PADDING * 2,
            total_height
        )

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if self.solve_button.handle_event(event):
                self._handle_solve()
                
            # Handle other events...
        return True

    def _handle_solve(self) -> None:
        self.state = GameState.SOLVING
        solver = SudokuSolver(self.board)
        solution = solver.solve()
        if solution:
            self._animate_solution(solution)
        self.state = GameState.PLAYING

    def draw_digit(self, pos: Tuple[int, int], digit: int, is_initial: bool = False) -> None:
        """
        Dessine un chiffre à une position donnée
        
        :param pos: Position (row, col)
        :param digit: Chiffre à dessiner
        :param is_initial: Si c'est un chiffre initial
        """
        i, j = pos
        x, y = self._resolution
        font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 22)
        
        if is_initial:
            color = Color.BLACK.value
        else:
            # Vérifier si le chiffre est valide
            current = self.board.grid[i, j]
            self.board.grid[i, j] = 0
            allowed = self.board.get_allowed(i, j)
            self.board.grid[i, j] = current
            
            color = (0, 0, 255) if digit in allowed else (255, 0, 0)
        
        text = font.render(str(digit), True, color)
        width, height = text.get_size()
        self._screen.blit(
            text,
            (
                j * x // 9 + x // 9 // 2 + self._padding - width // 2,
                i * y // 9 + y // 9 // 2 + self._stats_padding - height // 2,
            ),
        )

    def update(
        self, hover: pygame.Rect | None = None, click: pygame.Rect | None = None
    ) -> None:
        """
        Update the game screen.
        This method draws the grid, stats, and digits on the screen.

        :param pygame.Rect | None hover: the cell being hovered, defaults to None
        :param pygame.Rect | None click: the cell being clicked, defaults to None
        """

        x, y = self._resolution
        grid_offset_y = self._stats_padding  # Nouveau décalage vertical pour la grille

        def _draw_cells() -> None:
            """
            Draw the cells on the screen.
            """
            # Draw cells
            for i in range(9):
                for j in range(9):
                    rect = pygame.Rect(
                        j * x // 9 + self._padding,
                        i * y // 9 + grid_offset_y,
                        x // 9,
                        y // 9,
                    )
                    # Déterminer la couleur de la case
                    if (i, j) == self._selected_cell:
                        cell_color = Color.CORAL.value  # Couleur pour la case sélectionnée
                    elif self.board.grid[(i, j)] != 0:
                        cell_color = Color.BEIGE.value
                    else:
                        cell_color = Color.WHITE.value
                    pygame.draw.rect(self._screen, cell_color, rect)
                    pygame.draw.rect(self._screen, (150, 150, 150), rect, 1)
                    self.rects[i, j] = rect

            if hover:
                row, col = [i // (self._resolution[0] // 9) for i in hover.topleft]
                # Row
                pygame.draw.rect(
                    self._screen,
                    Color.GREEN.value,
                    pygame.Rect(
                        self._padding,
                        (col - 1) * y // 9 + grid_offset_y,
                        x,
                        y // 9,
                    ),
                    2,
                )
                # Column
                pygame.draw.rect(
                    self._screen,
                    Color.GREEN.value,
                    pygame.Rect(
                        row * x // 9 + self._padding,
                        grid_offset_y,
                        x // 9,
                        y,
                    ),
                    2,
                )
                # Subgrid
                pygame.draw.rect(
                    self._screen,
                    Color.GREEN.value,
                    pygame.Rect(
                        row // 3 * y // 3 + self._padding,
                        (col - 1) // 3 * x // 3 + grid_offset_y,
                        x // 3,
                        y // 3,
                    ),
                    3,
                )
                # Cell content
                pygame.draw.rect(self._screen, Color.GREEN.value, hover)
                # Cell border
                pygame.draw.rect(self._screen, Color.BLACK.value, hover, 1)

            if click:
                pygame.draw.rect(self._screen, Color.CORAL.value, click)
                pygame.draw.rect(self._screen, Color.BLACK.value, click, 1)

        def _draw_grid() -> None:
            """
            Draw the grid on the screen.
            """
            # Draw the border around the board
            pygame.draw.rect(
                self._screen,
                Color.BLACK.value,
                pygame.Rect(
                    self._padding,
                    grid_offset_y,
                    x,
                    y,
                ),
                3,
            )

            # Draw the 3x3 blocks
            for i in range(3):
                for j in range(3):
                    rect = pygame.Rect(
                        j * x // 3 + self._padding,
                        i * y // 3 + grid_offset_y,
                        x // 3,
                        y // 3,
                    )
                    pygame.draw.rect(self._screen, Color.BLACK.value, rect, 1)

        def _draw_digits() -> None:
            """
            Draw the digits on the screen.
            """
            for i in range(9):
                for j in range(9):
                    digit = self.board.grid[i, j]
                    if digit != 0:
                        self.draw_digit(
                            (i, j), 
                            digit, 
                            is_initial=(i, j) in self.board.initial_cells
                        )

        def _draw_time() -> None:
            """
            Draw the time on the screen.
            """
            font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 16)
            text = font.render(
                f"{int(time.time() - self._time) // 60:02d}:{int(time.time() - self._time) % 60:02.0f}",
                True,
                Color.BLACK.value,
                Color.WHITE.value,
            )
            width, height = text.get_size()
            self._screen.blit(
                text,
                (
                    self._resolution[0] + self._padding - width,
                    self._padding // 2 + self._stats_padding // 2 - height // 2,
                ),
            )

        self._screen.fill(Color.WHITE.value)
        self.solve_button.draw(self._screen)
        self._button_rect = self.solve_button.rect  # Garder une référence au rectangle du bouton
        
        pos = pygame.mouse.get_pos()
        if self._button_rect.collidepoint(pos):
            self._button_hovered = True
        else:
            self._button_hovered = False
            
        _draw_cells()
        _draw_grid()
        _draw_digits()
        _draw_time()

        pygame.display.flip()
        self.clock.tick(60)

    def play(self) -> bool:
        # Setup initial display
        x, y = self._resolution
        size = [x + self._padding * 2, self._total_height]
        self._screen = pygame.display.set_mode(size)

        self.update()
        pygame.display.flip()

        # Game loop
        self._clicked = None
        self._hovered = None
        while True:
            if all([self.board.grid[i, j] == self.board.solution[i, j] 
                    for i in range(9) for j in range(9)]):
                self.show_game_over("You Win!")
                return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

                pos = pygame.mouse.get_pos()

                # Gestion du survol
                if event.type == pygame.MOUSEMOTION:
                    hovered = [
                        (cell, rect)
                        for (cell, rect) in self.rects.items()
                        if rect.collidepoint(pos)
                    ]
                    if hovered:
                        cell, rect = hovered[0]
                        x, y = cell
                        if self.board.grid[x, y] == 0:
                            self._hovered = rect
                            self.update(hover=rect)
                        else:
                            self._hovered = None
                            self.update()
                    else:
                        self._hovered = None
                        self.update()

                # Gestion du clic
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._button_rect and self._button_rect.collidepoint(event.pos):
                        # Call the solver
                        solver = SudokuSolver(self.board)
                        solution = solver.solve()
                        if solution:
                            # Animate the solved digits
                            for (row, col), value in solution.items():
                                if self.board.grid[row, col] == 0:
                                    pygame.time.wait(500)  # Delay in milliseconds
                                    self.board.grid[row, col] = value
                                    self.draw_digit((row, col), value, is_initial=False)
                                    pygame.display.flip()
                            # Check if the board is complete
                            if all(self.board.grid[(i, j)] == self.board.solution[(i, j)] for i in range(9) for j in range(9)):
                                self.show_game_over("Solved!")
                        else:
                            print("No solution found.")
                    hovered = [
                        (cell, rect)
                        for (cell, rect) in self.rects.items()
                        if rect.collidepoint(pos)
                    ]
                    if hovered:
                        cell, rect = hovered[0]
                        row, col = cell
                        if (row, col) not in self.board.initial_cells:
                            self._selected_cell = (row, col)
                            self.update(click=rect)
                        else:
                            self._selected_cell = None
                    else:
                        self._selected_cell = None
                        self.update()

                # Gestion du clavier
                if event.type == pygame.KEYDOWN and self._selected_cell:
                    row, col = self._selected_cell
                    if event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                        if (row, col) not in self.board.initial_cells:
                            self.board.grid[row, col] = 0
                            self.update()
                    elif event.unicode.isdigit() and event.unicode != '0':
                        if (row, col) not in self.board.initial_cells:
                            digit = int(event.unicode)
                            self.board.grid[row, col] = digit
                            self.update()

            # Mise à jour de l'affichage
            if self._hovered and not self._selected_cell:
                self.update(hover=self._hovered)
            elif self._selected_cell:
                self.update(click=self.rects[self._selected_cell])
            else:
                self.update()

    def show_game_over(self, message: str) -> None:
        self._screen.fill(Color.WHITE.value)
        font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 32)
        text = font.render(message, True, Color.BLACK.value)
        text_rect = text.get_rect(center=(self._resolution[0] // 2, self._resolution[1] // 2))
        self._screen.blit(text, text_rect)

        time_text = font.render(
            f"Time: {int(time.time() - self._time) // 60:02d}:{int(time.time() - self._time) % 60:02.0f}",
            True,
            Color.BLACK.value,
        )
        time_text_rect = time_text.get_rect(
            center=(
                self._resolution[0] // 2,
                self._resolution[1] // 2 + 40,
            )
        )
        self._screen.blit(time_text, time_text_rect)
        pygame.display.flip()        
        pygame.time.wait(2000)
