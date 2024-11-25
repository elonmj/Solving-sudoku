import copy
import random

from sudoku.exceptions import InvalidDigitError

type Coordinates = tuple[int, int]


class Board:
    """
    Sudoku board.
    """

    def __init__(self) -> None:
        """
        Initialize and fill the board.
        """
        self.grid = {(row, col): 0 for row in range(9) for col in range(9)}
        self.prefill()
        self.fill()
        self.prune(n=40)

    def __str__(self) -> str:
        """
        Return the string representation of the board.

        :return str: string representation of the board
        """
        result = ""
        for row in range(9):
            for col in range(9):
                result += str(self.grid[row, col]) + " "
            result += "\n"

        return result

    def setter(self, row: int, col: int, digit: int) -> None:
        """
        Set a digit on the board.

        :param int row: row index
        :param int col: column index
        :param int digit: digit to set
        :raises InvalidDigitError: if digit is not in the range [1, 9]
        """
        if digit < 1 | digit > 9:
            raise InvalidDigitError(digit)

        self.grid[row, col] = digit

    def getter(self, row: int, col: int) -> int:
        """
        Get a digit from the board.

        :param int row: row index
        :param int col: column index
        :return int: digit at the [row, col] position
        """
        return self.grid[row, col]

    def prefill(self) -> None:
        """
        Fill the board with random digits.
        """
        for block in range(3):
            digits = list(range(1, 10))
            random.shuffle(digits)

            start = block * 3
            stop = start + 3
            for row in range(start, stop):
                for col in range(start, stop):
                    self.grid[row, col] = digits.pop()

    def is_empty(self, row: int, col: int) -> bool:
        """
        Check if the given position is empty.

        :param int row: row index
        :param int col: column index
        :return bool: True if the position is empty, False otherwise
        """
        return self.grid[row, col] == 0

    def get_allowed(self, row: int, col: int) -> set[int]:
        """
        Get possible digits for the given position.
        Check the horizontal, vertical and subgrid (3x3).

        :param int row: row index
        :param int col: column index
        :return set[int]: set of possible digits or None
        """
        if self.grid[row, col] == 0:
            digits = set(range(10))
            horizontal = {self.grid[row, c] for c in range(9)}
            vertical = {self.grid[r, col] for r in range(9)}
            subgrid = {
                self.grid[r, c]
                for r in range(row - row % 3, row - row % 3 + 3)
                for c in range(col - col % 3, col - col % 3 + 3)
            }
            return digits - horizontal - vertical - subgrid
        return set()

    def fill(self) -> bool:
        """
        Fill the board recursively.

        :return bool: True if the board is filled, False otherwise
        """
        for row in range(9):
            for col in range(9):
                if self.is_empty(row, col):
                    for digit in self.get_allowed(row, col):
                        self.grid[row, col] = digit
                        if self.fill():
                            return True
                        self.grid[row, col] = 0
                    return False
        return True

    def prune(self, n: int) -> None:
        """
        Randomly remove `n` digits from the board.
        """
        self.visible = copy.deepcopy(self.grid)
        cells = list(self.visible.keys())
        for _ in range(n):
            cell = random.choice(cells)
            cells.remove(cell)
            self.visible[cell] = 0
