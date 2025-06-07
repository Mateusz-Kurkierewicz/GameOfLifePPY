import pygame
import pygame_gui
from pygame_gui.elements import UIButton

from GameOfLifeUtils import Board, Options, BaseView, args_validator, \
    MooreNeighborhoodCalculator, SimpleController
from GameOfLifeVisuals import GridPanel, CheckBox

options = Options(20, 20, [2, 3], [3], False)

#GUI
border_color = (40, 141, 191)
alive_color = (32, 189, 61)
dead_color = (0, 0, 0)
screen_resolution = (1000, 600)
pygame.init()

#tekst
setup_label_properties = (50, 125, 210, 20)
display_label_properties = (375, 125, 60, 20)
inverted_label_properties = (50, 475, 60, 20)
alive_label_properties = (160, 475, 100, 20)
dead_label_properties = (340, 475, 100, 20)
#przyciski
start_button_properties = (50, 50, 100, 50)
stop_button_properties = (175, 50, 100, 50)
pause_button_properties = (300, 50, 100, 50)
#tabele
setup_rect_properties = (50, 150, 300, 300)
display_rect_properties = (375, 150, 300, 300)
#ustawienia
inverted_box_properties = (115, 475, 25, 25)
alive_entry_properties = (260, 475, 50, 30)
dead_entry_properties = (440, 475, 50, 30)

screen = pygame.display.set_mode(screen_resolution)
background = pygame.Surface(screen_resolution)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(screen_resolution)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(start_button_properties),
                                            text='Rozpocznij',
                                            manager=manager)

stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(stop_button_properties),
                                            text='Zakończ',
                                            manager=manager)

pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pause_button_properties),
                                            text='Pauza',
                                            manager=manager)

alive_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(alive_label_properties),
                                             text='Żywe przy:')
alive_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(alive_entry_properties))
dead_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(dead_label_properties),
                                             text='Ożywa przy:')
dead_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(dead_entry_properties))

inverted_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(inverted_label_properties),
                                             text='Negatyw')
inverted_box = CheckBox(screen, pygame.Rect(inverted_box_properties), border_color, False)

setup_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(setup_label_properties),
                                          text="Wprowadź kształt początkowy:")
setup_grid = GridPanel(screen, pygame.Rect(setup_rect_properties),
                       options.board_rows, options.board_columns, border_color, dead_color)
display_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(display_label_properties),
                                          text="Wynik:")
display_grid = GridPanel(screen, pygame.Rect(display_rect_properties),
                         options.board_rows, options.board_columns, border_color, dead_color)

#widok
class PygameView(BaseView):

    def __init__(self, alive_colour, dead_colour, setup_grd: GridPanel, display_grd: GridPanel,
                 start_btn: UIButton, stop_btn: UIButton, pause_btn: UIButton):
        self.alive_colour = alive_colour
        self.dead_colour = dead_colour
        self.setup_grd = setup_grd
        self.display_grd = display_grd
        self.start_btn = start_btn
        self.stop_btn = stop_btn
        self.pause_btn = pause_btn
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
        alive_entry.set_text(counts)

    def set_revive_counts(self, counts: str):
        dead_entry.set_text(counts)

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


#backend
board = Board(options.board_columns, options.board_rows)
calculator = MooreNeighborhoodCalculator(options)
view = PygameView(alive_color, dead_color, setup_grid, display_grid, start_button, stop_button, pause_button)
controller = SimpleController(options, board, view, calculator)

running = True

while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            controller.stop_animation()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                controller.start_animation()
            elif event.ui_element == stop_button:
                controller.stop_animation()
            elif event.ui_element == pause_button:
                controller.pause_animation()

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == alive_entry:
                controller.set_stay_alive_counts(alive_entry.get_text())
            if event.ui_element == dead_entry:
                controller.set_stay_alive_counts(dead_entry.get_text())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if inverted_box.check_click(event.pos[0], event.pos[1]):
                controller.set_inverted(inverted_box.is_clicked())
            if setup_grid.is_enabled:
                field = setup_grid.get_field_by_loc(event.pos[0], event.pos[1])
                if field is not None:
                    field.set_fill_colour(alive_color)
                    controller.handle_field_click(field.x, field.y)

        manager.process_events(event)

    manager.update(time_delta)

    screen.blit(background, (0, 0))

    setup_grid.draw()
    display_grid.draw()
    inverted_box.draw()
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()