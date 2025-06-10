class Options:

    """
    Klasa reprezentuje opcje gry
    """

    def __init__(self, board_columns: int = 20, board_rows: int = 20, stay_alive_counts: list = (2, 3), revive_counts: list = (3,),
                 inverted: bool = False, anim_speed: float = 1):
        """
        Args:
            board_columns (int): początkowa ilość kolumn planszy do gry
            board_rows (int): początkowa ilość wierszy planszy do gry
            stay_alive_counts (list): przy jakich ilościach żywych "sąsiadów" komórka pozostaje żywa
            revive_counts (list): przy jakich ilościach żywych "sąsiadów" martwa komórka ożywa
            inverted (bool): czy wynik pokazywać w negatywie
            anim_speed (float) częstotliwość aktualizacji stanu gry (w sekundach)
        """
        self.board_columns = board_columns
        self.board_rows = board_rows
        self.stay_alive_counts = stay_alive_counts
        self.revive_counts = revive_counts
        self.inverted = inverted
        self.anim_speed = anim_speed

    def set_board_columns(self, board_columns: int):
        self.board_columns = board_columns

    def set_board_rows(self, board_rows: int):
        self.board_rows = board_rows

    def set_stay_alive_counts(self, stay_alive_counts: list):
        self.stay_alive_counts = stay_alive_counts

    def set_revive_counts(self, revive_counts: list):
        self.revive_counts = revive_counts

    def set_inverted(self, inverted: bool):
        self.inverted = inverted

    def set_anim_speed(self, anim_speed: float):
        self.anim_speed = anim_speed

    def __str__(self):
        return ("Options[\ncolumns=" + str(self.board_columns)
                + ", \nrows=" + str(self.board_rows)
                + ", \nalive_counts=" + str(self.stay_alive_counts)
                + ", \ndead_counts=" + str(self.revive_counts)
                + ", \ninverted=" + str(self.inverted)
                + "]")