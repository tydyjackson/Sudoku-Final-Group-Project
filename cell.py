import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
RED = (200, 30, 30)
BLUE = (20, 20, 200)

CELL_SIZE = 60


class Cell:

    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

        # Original cells cannot be changed by the player.
        self.original = value != 0

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    # These two methods keep the current Board code compatible.
    def cell_value(self, value):
        self.set_cell_value(value)

    def sketch_value(self, value):
        self.set_sketched_value(value)

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        cell_rectangle = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self.screen, WHITE, cell_rectangle)

        if self.value != 0:
            number_font = pygame.font.Font(None, 42)

            if self.original:
                number_color = BLACK
            else:
                number_color = BLUE

            number = number_font.render(str(self.value), True, number_color)
            number_rectangle = number.get_rect(center=cell_rectangle.center)

            self.screen.blit(number, number_rectangle)

        elif self.sketched_value != 0:
            sketch_font = pygame.font.Font(None, 24)
            sketch = sketch_font.render(str(self.sketched_value), True, GRAY)
            self.screen.blit(sketch, (x + 6, y + 4))

        if self.selected:
            selected_rectangle = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4,)
            pygame.draw.rect(self.screen, RED, selected_rectangle, 3)