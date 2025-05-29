import functools
import numpy as np
from copy import deepcopy


def change_reporter(func):
    def wrapper(*args, **kwargs):
        wrapper.changes = []
        return func(*args, **kwargs)
    return wrapper

def xor(bool_1: bool, bool_2: bool) -> bool:
    if (not bool_1 and bool_2) or (bool_1 and not bool_2): return True
    return False

def args_validator(**validators):
    def decorator(func):
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(len(args)):
                name = arg_names[i]
                if validators.__contains__(name) and not validators[name](args[i]):
                    raise InvalidArgumentException(f"Argument nie spełnia wymagania: {args[i]}")
            for arg in kwargs.keys():
                if validators.__contains__(arg) and not validators[arg](kwargs[arg]):
                    raise InvalidArgumentException(f"Argument nie spełnia wymagania: {kwargs[arg]}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


class InvalidArgumentException(Exception):

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class Options:

    def __init__(self, board_columns: int, board_rows: int, stay_alive_counts: list, revive_counts: list, inverted: bool):
        self.board_columns = board_columns
        self.board_rows = board_rows
        self.stay_alive_counts = stay_alive_counts
        self.revive_counts = revive_counts
        self.inverted = inverted

    def __str__(self):
        return ("Options[\ncolumns=" + str(self.board_columns)
                + ", \nrows=" + str(self.board_rows)
                + ", \nalive_counts=" + str(self.stay_alive_counts)
                + ", \ndead_counts=" + str(self.revive_counts)
                + ", \ninverted=" + str(self.inverted)
                + "]")


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


class GameCalculator:

    @change_reporter
    def calculate(self, board: Board) -> Board: raise NotImplementedError


class BaseView:

    def set_inverted(self, inverted: bool): raise NotImplementedError

    def set_alive(self, row: int, column: int, alive: bool): raise NotImplementedError

    def update_size(self, rows: int, columns: int, save_state: bool): raise NotImplementedError

    def clear_board(self): raise NotImplementedError

    def set_stay_alive_counts(self, counts: str): raise NotImplementedError

    def set_revive_counts(self, counts: str): raise NotImplementedError

    @args_validator(state=lambda x: x in ['stopped', 'paused', 'active'])
    def set_state(self, state: str): raise NotImplementedError


class BaseController:

    def set_board_size(self, columns: int, rows: int): raise NotImplementedError

    def set_stay_alive_counts(self, from_str: str): raise NotImplementedError

    def set_revive_counts(self, from_str: str): raise NotImplementedError

    def start_animation(self): raise NotImplementedError

    def pause_animation(self): raise NotImplementedError

    def stop_animation(self): raise NotImplementedError


class MooreNeighborhoodCalculator(GameCalculator):

    def __init__(self, options: Options):
        self.options = options

    @change_reporter
    def calculate(self, board: Board) -> Board:
        new_board = Board(board.get_columns(), board.get_rows())
        for i in range(board.get_rows()):
            for j in range(board.get_columns()):
                alive_neighbours = 0
                if board.is_alive(i - 1, j + 1): alive_neighbours += 1
                if board.is_alive(i, j + 1): alive_neighbours += 1
                if board.is_alive(i + 1, j + 1): alive_neighbours += 1
                if board.is_alive(i + 1, j): alive_neighbours += 1
                if board.is_alive(i + 1, j - 1): alive_neighbours += 1
                if board.is_alive(i, j - 1): alive_neighbours += 1
                if board.is_alive(i - 1, j - 1): alive_neighbours += 1
                if board.is_alive(i - 1, j): alive_neighbours += 1
                if board.is_alive(i, j):
                    if not self.options.stay_alive_counts.__contains__(alive_neighbours):
                        new_board.set_alive(i, j, False)
                        self.calculate.changes.append((i, j))
                    else:
                        new_board.set_alive(i, j, True)
                else:
                    if self.options.revive_counts.__contains__(alive_neighbours):
                        new_board.set_alive(i, j, True)
                        self.calculate.changes.append((i, j))
                    else:
                        new_board.set_alive(i, j, False)
        return new_board


class SimpleController(BaseController):

    def __init__(self, options: Options, start_board: Board, view: BaseView, calculator: GameCalculator):
        self.options = options
        self.start_board = start_board
        self.current_board = start_board.__copy__()
        self.view = view
        self.calculator = calculator
        self.enabled = False

    def set_board_size(self, columns: int, rows: int):
        self.options.board_rows = rows
        self.options.board_columns = columns
        self.start_board.update_size(columns, rows, True)
        self.current_board.update_size(columns, rows, False)
        self.view.update_size(rows, columns, False)

    def set_stay_alive_counts(self, from_str: str):
        self.options.stay_alive_counts.clear()
        counts = ""
        for c in from_str:
            if int(c) in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
                self.options.stay_alive_counts.append(int(c))
                counts += c
        self.view.set_stay_alive_counts(counts)

    def set_revive_counts(self, from_str: str):
        self.options.revive_counts.clear()
        counts = ""
        for c in from_str:
            if int(c) in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
                self.options.revive_counts.append(int(c))
                counts += c
        self.view.set_revive_counts(counts)

    def start_animation(self):
        self.enabled = True
        self.current_board = self.calculator.calculate(self.current_board)
        while self.enabled and len(self.calculator.calculate.changes) > 0:
            for coordinates in self.calculator.calculate.changes:
                x = coordinates[0]
                y = coordinates[1]
                self.view.set_alive(x, y, self.current_board.is_alive(x, y))
            self.current_board = self.calculator.calculate(self.current_board)

    def pause_animation(self):
        self.enabled = False
        self.view.set_state("paused")

    def stop_animation(self):
        self.enabled = False
        self.current_board.clear()
        self.view.clear_board()
        self.view.set_state("stopped")