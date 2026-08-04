import random


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):  # TY IS EDITING - NOBODY ELSE EDIT
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

    def get_board(self):  # TY IS EDITING - NOBODY ELSE EDIT
        return self.board

    def print_board(self):  # TY IS EDITING - NOBODY ELSE EDIT
        for row in range(self.row_length):
            for col in range(self.row_length):
                print(self.board[row][col], end=" ")

            print()

    def valid_in_row(self, row, num):  # TY IS EDITING - NOBODY ELSE EDIT
        # Checks whether the number is already in the row
        for col in range(self.row_length):
            if self.board[row][col] == num:
                return False

        return True

    def valid_in_col(self, col, num):  # TY IS EDITING - NOBODY ELSE EDIT
        # Checks whether the number is already in the columns
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False

        return True

    def valid_in_box(self, row_start, col_start, num):  # TY IS EDITING - NOBODY ELSE EDIT
        # Checks whether the number is already in a 3x3 box or not
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                if self.board[row][col] == num:
                    return False

        return True

    def is_valid(self, row, col, num):  # TY IS EDITING - NOBODY ELSE EDIT
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
        # Make a shuffled list so every box is different.
        numbers = list(range(1, self.row_length + 1))
        random.shuffle(numbers)
        number_index = 0

        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                self.board[row][col] = numbers[number_index]
                number_index += 1

    def fill_diagonal(self):
        # These three boxes do not share rows or columns with each other.
        for start in range(0, self.row_length, self.box_length):
            self.fill_box(start, start)

    def fill_remaining(self):
        # Find the next empty space on the board.
        empty_row = -1
        empty_col = -1

        for row in range(self.row_length):
            for col in range(self.row_length):
                if self.board[row][col] == 0:
                    empty_row = row
                    empty_col = col
                    break

            if empty_row != -1:
                break

        # No empty space means the board is finished.
        if empty_row == -1:
            return True

        numbers = list(range(1, self.row_length + 1))
        random.shuffle(numbers)

        # Try each number until one lets the rest of the board work.
        for num in numbers:
            if self.is_valid(empty_row, empty_col, num):
                self.board[empty_row][empty_col] = num

                if self.fill_remaining():
                    return True

                self.board[empty_row][empty_col] = 0

        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        cells_removed = 0

        # Keep choosing random cells until the correct amount is empty.
        while cells_removed < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)

            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_removed += 1


def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    generator.fill_values()
    generator.remove_cells()
    return generator.get_board()


if __name__ == "__main__":
    test_board = SudokuGenerator(9, 30)
    test_board.fill_values()
    test_board.remove_cells()
    test_board.print_board()