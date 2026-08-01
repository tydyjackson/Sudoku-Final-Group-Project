# Wangieyo is editing - NOBODY ELSE EDIT

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (160, 160, 160)
# LIGHT_GRAY = (222, 222, 222)
# RED = (200, 30, 30)
# GREEN = (0, 140, 60)
# BLUE = (20, 20, 200)

BS = 9
CS = 60
BX = 0
BY = 0

WIDTH = BS * CS
HEIGHT = BS * CS + 110
BOARD_END = BS * CS

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

        generator = SudokuGenerator(BS, removed)
        generator.fill_values()
        self.solution = [row[:] for row in generator.get_board()]

        generator.remove_cells()
        puzzle = generator.get_board()

        self.cells = [
            [Cell(puzzle[r][c], r, c, screen) for c in range(BS)]
            for r in range(BS)
        ]
        self.board = puzzle

    def draw(self):
        """Draws the grid outline (with bold box borders) and every cell."""
        for row in self.cells:
            for cell in row:
                cell.draw()

        for i in range(BS + 1):
            line_width = 4 if i % 3 == 0 else 1
            # vertical line
            pygame.draw.line(
                self.screen, BLACK,
                (BX + i * CS, BY),
                (BX + i * CS, BY + BS * CS),
                line_width,
            )
            # horizontal line
            pygame.draw.line(
                self.screen, BLACK,
                (BX, BY + i * CS),
                (BX + BS * CS, BY + i * CS),
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
        if BX <= x < BX + BS * CS and \
                BY <= y < BY + BS * CS:
            col = (x - BX) // CS
            row = (y - BY) // CS
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
        for r in range(BS):
            for c in range(BS):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None

    def check_board(self):
        """Checks whether the current board is a fully valid Sudoku solution."""
        self.update_board()
        board = self.board

        for i in range(BS):
            row_vals = [v for v in board[i] if v != 0]
            if len(set(row_vals)) != len(row_vals):
                return False

            col_vals = [board[r][i] for r in range(BS) if board[r][i] != 0]
            if len(set(col_vals)) != len(col_vals):
                return False

        box_size = 3
        for box_row in range(0, BS, box_size):
            for box_col in range(0, BS, box_size):
                vals = [
                    board[r][c]
                    for r in range(box_row, box_row + box_size)
                    for c in range(box_col, box_col + box_size)
                    if board[r][c] != 0
                ]
                if len(set(vals)) != len(vals):
                    return False

        return True