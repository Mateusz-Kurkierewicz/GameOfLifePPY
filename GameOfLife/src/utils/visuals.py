import pygame
from pygame import Rect
from pygame_gui.core import UIElement

#TODO: Do zaimplementowania
class GridLayout:

    def __init__(self, screen, screen_resolution):
        self.screen = screen
        self.screen_resolution = screen_resolution
        self.grid = [[]]

    def configure_row(self, index: int, weight: int):
        pass

    def configure_column(self, index: int, weight: int):
        pass

    def add_component(self, component: UIElement, row: int, column: int):
        pass

    def set_resolution(self, resolution):
        pass

    class GridElement:

        def __init__(self, element, is_grid):
            self.element = element
            self.is_grid = is_grid


class GridField:

    def __init__(self, screen, base: Rect, border_colour, fill_colour, x: int, y: int):
        self.x = x
        self.y = y
        self.screen = screen
        self.base = base
        self.border_colour = border_colour
        self.fill_colour = fill_colour

    def draw(self):
        pygame.draw.rect(self.screen, self.fill_colour, self.base)
        pygame.draw.rect(self.screen, self.border_colour, self.base, 1)

    def is_in_bounds(self, x: int, y: int):
        return ((self.base.x < x < self.base.x + self.base.width)
                and (self.base.y < y < self.base.y + self.base.height))

    def set_fill_colour(self, colour: tuple):
        self.fill_colour = colour

    def __str__(self):
        return ("Field[x=" + str(self.base.x)
                + ", y=" + str(self.base.y)
                + ", width=" + str(self.base.width)
                + ", height=" + str(self.base.height)
                + "]")


class GridPanel:

    def __init__(self, screen, base: Rect, rows: int = 1, columns: int = 1, border_colour = (255, 255, 255), fill_colour = (0, 0, 0)):
        self.screen = screen
        self.base = base
        self.rows = rows
        self.columns = columns
        self.border_colour = border_colour
        self.fill_colour = fill_colour
        self.fields = [[]]
        self.update()
        self.is_enabled = True

    def set_rows(self, rows: int):
        self.rows = rows
        self.update()

    def set_columns(self, columns: int):
        self.columns = columns
        self.update()

    def draw(self):
        pygame.draw.rect(self.screen, self.border_colour, self.base, 3)
        for r in self.fields:
            for f in r:
                f.draw()

    def update(self):
        self.fields.clear()
        self.fields = [[None for _ in range(self.columns)].copy() for _ in range(self.rows)]
        field_x = self.base.width / self.columns
        field_y = self.base.height / self.rows
        x_coordinate = self.base.x
        y_coordinate = self.base.y
        for y in range(self.rows):
            for x in range(self.columns):
                rect = GridField(self.screen, pygame.Rect(x_coordinate + x * field_x,
                                                          y_coordinate + y * field_y,
                                                          field_x,
                                                          field_y),
                                 self.border_colour,
                                 self.fill_colour,
                                 y, x)
                self.fields[y][x] = rect

    def get_field_by_loc(self, x: int, y: int) -> GridField:
        for l in self.fields:
            for f in l:
                if f.is_in_bounds(x, y):
                    return f
        return None

    def get_field_by_index(self, x: int, y: int) -> GridField:
        return self.fields[x][y]

    def scale(self, x: int, y: int):
        pass

    def move(self, x: int, y: int):
        pass

    def enable(self):
        self.is_enabled = True

    def disable(self):
        self.is_enabled = False