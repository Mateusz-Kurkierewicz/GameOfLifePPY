import pygame
from pygame import Rect
from pygame_gui.core import UIElement


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

    """
    Reprezentuje pole planszy kratowanej. Może reagować na kliknięcia.
    """

    def __init__(self, screen, base: Rect, border_colour, fill_colour, x: int, y: int):
        """
        Args:
            screen: Ekran, na którym ma się wyświetlać pole
            base (Rect): Kształt bazowy do rysowania pola
            border_colour (tuple): Kolor obramowania
            fill_colour (tuple): Kolor wypełnienia
            x (int): Współrzędna x (kolumna)
            y (int): Współrzędna y (wiersz)
        """
        self.x = x
        self.y = y
        self.screen = screen
        self.base = base
        self.border_colour = border_colour
        self.fill_colour = fill_colour

    def draw(self):
        """
        Wyświetla pole na ekranie
        """
        pygame.draw.rect(self.screen, self.fill_colour, self.base)
        pygame.draw.rect(self.screen, self.border_colour, self.base, 1)

    def is_in_bounds(self, x: int, y: int):
        """
        Sprawdza, czy podane koordynaty znajdują się w obrębie pola.

        Args:
            x (int): Współrzędna x
            y (int): Współrzędna y
        """
        return ((self.base.x < x < self.base.x + self.base.width)
                and (self.base.y < y < self.base.y + self.base.height))

    def set_fill_colour(self, colour: tuple):
        """
        Wypełnia pole podanym kolorem.

        Args:
            colour (tuple): Kolor do wypełnienia pola
        """
        self.fill_colour = colour

    def __str__(self):
        return ("Field[x=" + str(self.base.x)
                + ", y=" + str(self.base.y)
                + ", width=" + str(self.base.width)
                + ", height=" + str(self.base.height)
                + "]")


class GridPanel:

    """
    Reprezentuje kratowaną planszę interfejsie graficznym.
    """

    def __init__(self, screen, base: Rect, rows: int = 1, columns: int = 1, border_colour = (255, 255, 255), fill_colour = (0, 0, 0)):
        """
        Args:
            screen: Ekran, na którym będzie wyświetlana plansza
            base (Rect): Kształt bazowy do wyświetlania planszy
            rows (int): Ilość wierszy planszy
            columns (int): Ilość kolumn planszy
            border_colour (tuple): Kolor krawędzi planszy
            fill_colour (tuple): Kolor wypełnienia planszy
        """
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
        """
        Ustawia ilość wierszy

        Args:
            rows (int): Nowa ilość wierszy
        """
        self.rows = rows
        self.update()

    def set_columns(self, columns: int):
        """
        Ustawia ilość kolumn

        Args:
            columns (int): Nowa ilość kolumn
        """
        self.columns = columns
        self.update()

    def draw(self):
        """
        Wyświetla planszę na ekranie
        """
        pygame.draw.rect(self.screen, self.border_colour, self.base, 3)
        for r in self.fields:
            for f in r:
                f.draw()

    def update(self):
        """
        Aktualizuje wygląd planszy
        """
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
        """
        Wyszukuje pola po podanych współrzędnych.

        Args:
            x (int): Współrzędna x
            y (int): Współrzędna y
        Returns:
            GridField: Pole, które zawiera dane współrzędne lub None, jeżeli takiego pola nie ma
        """
        for l in self.fields:
            for f in l:
                if f.is_in_bounds(x, y):
                    return f
        return None

    def get_field_by_index(self, x: int, y: int) -> GridField:
        """
        Wyszukuje pola po podanych indeksach.

        Args:
            x (int): Indeks kolumny
            y (int): Indeks wiersza
        Returns:
            GridField: Pole, które znajduje się w podanych koordynatach
        """
        return self.fields[x][y]

    def enable(self):
        """
        Ustawia stan planszy na aktywny
        """
        self.is_enabled = True

    def disable(self):
        """
        Ustawia stan planszy na nieaktywny
        """
        self.is_enabled = False