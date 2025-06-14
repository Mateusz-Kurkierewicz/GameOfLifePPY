import pygame
import pygame_gui

from src.model.board import Board
from src.calculator import MooreNeighborhoodCalculator
from src.controller.controller import SimpleController
from src.model.options import Options
from src.view.view import PygameView
from src.utils.visuals import GridPanel

options = Options(20, 20, [2, 3], [3], False, 0.5)

#główne
border_color = (40, 141, 191)
alive_color = (32, 189, 61)
dead_color = (0, 0, 0)
screen_resolution = (725, 600)
#tekst
setup_label_properties = (50, 125, 210, 20)
display_label_properties = (375, 125, 60, 20)
inverted_label_properties = (50, 475, 65, 20)
alive_label_properties = (160, 475, 100, 20)
dead_label_properties = (330, 475, 100, 20)
#przyciski
start_button_properties = (50, 50, 100, 50)
stop_button_properties = (175, 50, 100, 50)
pause_button_properties = (300, 50, 100, 50)
clear_button_properties = (425, 50, 100, 50)
#tabele
setup_rect_properties = (50, 150, 300, 300)
display_rect_properties = (375, 150, 300, 300)
#ustawienia
inverted_box_properties = (120, 475, 25, 25)
alive_entry_properties = (260, 475, 50, 30)
dead_entry_properties = (430, 475, 50, 30)
velocity_status_bar_properties = (50, 520, 200, 30)

pygame.init()
screen = pygame.display.set_mode(screen_resolution)
background = pygame.Surface(screen_resolution)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(screen_resolution)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(start_button_properties),
                                            text='Start',
                                            manager=manager)

stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(stop_button_properties),
                                            text='Stop',
                                            manager=manager)

pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pause_button_properties),
                                            text='Pauza',
                                            manager=manager)

clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(clear_button_properties),
                                            text='Wyczyść',
                                            manager=manager)

alive_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(alive_label_properties),
                                             text='Żywe przy:')

alive_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(alive_entry_properties))

dead_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(dead_label_properties),
                                             text='Ożywa przy:')

dead_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(dead_entry_properties))

inverted_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(inverted_label_properties),
                                             text='Negatyw:')

inverted_box = pygame_gui.elements.UICheckBox(relative_rect=inverted_box_properties,
                                              manager=manager,
                                              text="")

setup_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(setup_label_properties),
                                          text="Wprowadź kształt początkowy:")

setup_grid = GridPanel(screen, pygame.Rect(setup_rect_properties),
                       options.board_rows, options.board_columns, border_color, dead_color)

display_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(display_label_properties),
                                          text="Wynik:")

display_grid = GridPanel(screen, pygame.Rect(display_rect_properties),
                         options.board_rows, options.board_columns, border_color, dead_color)

# velocity_status_bar = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=velocity_status_bar_properties,
#                                                       manager=manager)


#backend
board = Board(options.board_columns, options.board_rows)
calculator = MooreNeighborhoodCalculator(options)
view = PygameView(alive_color, dead_color, setup_grid, display_grid, start_button, stop_button, pause_button, clear_button, alive_entry, dead_entry)
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
            elif event.ui_element == clear_button:
                controller.clear_board()

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == alive_entry:
                controller.set_stay_alive_counts(alive_entry.get_text())
            if event.ui_element == dead_entry:
                controller.set_revive_counts(dead_entry.get_text())

        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            controller.set_inverted(True)

        if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
            controller.set_inverted(False)

        if event.type == pygame.MOUSEBUTTONDOWN:
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
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()