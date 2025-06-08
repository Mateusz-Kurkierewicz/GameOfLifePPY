from src.calculator import MooreNeighborhoodCalculator
from src.model.board import Board
from src.model.options import Options
from src.utils.util_funcs import args_validator


def board_test():
    board = Board(3, 5)
    board.print()
    print()
    board.set_alive(1, 1, True)
    board.set_alive(2, 1, True)
    board.set_alive(3, 2, True)
    board.print()
    print()
    board.update_size(4, 6, True)
    board.print()
    print()
    board.clear()
    board.print()
    print()
    board.set_alive(7, 1, True)
    board.set_alive(-10, 0, True)
    board.print()
    print()
    print(board.get_rows())
    print(board.get_columns())

def calculator_test():
    calculator = MooreNeighborhoodCalculator(Options(1, 1, [2, 3], [3], False))
    board = Board(5, 5)
    board.set_alive(2, 1)
    board.set_alive(2, 2)
    board.set_alive(2, 3)
    print(board)
    board = calculator.calculate(board)
    print(board)
    print(calculator.calculate.changes)
    board = calculator.calculate(board)
    print(board)
    print(calculator.calculate.changes)

def validator_test():
    @args_validator(state=lambda x: x in ['stopped', 'paused', 'active'])
    def test_func(state: str):
        print(state)
    test_func('stopped')
    test_func("active")
    test_func("whatever")


#board_test()
#calculator_test()
validator_test()
