from copy import deepcopy

import numpy as np

from src.exceptions import InvalidArgumentException


class Board:

    min_size = 3
    max_size = 50

    def __init__(self, columns: int, rows: int):
        self.validate_size(columns, rows)
        self.board = [np.zeros(columns, dtype=int) for _ in range(rows)]

    def get_rows(self):
        return len(self.board)

    def get_columns(self):
        return len(self.board[0])

    def is_alive(self, row: int, column: int):
        if row < 0: row = row % len(self.board)
        elif row >= len(self.board): row = row % len(self.board)
        if column < 0: column = column % len(self.board[0])
        elif column >= len(self.board[0]): column = column % len(self.board[0])
        return self.board[row][column] == 1

    def set_alive(self, row: int, column: int, alive: bool = True):
        if row < 0: row = row % len(self.board)
        elif row >= len(self.board): row = row % len(self.board)
        if column < 0: column = column % len(self.board[0])
        elif column >= len(self.board[0]): column = column % len(self.board[0])
        if alive:
            self.board[row][column] = 1
        else:
            self.board[row][column] = 0

    def update_size(self, columns: int, rows: int, save_state: bool):
        self.validate_size(columns, rows)
        new_board = [np.zeros(columns, dtype=int) for _ in range(rows)]
        if save_state:
            for i in range(rows):
                for j in range(columns):
                    if not (i >= len(self.board) or j >= len(self.board[0])):
                        new_board[i][j] = self.board[i][j]
        self.board = new_board

    def clear(self):
        for i in self.board:
            for j in range(len(i)):
                i[j] = 0

    @staticmethod
    def validate_size(columns: int, rows: int):
        if columns > Board.max_size or columns < Board.min_size or rows > Board.max_size or rows < Board.min_size:
            raise InvalidArgumentException(f"Niepoprawna wysokość lub szerokość tablicy! (max:{Board.max_size}, min:{Board.min_size})")

    def print(self):
        for a in self.board: print(a)

    def __copy__(self):
        new_board = Board(3, 3)
        new_board.board = deepcopy(self.board)
        return new_board

    def __str__(self):
        final_str = ""
        for a in self.board: final_str += str(a) + "\n"
        return final_str

