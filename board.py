# Wangieyo is editing - NOBODY ELSE EDIT

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

        self.cells = [
            [Cell(puzzle[r][c], r, c, screen) for c in range(BOARD_SIZE)]
            for r in range(BOARD_SIZE)
        ]
        self.board = puzzle

    def draw(self):
        """Draws the grid outline (with bold box borders) and every cell."""
        for row in self.cells:
            for cell in row:
                cell.draw()

        for i in range(BOARD_SIZE + 1):
            line_width = 4 if i % 3 == 0 else 1
            # vertical line
            pygame.draw.line(
                self.screen, BLACK,
                (BOARD_X + i * CELL_SIZE, BOARD_Y),
                (BOARD_X + i * CELL_SIZE, BOARD_Y + BOARD_SIZE * CELL_SIZE),
                line_width,
            )
            # horizontal line
            pygame.draw.line(
                self.screen, BLACK,
                (BOARD_X, BOARD_Y + i * CELL_SIZE),
                (BOARD_X + BOARD_SIZE * CELL_SIZE, BOARD_Y + i * CELL_SIZE),
                line_width,
            )

    def select(self, row, col):
        """Marks the cell at (row, col) as the current selected cell."""
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
            cell.cell_value(0)
            cell.sketched_value(0)

    def sketch(self, value):
        """Sets the sketched value of the currently selected cell."""
        if self.selected_row is None:
            return
        cell = self.cells[self.selected_row][self.selected_col]
        if not cell.original:
            cell.sketched_value(value)

    def place_number(self, value):
        """Sets the value of the currently selected cell (on Enter)."""
        if self.selected_row is None:
            return
        cell = self.cells[self.selected_row][self.selected_col]
        if not cell.original:
            cell.cell_value(value)
            cell.sketched_value(0)

    def reset_to_original(self):
        """Resets all non-original cells back to empty (0)."""
        for row in self.cells:
            for cell in row:
                if not cell.original:
                    cell.cell_value(0)
                    cell.sketched_value(0)

    def is_full(self):
        """Returns True if every cell on the board has a nonzero value."""
        return all(cell.value != 0 for row in self.cells for cell in row)

    def update_board(self):
        """Updates the underlying 2D board list from all Cell values."""
        self.board = [[cell.value for cell in row] for row in self.cells]

    def find_empty(self):
        """Finds an empty cell and returns its (row, col), or None."""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None

    def check_board(self):
        """Checks whether the current board is a fully valid Sudoku solution."""
        self.update_board()
        board = self.board

        for i in range(BOARD_SIZE):
            row_vals = [v for v in board[i] if v != 0]
            if len(set(row_vals)) != len(row_vals):
                return False

            col_vals = [board[r][i] for r in range(BOARD_SIZE) if board[r][i] != 0]
            if len(set(col_vals)) != len(col_vals):
                return False

        box_size = 3
        for box_row in range(0, BOARD_SIZE, box_size):
            for box_col in range(0, BOARD_SIZE, box_size):
                vals = [
                    board[r][c]
                    for r in range(box_row, box_row + box_size)
                    for c in range(box_col, box_col + box_size)
                    if board[r][c] != 0
                ]
                if len(set(vals)) != len(vals):
                    return False

        return True