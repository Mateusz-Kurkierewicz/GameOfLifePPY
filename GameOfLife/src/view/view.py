from pygame_gui.elements import UIButton

from src.utils.util_funcs import args_validator
from src.utils.visuals import GridPanel


class BaseView:

    def set_inverted(self, inverted: bool): raise NotImplementedError

    def set_alive(self, row: int, column: int, alive: bool): raise NotImplementedError

    def update_size(self, rows: int, columns: int): raise NotImplementedError

    def clear_board(self): raise NotImplementedError

    def set_stay_alive_counts(self, counts: str): raise NotImplementedError

    def set_revive_counts(self, counts: str): raise NotImplementedError

    @args_validator(state=lambda x: x in ['stopped', 'paused', 'active'])
    def set_state(self, state: str): raise NotImplementedError


class PygameView(BaseView):

    def __init__(self, alive_colour, dead_colour, setup_grd: GridPanel, display_grd: GridPanel,
                 start_btn: UIButton, stop_btn: UIButton, pause_btn: UIButton,
                 alive_entry, dead_entry):
        self.alive_colour = alive_colour
        self.dead_colour = dead_colour
        self.setup_grd = setup_grd
        self.display_grd = display_grd
        self.start_btn = start_btn
        self.stop_btn = stop_btn
        self.pause_btn = pause_btn
        self.alive_entry = alive_entry
        self.dead_entry = dead_entry
        self.state = "stopped"
        self.set_state("stopped")

    def set_inverted(self, inverted: bool):
        for r in range(self.display_grd.rows):
            for c in range(self.display_grd.columns):
                f = self.display_grd.get_field_by_index(r, c)
                if f.fill_colour == self.alive_colour:
                    f.set_fill_colour(self.dead_colour)
                else:
                    f.set_fill_colour(self.alive_colour)
        temp = self.alive_colour
        self.alive_colour = self.dead_colour
        self.dead_colour = temp

    def set_alive(self, row: int, column: int, alive: bool):
        if self.state == "active":
            if alive:
                self.display_grd.get_field_by_index(row, column).set_fill_colour(self.alive_colour)
            else:
                self.display_grd.get_field_by_index(row, column).set_fill_colour(self.dead_colour)
        else:
            if alive:
                self.setup_grd.get_field_by_index(row, column).set_fill_colour(self.alive_colour)
            else:
                self.setup_grd.get_field_by_index(row, column).set_fill_colour(self.dead_colour)

    def update_size(self, rows: int, columns: int):
        self.setup_grd.set_rows(rows)
        self.setup_grd.set_columns(columns)
        self.display_grd.set_rows(rows)
        self.display_grd.set_columns(columns)

    def clear_board(self):
        for r in range(self.setup_grd.rows):
            for c in range(self.setup_grd.columns):
                self.setup_grd.get_field_by_index(r, c).set_fill_colour(self.dead_colour)
                self.display_grd.get_field_by_index(r, c).set_fill_colour(self.dead_colour)

    def set_stay_alive_counts(self, counts: str):
        self.alive_entry.set_text(counts)

    def set_revive_counts(self, counts: str):
        self.dead_entry.set_text(counts)

    @args_validator(state=lambda x: x in ['stopped', 'paused', 'active'])
    def set_state(self, state: str):
        self.state = state
        if state == "stopped":
            self.start_btn.enable()
            self.stop_btn.disable()
            self.pause_btn.disable()
        elif state == "paused":
            self.start_btn.enable()
            self.stop_btn.enable()
            self.pause_btn.disable()
        else:
            self.start_btn.disable()
            self.stop_btn.enable()
            self.pause_btn.enable()