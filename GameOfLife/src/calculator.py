from src.board import Board
from src.options import Options
from src.utils import change_reporter


class GameCalculator:

    @change_reporter
    def calculate(self, board: Board) -> Board: raise NotImplementedError


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