# importing pygame library to use in file
import pygame

# importing specific classes (button use) from pygame.gui library to use later
from pygame_gui.elements import UIButton
from pygame_gui import UI_BUTTON_PRESSED


# creating class for MainMenuState
class MainMenuState:
    # initialising all variables
    def __init__(self, window_surface, ui_manager):
        self.transition_target = None   # controlling where the change of state will go to
        self.window_surface = window_surface
        self.ui_manager = ui_manager    # interactivity of interface
        self.title_font = pygame.font.Font(None, 64)

        # visual elements
        self.background_img = None
        self.image = None
        self.image_pos_rect = None

        # button variables
        self.start_game_button = None
        self.settings_button = None
        self.quit_button = None

    # method - as soon as the state is run, what should happen
    def start(self):
        self.transition_target = None
        self.background_img = pygame.transform.scale(pygame.image.load('img/bg.png').convert_alpha(), (1200, 640))
        self.image = pygame.image.load('MAIN LOGO.png')     # loading logo
        self.image_pos_rect = self.image.get_rect()
        self.image_pos_rect.center = (400, 150)             # position of logo

        # positioning buttons and activating them
        self.start_game_button = UIButton(pygame.Rect((310, 250), (175, 50)),
                                          'START GAME',
                                          self.ui_manager)
        self.settings_button = UIButton(pygame.Rect((310, 325), (175, 50)),
                                        'SETTINGS',
                                        self.ui_manager)
        self.quit_button = UIButton(pygame.Rect((310, 400), (175, 50)),
                                    'QUIT',
                                    self.ui_manager)

    # killing all actions when main menu state is no longer in use
    def stop(self):
        self.background_img = None
        self.image = None
        self.image_pos_rect = None

        self.start_game_button.kill()
        self.start_game_button = None
        self.settings_button.kill()
        self.settings_button = None
        self.quit_button.kill()
        self.quit_button = None

    # handling what should happen when the button(s) are clicked
    def handle_events(self, event):
        if event.type == pygame.USEREVENT and event.user_type == UI_BUTTON_PRESSED:
            if event.ui_element == self.start_game_button:
                self.transition_target = 'game'
            elif event.ui_element == self.settings_button:
                self.transition_target = 'settings'
            elif event.ui_element == self.quit_button:
                self.transition_target = 'quit'

    # update function to draw all elements onto the screen
    def update(self, time_delta):
        self.window_surface.blit(self.background_img, (0, 0))  # clear the window to the background surface
        self.window_surface.blit(self.image, self.image_pos_rect)
        self.ui_manager.draw_ui(self.window_surface)  # Draw the UI Bits
