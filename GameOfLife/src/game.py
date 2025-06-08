from threading import Thread
from time import sleep

from src.calculator import GameCalculator
from src.model.board import Board
from src.observer.event import GameCompleteEvent, BoardUpdateEvent
from src.observer.observer import Observable


class GameOfLife(Observable):

    def __init__(self, calculator: GameCalculator, current_board: Board):
        super().__init__()
        self.calculator = calculator
        self.current_board = current_board
        self.enabled = False
        self.completed = False
        self.thread = Thread(target=self.animate)

    def start_async(self):
        self.thread.start()

    def animate(self):
        for r in range(self.current_board.get_rows()):
            for c in range(self.current_board.get_columns()):
                self.call_observers(BoardUpdateEvent(c, r, self.current_board.is_alive(c, r)))
        self.current_board = self.calculator.calculate(self.current_board)
        while self.enabled and len(self.calculator.calculate.changes) > 0:
            for coordinates in self.calculator.calculate.changes:
                c = coordinates[0]
                r = coordinates[1]
                self.call_observers(BoardUpdateEvent(c, r, self.current_board.is_alive(c, r)))
            self.current_board = self.calculator.calculate(self.current_board)
            sleep(0.5)
        if len(self.calculator.calculate.changes) == 0:
            self.enabled = False
            self.call_observers(GameCompleteEvent())

    def is_active(self):
        return self.enabled

    def is_completed(self):
        return self.completed

    def stop(self):
        self.enabled = False