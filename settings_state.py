import pygame

from pygame_gui.elements import UIButton
from pygame_gui import UI_BUTTON_PRESSED

# setting width and height variables of window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
FRAME_RATE = 400


class SettingsState:

    def __init__(self, window_surface, ui_manager):
        self.transition_target = None
        self.window_surface = window_surface
        self.ui_manager = ui_manager
        self.title_font = pygame.font.Font(None, 64)

        self.background_img = None
        self.title_text = None
        self.title_pos_rect = None
        self.image = None
        self.image_pos_rect = None

        self.back_button = None

    def start(self):
        self.transition_target = None
        self.background_img = pygame.transform.scale(pygame.image.load('img/bg.png').convert_alpha(), (1200, 640))
        self.image = pygame.image.load('MAIN LOGO.png')
        self.image_pos_rect = self.image.get_rect()
        self.image_pos_rect.center = (400, 150)
        self.title_text = self.title_font.render('Settings', True, (198, 90, 0))
        self.title_pos_rect = self.title_text.get_rect()
        self.title_pos_rect.center = (400, 220)

        self.back_button = UIButton(pygame.Rect((550, 550), (200, 30)),
                                    'Back to menu', self.ui_manager)

    def stop(self):
        self.background_img = None
        self.title_text = None
        self.title_pos_rect = None
        self.image = None
        self.image_pos_rect = None

        self.back_button.kill()
        self.back_button = None

    def handle_events(self, event):
        if event.type == pygame.USEREVENT and event.user_type == UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.transition_target = 'main_menu'

    def update(self, time_delta):
        self.window_surface.blit(self.background_img, (0, 0))         # clear the window to the background surface
        self.window_surface.blit(self.title_text, self.title_pos_rect)        # stick the title at the top
        self.window_surface.blit(self.image, self.image_pos_rect)
        self.ui_manager.draw_ui(self.window_surface)  # Draw the UI Bits
