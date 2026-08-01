class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = 3
        self.board = []

        # Creates an empty board filled with 0's
        for row in range(self.row_length):
            new_row = []

            for col in range(self.row_length):
                new_row.append(0)

            self.board.append(new_row)

    def get_board(self):
        return self.board

    def print_board(self):
        for row in range(self.row_length):
            for col in range(self.row_length):
                print(self.board[row][col], end=" ")

            print()

    def valid_in_row(self, row, num):
        # Checks whether the number is already in the row
        for col in range(self.row_length):
            if self.board[row][col] == num:
                return False

        return True

    def valid_in_col(self, col, num):
        # Checks whether the number is already in the columns
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False

        return True

    def valid_in_box(self, row_start, col_start, num):
        # Checks whether the number is already in a 3x3 box or not
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                if self.board[row][col] == num:
                    return False

        return True

    def is_valid(self, row, col, num):
        row_start = row - row % self.box_length
        col_start = col - col % self.box_length

        if not self.valid_in_row(row, num):
            return False

        if not self.valid_in_col(col, num):
            return False

        if not self.valid_in_box(row_start, col_start, num):
            return False

        return True

    def fill_box(self, row_start, col_start):
        pass

    def fill_diagonal(self):
        pass

    def fill_remaining(self):
        pass

    def fill_values(self):
        pass

    def remove_cells(self):
        pass


def generate_sudoku(size, removed):
    pass


if __name__ == "__main__":
    test_board = SudokuGenerator(9, 30)
    test_board.print_board()