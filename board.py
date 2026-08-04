# Wangieyo is editing - NOBODY ELSE EDIT

import pygame

from cell import Cell
from sudoku_generator import SudokuGenerator


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
LIGHT_GRAY = (222, 222, 222)
RED = (200, 30, 30)
GREEN = (0, 140, 60)
BLUE = (20, 20, 200)

BOARD_SIZE = 9
CELL_SIZE = 60
BOARD_X = 0
BOARD_Y = 0

WIDTH = BOARD_SIZE * CELL_SIZE
HEIGHT = BOARD_SIZE * CELL_SIZE + 110
BOARD_END = BOARD_SIZE * CELL_SIZE

DIFFICULTY_REMOVED = {
    "easy": 30,
    "medium": 40,
    "hard": 50,
}


class Board:
    def __init__(self, width, height, screen, difficulty):
        """
        Constructor for the Board class.
        screen: a PyGame window/surface.
        difficulty: "easy", "medium", or "hard".
        """
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        self.selected_row = None
        self.selected_col = None

        removed = DIFFICULTY_REMOVED.get(difficulty, 30)

        generator = SudokuGenerator(BOARD_SIZE, removed)
        generator.fill_values()
        self.solution = [row[:] for row in generator.get_board()]

        generator.remove_cells()
        puzzle = generator.get_board()

        # Save the starting puzzle so Reset can restore it.
        self.original_board = [row[:] for row in puzzle]

        self.cells = [
            [Cell(puzzle[r][c], r, c, screen) for c in range(BOARD_SIZE)]
            for r in range(BOARD_SIZE)
        ]
        self.board = [row[:] for row in puzzle]

    def draw(self):
        """Draws the grid outline (with bold box borders) and every cell."""
        for row in self.cells:
            for cell in row:
                cell.draw()

        for i in range(BOARD_SIZE + 1):
            line_width = 4 if i % 3 == 0 else 1

            # Vertical line
            pygame.draw.line(
                self.screen,
                BLACK,
                (BOARD_X + i * CELL_SIZE, BOARD_Y),
                (BOARD_X + i * CELL_SIZE, BOARD_Y + BOARD_SIZE * CELL_SIZE),
                line_width,
            )

            # Horizontal line
            pygame.draw.line(
                self.screen,
                BLACK,
                (BOARD_X, BOARD_Y + i * CELL_SIZE),
                (BOARD_X + BOARD_SIZE * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                line_width,
            )

    def select(self, row, col):
        """Marks the cell at (row, col) as the current selected cell."""
        if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
            return

        if self.selected_row is not None:
            self.cells[self.selected_row][self.selected_col].selected = False

        self.selected_row = row
        self.selected_col = col
        self.cells[row][col].selected = True

    def click(self, x, y):
        """
        If (x, y) is within the displayed board, returns (row, col) of the
        clicked cell. Otherwise returns None.
        """
        if BOARD_X <= x < BOARD_X + BOARD_SIZE * CELL_SIZE and \
                BOARD_Y <= y < BOARD_Y + BOARD_SIZE * CELL_SIZE:
            col = (x - BOARD_X) // CELL_SIZE
            row = (y - BOARD_Y) // CELL_SIZE
            return (row, col)

        return None

    def clear(self):
        """
        Clears the value and sketched value of the selected cell, but only
        if that cell was not part of the original generated puzzle.
        """
        if self.selected_row is None:
            return

        cell = self.cells[self.selected_row][self.selected_col]

        if not cell.original:
            cell.set_cell_value(0)
            cell.set_sketched_value(0)

    def sketch(self, value):
        """Sets the sketched value of the currently selected cell."""
        if self.selected_row is None:
            return

        cell = self.cells[self.selected_row][self.selected_col]

        if not cell.original:
            cell.set_sketched_value(value)

    def place_number(self, value):
        """Sets the value of the currently selected cell (on Enter)."""
        if self.selected_row is None:
            return

        cell = self.cells[self.selected_row][self.selected_col]

        if not cell.original:
            cell.set_cell_value(value)
            cell.set_sketched_value(0)

    def reset_to_original(self):
        """Resets all cells to the values from the starting puzzle."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell = self.cells[row][col]
                cell.set_cell_value(self.original_board[row][col])
                cell.set_sketched_value(0)

        self.update_board()

    def is_full(self):
        """Returns True if every cell on the board has a nonzero value."""
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False

        return True

    def update_board(self):
        """Updates the underlying 2D board list from all Cell values."""
        self.board = []

        for row in self.cells:
            board_row = []

            for cell in row:
                board_row.append(cell.value)

            self.board.append(board_row)

    def find_empty(self):
        """Finds an empty cell and returns its (row, col), or None."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.cells[row][col].value == 0:
                    return (row, col)

        return None

    def check_board(self):
        """Checks whether the current board is the completed solution."""
        if not self.is_full():
            return False

        self.update_board()

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != self.solution[row][col]:
                    return False

        return True