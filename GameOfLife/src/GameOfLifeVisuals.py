from typing import SupportsIndex

import pygame
import pygame_gui
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


class GridPanel:

    def __init__(self, screen, base: Rect, rows: int = 1, columns: int = 1, colour = (255, 255, 255)):
        self.screen = screen
        self.base = base
        self.rows = rows
        self.columns = columns
        self.colour = colour
        self.fields = [[]]
        self.update()

    def set_rows(self, rows: int):
        self.rows = rows
        self.update()

    def set_columns(self, columns: int):
        self.columns = columns
        self.update()

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.base, 3)
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
        for i in self.fields:
            print(i)
        #x = 0
        # while x < self.base.width:
        #     y = 0
        #     while y < self.base.height:
        #         rect = pygame.Rect(x_coordinate + x, y_coordinate + y, field_x, field_y)
        #         y += field_y
        #     x += field_x
        #
        for x in range(self.rows):
            for y in range(self.columns):
                rect = GridField(self.screen, pygame.Rect(x_coordinate + x * field_x, y_coordinate + y * field_y, field_x, field_y), self.colour)
                self.fields[x][y] = rect

    def handle_click(self, x: int, y: int):
        pass

    def scale(self, x: int, y: int):
        pass

    def move(self, x: int, y: int):
        pass


class GridField:

    def __init__(self, screen, base: Rect, colour):
        self.screen = screen
        self.base = base
        self.colour = colour

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.base, 1)