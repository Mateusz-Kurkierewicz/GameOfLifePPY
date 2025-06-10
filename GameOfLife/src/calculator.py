from src.model.board import Board
from src.model.options import Options
from src.utils.util_funcs import change_reporter


class GameCalculator:

    """
    Reprezentuje logikę aktualizacji planszy
    """

    @change_reporter
    def calculate(self, board: Board) -> Board:
        """
        Metoda ta definiuje w jaki sposób plansza powinna być zaktualizowama,
        czyli na jakiej zasadzie komórki na planszy powinny zmienić swój stan.
        Metoda jest udekorowana @change_reporter, zapisując w nim koordynaty
        komórek, których stan uległ zmianie.
        Args:
            board (Board): Plansza z grą
        Returns:
            Board: Zaktualizowana plansza po 1 iteracji
        """
        raise NotImplementedError


class MooreNeighborhoodCalculator(GameCalculator):

    """
    Implementuje GameCalculator bazując na sąsiedztwie Moore'a
    """

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