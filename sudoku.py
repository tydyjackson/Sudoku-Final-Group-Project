import random
import math

# Three conditions to be checked
# NUMBER DOES NOT REPEAT INSIDE THE BOX
# NUMBER DOES NOT REPEAT INSIDE THE ROW
# NUMBER DOES NOT REPEAT INSIDE THE COLUMN

# print(random.randint(1, 10))
# box ranges 0-2, 3-5, 6-8
import random

import pygame

from board import Board, WIDTH, HEIGHT, BOARD_END, BOARD_SIZE


# The original helper functions are kept here from the current project.
def is_valid(board, row, col, num):
    # Check row and column
    for i in range(9):
        # If the number is already in the row or column, it does not work.
        if board[row][i] == num or board[i][col] == num:
            return False

    # Find the top-left position of this cell's 3x3 box.
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True


def fill_board(board):
    for row in range(9):
        for col in range(9):
            # Look for an empty value.
            if board[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)

                for num in numbers:
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        if fill_board(board):
                            return True

                        board[row][col] = 0

                return False

    return True


def initialize_board(num_cols):
    secret_board = [[0 for _ in range(num_cols)] for _ in range(9)]
    return secret_board


def print_board(board):
    for row in range(len(board)):
        for column in range(len(board[0])):
            if column == len(board[0]) - 1:
                print(board[row][column], end="")
            else:
                print(board[row][column], end=" ")

        print()


# This keeps the old generator code available without running it at startup.
def test_old_generator():
    board = initialize_board(9)
    fill_board(board)
    return board


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (220, 238, 245)
DARK_BLUE = (20, 60, 100)
ORANGE = (225, 105, 30)
LIGHT_ORANGE = (245, 150, 80)
GREEN = (30, 150, 70)
RED = (190, 40, 40)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rectangle = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, ORANGE, self.rectangle)
        pygame.draw.rect(screen, BLACK, self.rectangle, 3)

        font = pygame.font.Font(None, 32)
        words = font.render(self.text, True, WHITE)
        words_rectangle = words.get_rect(center=self.rectangle.center)
        screen.blit(words, words_rectangle)

    def was_clicked(self, position):
        return self.rectangle.collidepoint(position)


