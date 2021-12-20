# import graphical user interface and pygame library
import pygame
import pygame_gui

# importing classes from other files
import settings_state
from main_menu_state import MainMenuState
from settings_state import SettingsState
from game_state import GameState


# creating class GameApp (main start-up of game)
class GameApp:
    def __init__(self):
        pygame.init()  # initializing pygame

        pygame.display.set_caption('Ground Breaker')  # window title
        # creating window surface for game to run on
        self.window_surface = pygame.display.set_mode((settings_state.SCREEN_WIDTH,
                                                       settings_state.SCREEN_HEIGHT))
        self.ui_manager = pygame_gui.UIManager((settings_state.SCREEN_WIDTH,
                                                settings_state.SCREEN_HEIGHT), 'theme.json')
        self.clock = pygame.time.Clock()  # creating a clock
        self.running = True  # boolean variable to be involved in loop

        self.states = {'main_menu': MainMenuState(self.window_surface, self.ui_manager),
                       'settings': SettingsState(self.window_surface, self.ui_manager),
                       'game': GameState(self.window_surface), }

        self.active_state = self.states['main_menu']  # to start app with the main menu
        self.active_state.start()

    # method for when the game is run
    def run(self):
        # while loop only runs when running = True
        while self.running:
            time_delta = self.clock.tick(settings_state.FRAME_RATE)/1000.0

            # loop for when program ends when 'x' button is clicked on window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # processing all user interface events
                self.ui_manager.process_events(event)

                # calling the active state's handle_event method
                self.active_state.handle_events(event)

            # updating UI Manager with every frame
            self.ui_manager.update(time_delta)

            # updating active state every frame
            self.active_state.update(time_delta)

            # check for change in active state
            if self.active_state.transition_target is not None:
                if self.active_state.transition_target in self.states:
                    self.active_state.stop()
                    # setting active state to newly set one by user
                    self.active_state = self.states[self.active_state.transition_target]
                    self.active_state.start()
                elif self.active_state.transition_target == 'quit':
                    self.running = False

            # function to continuously update display
            pygame.display.update()


if __name__ == '__main__':
    app = GameApp()     # creating instance of GameApp class i.e. the app
    app.run()   # calling the run method on the instance
