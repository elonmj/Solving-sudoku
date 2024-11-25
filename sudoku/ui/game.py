import time
from enum import Enum

import pygame
import pygame.freetype

from sudoku.logic.board import Board, Coordinates

pygame.init()
pygame.display.set_caption("Sudoku")


class Color(Enum):
    BEIGE = (202, 194, 186)
    BLACK = (0, 0, 0)
    CORAL = (255, 127, 8)
    GREEN = (79, 159, 77)
    WHITE = (225, 225, 225)


class Game:
    def __init__(self) -> None:
        # Pygame setup
        self._clock = pygame.time.Clock()
        self._padding = 10
        self._resolution = (360, 360)
        self._stats_padding = 40
        self._time = time.time()

        # Game state
        self.board = Board()
        self.lives = 5
        self.rects: dict[Coordinates, pygame.Rect] = {}

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
        padding = self._padding + self._stats_padding

        def _draw_cells() -> None:
            """
            Draw the cells on the screen.
            """
            # Draw cells
            for i in range(9):
                for j in range(9):
                    rect = pygame.Rect(
                        j * x // 9 + self._padding,
                        i * y // 9 + padding,
                        x // 9,
                        y // 9,
                    )
                    pygame.draw.rect(
                        self._screen,
                        Color.BEIGE.value
                        if self.board.visible[(i, j)] != 0
                        else Color.WHITE.value,
                        rect,
                    )
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
                        (col - 1) * y // 9 + padding,
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
                        padding,
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
                        (col - 1) // 3 * x // 3 + padding,
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
                    padding,
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
                        i * y // 3 + padding,
                        x // 3,
                        y // 3,
                    )
                    pygame.draw.rect(self._screen, Color.BLACK.value, rect, 1)

        def _draw_stats() -> None:
            """
            Draw the stats on the screen.
            """
            font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 18)
            heart = pygame.image.load("assets/images/heart.png")
            text = font.render("Lives: ", True, Color.BLACK.value)
            self._screen.blit(
                text,
                (
                    self._padding,
                    self._padding // 2
                    + self._stats_padding // 2
                    - text.get_size()[1] // 2,
                ),
            )
            for i in range(self.lives):
                self._screen.blit(
                    heart,
                    (
                        self._padding + text.get_size()[0] + i * 20,
                        self._padding // 2 + self._stats_padding // 2 - 6,
                    ),
                )

        def _draw_digits() -> None:
            """
            Draw the digits on the screen.
            """
            font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 22)
            x, y = self._resolution
            for i in range(9):
                for j in range(9):
                    if self.board.visible[i, j] != 0:
                        text = font.render(
                            str(self.board.visible[i, j]), True, Color.BLACK.value
                        )
                        width, height = text.get_size()
                        self._screen.blit(
                            text,
                            (
                                j * x // 9 + x // 9 // 2 + self._padding - width // 2,
                                i * y // 9
                                + y // 9 // 2
                                + self._padding
                                + self._stats_padding
                                - height // 2,
                            ),
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

        _draw_cells()
        _draw_grid()
        _draw_stats()
        _draw_digits()
        _draw_time()

        pygame.display.flip()
        self._clock.tick(60)

    def play(self) -> bool:
        # Set resolution
        x, y = self._resolution
        size = [
            x + self._padding * 2,
            y + self._padding * 2 + self._stats_padding,
        ]
        self._screen = pygame.display.set_mode(size)

        self.update()
        pygame.display.flip()

        # Game loop
        self._clicked = None
        self._hovered = None
        while True:
            # Check if the game is won
            if all([digit != 0 for digit in self.board.visible.values()]):
                self.show_game_over("You Win!")
                return True

            for event in pygame.event.get():
                # Get mouse position
                pos = pygame.mouse.get_pos()

                # Handle mouse movement
                if event.type == pygame.MOUSEMOTION:
                    hovered = [
                        (cell, rect)
                        for (cell, rect) in self.rects.items()
                        if rect.collidepoint(pos)
                    ]
                    if hovered:
                        cell, rect = hovered[0]
                        x, y = cell
                        if self.board.visible[x, y] == 0:
                            self._hovered = rect
                            self.update(hover=rect)

                        else:
                            self._hovered = None
                            self.update()

                    else:
                        self._hovered = None
                        self.update()

                # Handle mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hovered = [
                        (cell, rect)
                        for (cell, rect) in self.rects.items()
                        if rect.collidepoint(pos)
                    ]
                    row, col = hovered[0][0]
                    if self.board.visible[row, col] == 0:
                        self.update(click=rect)
                        pygame.display.flip()

                        digit = None
                        while digit is None:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.unicode.isdigit():
                                        digit = int(event.unicode)
                                        if digit == self.board.grid[x, y]:
                                            pygame.mixer.music.load(
                                                "assets/sounds/Misc 1.wav"
                                            )
                                            pygame.mixer.music.play()
                                            self.board.visible[x, y] = digit
                                            self.update()
                                            break

                                        else:
                                            self.lives -= 1
                                            pygame.mixer.music.load(
                                                "assets/sounds/Coin 1.wav"
                                            )
                                            pygame.mixer.music.play()
                                            if self.lives <= 0:
                                                self.show_game_over("Game Over!")
                                                return False

                                            self.update()
                                            break

                if event.type == pygame.QUIT:
                    return True

            if self._hovered:
                self.update(hover=self._hovered)
            else:
                self.update()

    def show_game_over(self, message: str) -> None:
        """
        Show the game over screen.

        :param str message: message to display
        """
        self._screen.fill(Color.WHITE.value)
        font = pygame.font.Font("assets/fonts/OpenSans-Medium.ttf", 32)
        text = font.render(message, True, Color.BLACK.value)
        text_rect = text.get_rect(
            center=(
                self._resolution[0] // 2,
                self._resolution[1] // 2,
            )
        )
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
        pygame.time.wait(5000)
