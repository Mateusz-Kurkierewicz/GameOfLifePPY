from threading import Thread
from time import sleep

from src.calculator import GameCalculator
from src.board import Board
from src.options import Options
from src.view import BaseView


class BaseController:

    def set_inverted(self, inverted: bool): raise NotImplementedError

    def set_board_size(self, columns: int, rows: int): raise NotImplementedError

    def set_stay_alive_counts(self, from_str: str): raise NotImplementedError

    def set_revive_counts(self, from_str: str): raise NotImplementedError

    def handle_field_click(self, row: int, column: int): raise NotImplementedError

    def start_animation(self): raise NotImplementedError

    def pause_animation(self): raise NotImplementedError

    def stop_animation(self): raise NotImplementedError


class SimpleController(BaseController):

    def __init__(self, options: Options, start_board: Board, view: BaseView, calculator: GameCalculator):
        self.options = options
        self.start_board = start_board
        self.current_board = start_board.__copy__()
        self.view = view
        self.calculator = calculator
        self.enabled = False

    def set_inverted(self, inverted: bool):
        self.view.set_inverted(inverted)

    def set_board_size(self, columns: int, rows: int):
        self.options.board_rows = rows
        self.options.board_columns = columns
        self.start_board.update_size(columns, rows, True)
        self.current_board.update_size(columns, rows, False)
        self.view.update_size(rows, columns)
        for r in range(rows):
            for c in range(columns):
                self.view.set_alive(r, c, self.start_board.is_alive(r, c))

    def set_stay_alive_counts(self, from_str: str):
        self.options.stay_alive_counts.clear()
        counts = ""
        for c in from_str:
            if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                self.options.stay_alive_counts.append(int(c))
                counts += c
        self.view.set_stay_alive_counts(counts)

    def set_revive_counts(self, from_str: str):
        self.options.revive_counts.clear()
        counts = ""
        for c in from_str:
            if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                self.options.revive_counts.append(int(c))
                counts += c
        self.view.set_revive_counts(counts)

    def handle_field_click(self, row: int, column: int):
        if self.start_board.is_alive(row, column):
            self.start_board.set_alive(row, column, False)
            self.current_board.set_alive(row, column, False)
            self.view.set_alive(row, column, False)
        else:
            self.start_board.set_alive(row, column, True)
            self.current_board.set_alive(row, column, True)
            self.view.set_alive(row, column, True)

    def start_animation(self):
        self.enabled = True
        self.view.set_state("active")
        thread = Thread(target=self.animate)
        thread.start()

    def animate(self):
        for r in range(self.current_board.get_rows()):
            for c in range(self.current_board.get_columns()):
                self.view.set_alive(c, r, self.current_board.is_alive(c, r))
        self.current_board = self.calculator.calculate(self.current_board)
        while self.enabled and len(self.calculator.calculate.changes) > 0:
            for coordinates in self.calculator.calculate.changes:
                x = coordinates[0]
                y = coordinates[1]
                self.view.set_alive(x, y, self.current_board.is_alive(x, y))
            self.current_board = self.calculator.calculate(self.current_board)
            sleep(0.5)
        if len(self.calculator.calculate.changes) == 0:
            self.enabled = False
            self.view.set_state('stopped')

    def pause_animation(self):
        self.enabled = False
        self.view.set_state("paused")

    def stop_animation(self):
        self.enabled = False
        self.current_board.clear()
        self.view.clear_board()
        self.view.set_state("stopped")