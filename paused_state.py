# import the library pygame
import pygame
import pygame_gui

from game_state import GameState
import settings_state

from pygame_gui.elements import UIButton
from pygame_gui import UI_BUTTON_PRESSED


class PausedState(GameState):
    def __init__(self, window_surface, ui_manager):
        super().__init__(window_surface)
        self.transition_target = None
        self.window_surface = window_surface
        self.background_surf = None
        # pause variables
        self.pause = False
        self.pause_img = pygame.image.load('img/pause.png')
        self.pause_img_pos_rect = self.pause_img.get_rect()
        self.ui_manager = ui_manager
        # resume variables
        self.resume_button = None
        self.ui_manager_pause = None
        self.ui_manager_resume = None
        self.score_font = pygame.font.SysFont('Roboto', 35)
        self.pause = True

    def start(self):
        self.ui_manager_resume = pygame_gui.UIManager((settings_state.SCREEN_WIDTH,
                                                       settings_state.SCREEN_HEIGHT), 'theme.json')


        self.resume_button = UIButton(pygame.Rect((310, 300), (175, 50)),
                                      'RESUME',
                                      self.ui_manager_resume)

    def stop(self):
        self.background_surf = None
        self.resume_button.kill()
        self.resume_button = None

    def handle_events(self, event):
        if event.type == pygame.USEREVENT and event.user_type == UI_BUTTON_PRESSED:
            # exit to main menu if the back button is pressed
            if event.ui_element == self.resume_button:
                self.transition_target = 'game'
                self.score_x = 20
                self.score_y = 20

    def update(self, time_delta):

        for event in pygame.event.get():
            # display bg image
            self.window_surface.blit(pygame.transform.scale(pygame.image.load('img/bg.png').convert_alpha(),
                                                            (1200, 640)), (0, 0))
            self.window_surface.blit(self.pause_img, (240, 200))  # pause img display
            self.ui_manager_resume.draw_ui(self.window_surface)  # draw resume button
            self.ui_manager_resume.update(time_delta)  # update ui button

            # redraw current score at position
            score = self.score_font.render(" CURRENT SCORE : " + str(self.score_value), True, (198, 90, 0))
            self.score_x = 260
            self.score_y = 380
            score_text_pos = self.score_x, self.score_y
            self.window_surface.blit(score, score_text_pos)

            self.ui_manager_resume.process_events(event)
