from threading import Thread
from time import sleep

from src.calculator import GameCalculator
from src.model.board import Board
from src.model.options import Options
from src.utils.util_funcs import args_validator
from src.view.view import BaseView


class BaseController:

    def set_inverted(self, inverted: bool):
        """
        Ustawia, czy wynik pokazywać w negatywie

        Args:
            inverted (bool): czy wynik pokazywać w negatywie
        """
        raise NotImplementedError()

    def set_board_size(self, columns: int, rows: int):
        """
        Aktualizuje wymiary planszy

        Args:
            columns (int): Nowa ilość kolumn
            rows (int):  Nowa ilość wierszy
        """
        raise NotImplementedError()

    def set_stay_alive_counts(self, from_str: str):
        """
        Waliduje i aktualizuje przy jakich ilościach żywych "sąsiadów" komórka pozostaje żywa

        Args:
            from_str (str): Napis reprezentujący ilości (każdy znak to osobna ilość
        """
        raise NotImplementedError()

    def set_revive_counts(self, from_str: str):
        """
        Waliduje i aktualizuje przy jakich ilościach żywych "sąsiadów" martwa komórka ożywa

        Args:
            from_str (str): Napis reprezentujący ilości (każdy znak to osobna ilość
        """
        raise NotImplementedError()

    def handle_field_click(self, row: int, column: int):
        """
        Obsługuje zdarzenie kliknięcia na komórkę planszy

        Args:
            row (int):  Wiersz, w którym znajduje się kliknięta komórka
            column (int): Kolumna, w której znajduje się kliknięta komórka
        """
        raise NotImplementedError()

    def start_animation(self):
        """
        Zaczyna wyświetlać animację
        """
        raise NotImplementedError()

    def pause_animation(self):
        """
        Przerywa animację
        """
        raise NotImplementedError()

    def stop_animation(self):
        """
        Kończy animację
        """
        raise NotImplementedError()

    def clear_board(self):
        """
        Czyści planszę do ustawiania stanu początkowego
        """
        raise NotImplementedError()

    def set_animation_speed(self, speed: int):
        """
        Ustawia prędkość animacji
        """
        raise NotImplementedError()


class SimpleController(BaseController):

    def __init__(self, options: Options, start_board: Board, view: BaseView, calculator: GameCalculator):
        self.options = options
        self.start_board = start_board
        self.current_board = start_board.__copy__()
        self.view = view
        sac = ""
        for c in self.options.stay_alive_counts: sac += str(c)
        rc = ""
        for c in self.options.revive_counts: rc += str(c)
        self.view.set_stay_alive_counts(sac)
        self.view.set_revive_counts(rc)
        self.calculator = calculator
        self.enabled = False
        self.state = None
        self.set_state("initial")

    def set_inverted(self, inverted: bool):
        self.view.set_inverted(inverted)

    def set_board_size(self, columns: int, rows: int):
        self.options.board_rows = rows
        self.options.board_columns = columns
        self.start_board.update_size(columns, rows, True)
        self.current_board.update_size(columns, rows, False)
        self.view.update_display_size(rows, columns)
        self.view.update_setup_size(rows, columns)
        for r in range(rows):
            for c in range(columns):
                self.view.set_setup_alive(r, c, self.start_board.is_alive(r, c))

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
            self.view.set_setup_alive(row, column, False)
        else:
            self.start_board.set_alive(row, column, True)
            self.current_board.set_alive(row, column, True)
            self.view.set_setup_alive(row, column, True)

    def start_animation(self):
        if self.state == "completed":
            self.current_board = self.start_board.__copy__()
            self.view.clear_display_board()
        self.enabled = True
        self.set_state("active")
        thread = Thread(target=self.animate)
        thread.start()

    def animate(self):
        for r in range(self.current_board.get_rows()):
            for c in range(self.current_board.get_columns()):
                self.view.set_display_alive(c, r, self.current_board.is_alive(c, r))
        self.current_board = self.calculator.calculate(self.current_board)
        while self.enabled and len(self.calculator.calculate.changes) > 0:
            for coordinates in self.calculator.calculate.changes:
                x = coordinates[0]
                y = coordinates[1]
                self.view.set_display_alive(x, y, self.current_board.is_alive(x, y))
            self.current_board = self.calculator.calculate(self.current_board)
            sleep(self.options.anim_speed)
        if len(self.calculator.calculate.changes) == 0:
            self.enabled = False
            self.set_state("completed")

    def pause_animation(self):
        self.enabled = False
        self.set_state("paused")

    def stop_animation(self):
        self.enabled = False
        self.set_state("completed")

    def clear_board(self):
        self.start_board.clear()
        self.view.clear_setup_board()

    def set_animation_speed(self, speed: int):
        self.options.anim_speed = speed

    @args_validator(state=lambda x: x in ['initial', 'paused', 'active', 'completed'])
    def set_state(self, state: str):
        self.state = state
        if state == "initial":
            self.view.start_btn.enable()
            self.view.stop_btn.disable()
            self.view.pause_btn.disable()
            self.view.clear_btn.enable()
        elif state == "paused":
            self.view.start_btn.enable()
            self.view.stop_btn.enable()
            self.view.pause_btn.disable()
            self.view.clear_btn.disable()
            self.view.setup_grd.enable()
        elif state == "active":
            self.view.start_btn.disable()
            self.view.stop_btn.enable()
            self.view.pause_btn.enable()
            self.view.clear_btn.disable()
            self.view.setup_grd.disable()
        elif state == "completed":
            self.view.start_btn.enable()
            self.view.stop_btn.disable()
            self.view.pause_btn.disable()
            self.view.clear_btn.enable()
            self.view.setup_grd.enable()