from copy import deepcopy

import numpy as np

from src.exceptions import InvalidArgumentException


class Board:

    """Klasa reprezentująca planszę do gry w życie
        Klasa ta posiada metody operujące na planszy do gry w życie.
        Jest ona wyłącznie modelem, co oznacza, że nie dysponuje ona
        logiką odpowiedzialną za interfejs graficzny.
    """

    min_size = 3
    max_size = 50

    def __init__(self, columns: int, rows: int):
        """
        Args:
            columns (int): Ilość kolumn planszy
            rows (int): Ilość wierszy planszy
        Throws:
            InvalidArgumentException: Kiedy podano nieprawidłową ilość wierszy lub kolumn
        """
        self.validate_size(columns, rows)
        self.board = [np.zeros(columns, dtype=int) for _ in range(rows)]

    def get_rows(self):
        """
        Returns:
            int: Ilość wierszy planszy
        """
        return len(self.board)

    def get_columns(self):
        """
        Returns:
            int: Ilość kolumn planszy
        """
        return len(self.board[0])

    def is_alive(self, row: int, column: int):
        """
        Funkcja informuje, czy komórka o danych koordynatach jest żywa. W przypadku podania
        wartości wiersza lub kolumny wykraczającej poza wielkość planszy, zostanie obliczona
        odpowiednia reszta z dzielenia

        Args:
            row (int): Wiersz, w którym znajduje się komórka
            column (int): Kolumna, w której znajduje się komórka
        Returns:
            bool: Czy komórka o podanych koordynatach jest żywa
        """
        if row < 0: row = row % len(self.board)
        elif row >= len(self.board): row = row % len(self.board)
        if column < 0: column = column % len(self.board[0])
        elif column >= len(self.board[0]): column = column % len(self.board[0])
        return self.board[row][column] == 1

    def set_alive(self, row: int, column: int, alive: bool = True):
        """
        Ustawia wartość komórki o podanych koordynatach. W przypadku podania
        wartości wiersza lub kolumny wykraczającej poza wielkość planszy, zostanie obliczona
        odpowiednia reszta z dzielenia

        Args:
            row (int): Wiersz, w którym znajduje się komórka
            column (int): Kolumna, w której znajduje się komórka
            alive (bool): Czy komórka ma być żywa
        """
        if row < 0: row = row % len(self.board)
        elif row >= len(self.board): row = row % len(self.board)
        if column < 0: column = column % len(self.board[0])
        elif column >= len(self.board[0]): column = column % len(self.board[0])
        if alive:
            self.board[row][column] = 1
        else:
            self.board[row][column] = 0

    def update_size(self, columns: int, rows: int, save_state: bool):
        """
        Aktualizuje wymiary planszy z możliwością zapisania jej stanu. Stan zostanie
        zapisany w taki sposób, że żywe komórki zostaną odtworzone na nowej planszy
        na odpowiednich koordynatach. W przypadku, gdy któryś z wymiarów będzie mniejszy
        od aktualnego, komórki znajdujące się poza zakresem zostaną pominięte.

        Args:
            columns (int): Nowa ilość kolumn
            rows (int):  Nowa ilość wierszy
            save_state (bool):  Czy zapisać stan aktualnej planszy
        """
        self.validate_size(columns, rows)
        new_board = [np.zeros(columns, dtype=int) for _ in range(rows)]
        if save_state:
            for i in range(rows):
                for j in range(columns):
                    if not (i >= len(self.board) or j >= len(self.board[0])):
                        new_board[i][j] = self.board[i][j]
        self.board = new_board

    def clear(self):
        """
        Ustawia wszystkie komórki na martwe
        """
        for i in self.board:
            for j in range(len(i)):
                i[j] = 0

    @staticmethod
    def validate_size(columns: int, rows: int):
        """
        Weryfikuje, czy wstawiane wartości kolumn i wierszy nie wykraczają poza dozwolony zakres

        Args:
            columns (int): Ilość kolumn
            rows (int): Ilość wierszy
        """
        if columns > Board.max_size or columns < Board.min_size or rows > Board.max_size or rows < Board.min_size:
            raise InvalidArgumentException(f"Niepoprawna wysokość lub szerokość tablicy! (max:{Board.max_size}, min:{Board.min_size})")

    def print(self):
        """
        Wyświetla informacje o planszy
        """
        for a in self.board: print(a)

    def __copy__(self):
        new_board = Board(3, 3)
        new_board.board = deepcopy(self.board)
        return new_board

    def __str__(self):
        final_str = ""
        for a in self.board: final_str += str(a) + "\n"
        return final_str

