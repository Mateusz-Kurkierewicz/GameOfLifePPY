import pygame
import pygame_gui

from GameOfLifeUtils import GameCalculator, Board, Options, BaseController, BaseView, args_validator, \
    MooreNeighborhoodCalculator, SimpleController
from GameOfLifeVisuals import GridPanel


class PygameView(BaseView):

    def set_inverted(self, inverted: bool): raise NotImplementedError

    def set_alive(self, row: int, column: int, alive: bool): raise NotImplementedError

    def update_size(self, rows: int, columns: int, save_state: bool): raise NotImplementedError

    def clear_board(self): raise NotImplementedError

    def set_stay_alive_counts(self, counts: str): raise NotImplementedError

    def set_revive_counts(self, counts: str): raise NotImplementedError

    @args_validator(state=lambda x: x in ['stopped', 'paused', 'active'])
    def set_state(self, state: str): raise NotImplementedError


#backend
options = Options(10, 10, [2, 3], [3], False)
board = Board(options.board_columns, options.board_rows)
calculator = MooreNeighborhoodCalculator(options)
view = PygameView()
controller = SimpleController(options, board, view, calculator)


#GUI
alive_color = (32, 189, 61)
screen_resolution = (1280, 720)
pygame.init()

screen = pygame.display.set_mode(screen_resolution)
background = pygame.Surface(screen_resolution)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(screen_resolution)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Rozpocznij',
                                            manager=manager)

stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 275), (100, 50)),
                                            text='Zakończ',
                                            manager=manager)

test_rect = pygame.Rect(350, 400, 300, 250)
test_grid = GridPanel(screen, test_rect, 3, 4, alive_color)

running = True

while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    screen.blit(background, (0, 0))

    test_grid.draw()
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()