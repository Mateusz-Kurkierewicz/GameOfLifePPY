from src.observer.event import PropertyChangeEvent
from src.observer.observer import Observable


class Options(Observable):

    def __init__(self, board_columns: int = 20, board_rows: int = 20, stay_alive_counts: list = (2, 3), revive_counts: list = (3,),
                 inverted: bool = False, anim_speed: float = 1):
        super().__init__()
        self.board_columns = board_columns
        self.board_rows = board_rows
        self.stay_alive_counts = stay_alive_counts
        self.revive_counts = revive_counts
        self.inverted = inverted
        self.anim_speed = anim_speed

    def set_board_columns(self, board_columns: int):
        self.board_columns = board_columns
        self.call_observers(PropertyChangeEvent())

    def set_board_rows(self, board_rows: int):
        self.board_rows = board_rows
        self.call_observers(PropertyChangeEvent())

    def set_stay_alive_counts(self, stay_alive_counts: list):
        self.stay_alive_counts = stay_alive_counts
        self.call_observers(PropertyChangeEvent())

    def set_revive_counts(self, revive_counts: list):
        self.revive_counts = revive_counts
        self.call_observers(PropertyChangeEvent())

    def set_inverted(self, inverted: bool):
        self.inverted = inverted
        self.call_observers()

    def set_anim_speed(self, anim_speed: float):
        self.anim_speed = anim_speed
        self.call_observers()

    def __str__(self):
        return ("Options[\ncolumns=" + str(self.board_columns)
                + ", \nrows=" + str(self.board_rows)
                + ", \nalive_counts=" + str(self.stay_alive_counts)
                + ", \ndead_counts=" + str(self.revive_counts)
                + ", \ninverted=" + str(self.inverted)
                + "]")