def draw_centered_text(screen, text, y, size, color):
    font = pygame.font.Font(None, size)
    words = font.render(text, True, color)
    words_rectangle = words.get_rect(center=(WIDTH // 2, y))
    screen.blit(words, words_rectangle)


def create_start_buttons():
    easy_button = Button(30, 360, 145, 55, "EASY")
    medium_button = Button(198, 360, 145, 55, "MEDIUM")
    hard_button = Button(365, 360, 145, 55, "HARD")
    return easy_button, medium_button, hard_button


def create_game_buttons():
    reset_button = Button(20, BOARD_END + 28, 145, 52, "RESET")
    restart_button = Button(198, BOARD_END + 28, 145, 52, "RESTART")
    exit_button = Button(375, BOARD_END + 28, 145, 52, "EXIT")
    return reset_button, restart_button, exit_button


def draw_start_screen(screen, buttons):
    screen.fill(LIGHT_BLUE)
    draw_centered_text(screen, "Welcome to Sudoku", 170, 58, BLACK)
    draw_centered_text(screen, "Select Game Mode:", 285, 42, DARK_BLUE)

    for button in buttons:
        button.draw(screen)


def draw_game_screen(screen, game_board, buttons):
    screen.fill(LIGHT_BLUE)
    game_board.draw()

    for button in buttons:
        button.draw(screen)

    difficulty_text = "Difficulty: " + game_board.difficulty.capitalize()
    font = pygame.font.Font(None, 24)
    words = font.render(difficulty_text, True, DARK_BLUE)
    words_rectangle = words.get_rect(center=(WIDTH // 2, HEIGHT - 12))
    screen.blit(words, words_rectangle)


def draw_win_screen(screen, exit_button):
    screen.fill(LIGHT_BLUE)
    draw_centered_text(screen, "Game Won!", 250, 72, GREEN)
    exit_button.draw(screen)


def draw_lose_screen(screen, restart_button):
    screen.fill(LIGHT_BLUE)
    draw_centered_text(screen, "Game Over :(", 235, 68, RED)
    restart_button.draw(screen)


def move_selection(game_board, row_change, col_change):
    if game_board.selected_row is None:
        game_board.select(0, 0)
        return

    new_row = game_board.selected_row + row_change
    new_col = game_board.selected_col + col_change

    if new_row < 0:
        new_row = 0
    elif new_row >= BOARD_SIZE:
        new_row = BOARD_SIZE - 1

    if new_col < 0:
        new_col = 0
    elif new_col >= BOARD_SIZE:
        new_col = BOARD_SIZE - 1

    game_board.select(new_row, new_col)


def get_number_from_key(key):
    number_keys = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9,
        pygame.K_KP1: 1,
        pygame.K_KP2: 2,
        pygame.K_KP3: 3,
        pygame.K_KP4: 4,
        pygame.K_KP5: 5,
        pygame.K_KP6: 6,
        pygame.K_KP7: 7,
        pygame.K_KP8: 8,
        pygame.K_KP9: 9,
    }

    return number_keys.get(key)


def main():
    pygame.init()
    pygame.display.set_caption("Sudoku")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    state = "start"
    game_board = None
    running = True

    start_buttons = create_start_buttons()
    game_buttons = create_game_buttons()

    win_exit_button = Button(195, 340, 150, 58, "EXIT")
    lose_restart_button = Button(180, 330, 180, 58, "RESTART")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos

                if state == "start":
                    if start_buttons[0].was_clicked(mouse_position):
                        game_board = Board(WIDTH, HEIGHT, screen, "easy")
                        state = "game"

                    elif start_buttons[1].was_clicked(mouse_position):
                        game_board = Board(WIDTH, HEIGHT, screen, "medium")
                        state = "game"

                    elif start_buttons[2].was_clicked(mouse_position):
                        game_board = Board(WIDTH, HEIGHT, screen, "hard")
                        state = "game"

                elif state == "game":
                    clicked_cell = game_board.click(
                        mouse_position[0],
                        mouse_position[1],
                    )

                    if clicked_cell is not None:
                        game_board.select(clicked_cell[0], clicked_cell[1])

                    elif game_buttons[0].was_clicked(mouse_position):
                        game_board.reset_to_original()

                    elif game_buttons[1].was_clicked(mouse_position):
                        game_board = None
                        state = "start"

                    elif game_buttons[2].was_clicked(mouse_position):
                        running = False

                elif state == "won":
                    if win_exit_button.was_clicked(mouse_position):
                        running = False

                elif state == "lost":
                    if lose_restart_button.was_clicked(mouse_position):
                        game_board = None
                        state = "start"

            elif event.type == pygame.KEYDOWN and state == "game":
                # This safely reads the number row and number pad.
                number = get_number_from_key(event.key)

                if number is not None:
                    game_board.sketch(number)

                elif (
                    event.key == pygame.K_RETURN
                    or event.key == pygame.K_KP_ENTER
                ):
                    if game_board.selected_row is not None:
                        selected_cell = game_board.cells[
                            game_board.selected_row
                        ][game_board.selected_col]

                        if not selected_cell.original:
                            if selected_cell.sketched_value != 0:
                                game_board.place_number(
                                    selected_cell.sketched_value
                                )

                                if game_board.is_full():
                                    if game_board.check_board():
                                        state = "won"
                                    else:
                                        state = "lost"

                elif (
                    event.key == pygame.K_BACKSPACE
                    or event.key == pygame.K_DELETE
                ):
                    game_board.clear()

                elif event.key == pygame.K_UP:
                    move_selection(game_board, -1, 0)

                elif event.key == pygame.K_DOWN:
                    move_selection(game_board, 1, 0)

                elif event.key == pygame.K_LEFT:
                    move_selection(game_board, 0, -1)

                elif event.key == pygame.K_RIGHT:
                    move_selection(game_board, 0, 1)

        if state == "start":
            draw_start_screen(screen, start_buttons)

        elif state == "game":
            draw_game_screen(screen, game_board, game_buttons)

        elif state == "won":
            draw_win_screen(screen, win_exit_button)

        elif state == "lost":
            draw_lose_screen(screen, lose_restart_button)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()