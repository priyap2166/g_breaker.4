# importing pygame library and player file to integrate
import pygame
import player
import world
import decorations
import coins
import obstacles
import health
import csv
import buttons
import settings_state
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui import UI_BUTTON_PRESSED


# creating class for game state
class GameState:
    # initialising variables
    def __init__(self, window_surface):
        self.transition_target = None
        self.window_surface = window_surface
        self.background_surf = None
        self.background_image = pygame.image.load('img/bg.png')

        # scaling background image down to fit where needed
        self.background_image = pygame.transform.scale(self.background_image, (1200, 640))
        self.width = self.background_image.get_width()

        # creating instances
        self.player = player.Character(50, 400, 7.0, 0.15, 80, 67, 0, 9)

        # health bar instance
        self.health = health.HealthBar(20, 60, self.player.health, self.player.max_health)

        # scoring variables
        self.score_value = 100
        self.score_font = pygame.font.SysFont('Roboto', 35)
        self.score_x = 20
        self.score_y = 20

        # collision variable
        self.get_hit = False

        # restart and end game variables
        self.ui_manager = pygame_gui.UIManager((settings_state.SCREEN_WIDTH,
                                                settings_state.SCREEN_HEIGHT), 'theme.json')
        self.restart_button = None
        self.end_game = False

        # game over variables
        self.game_over_text = self.score_font.render('GAME OVER!', True, (198, 90, 0))
        self.game_over_pos_rect = self.game_over_text.get_rect()

        # sounds
        self.coin_sfx = pygame.mixer.Sound('sounds/coin collect.wav')
        self.coin_sfx.set_volume(0.05)
        self.jump_sfx = pygame.mixer.Sound('sounds/jump.wav')
        self.jump_sfx.set_volume(0.05)

    # function for what happens as soon as game state is called through the main menu
    def start(self):
        self.transition_target = None
        self.background_surf = pygame.Surface((800, 640))

        # positioning buttons and activating them
        self.restart_button = UIButton(pygame.Rect((310, 300), (175, 50)),
                                       'RESTART',
                                       self.ui_manager)

    # function for killing screen when state is no longer in use
    def stop(self):
        self.background_surf = None

    # function for handling user events (back to main menu when user presses escape)
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.transition_target = 'main_menu'
        # keyboard input (on press)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:  # initiates move
                self.player.move_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.move_right = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.player.jump = True
                self.jump_sfx.play()

        # keyboard input (on release)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:  # stops movement on release
                self.player.move_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.move_right = False

        # draw restart button and go back to first level
        if event.type == pygame.USEREVENT and event.user_type == UI_BUTTON_PRESSED:
            if event.ui_element == self.restart_button:
                self.end_game = False
                world.level = 0
                player.bg_scroll = 0
                decorations.decoration_group.empty()
                coins.coin_group.empty()
                obstacles.obstacle_group.empty()
                world.exit_group.empty()
                with open(f'level{world.level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            # assigning each index in 2D list to the tile number in csv file
                            world.world_data[x][y] = int(tile)
                # creating instance of class and calling method within
                world.my_world = world.World()
                world.my_world.process_data(world.world_data)
                self.player.set_position(50, 400)  # reset the position of the player
                self.player.health = 100
                self.score_value = 0
                self.player.level_complete = False

    # when health is 0
    def game_over(self):
        self.end_game = True
        self.game_over_pos_rect.center = (400, 250)

    # update function for drawing elements onto screen
    def update(self, time_delta):
        if not self.end_game:
            if self.player.health == 0:
                self.game_over()
            # calling the move function on the player
            player.screen_scroll = self.player.move()
            self.window_surface.blit(self.background_surf, (0, 0))

            # updating background image
            for x in range(4):
                # repeating background and parallax scrolling
                self.window_surface.blit(self.background_image, ((x * self.width) - player.bg_scroll * 0.75, 0))

            # drawing world
            world.my_world.draw(self.window_surface)
            player.bg_scroll -= player.screen_scroll

            # check for collision with coin - remove coin once collected
            if pygame.sprite.spritecollide(self.player, coins.coin_group, True):
                self.score_value += 15
                self.coin_sfx.play()

            # check for collision with obstacle
            if pygame.sprite.spritecollide(self.player, obstacles.obstacle_group, False) and not self.get_hit:
                self.get_hit = True
                self.player.health -= 15
                if self.score_value >= 0:
                    self.score_value -= 15
                if self.score_value <= 0:
                    self.score_value = 0
            # when not in collision with obstacle
            if not pygame.sprite.spritecollide(self.player, obstacles.obstacle_group, False):
                self.get_hit = False

            # drawing and updating decoration tiles
            decorations.decoration_group.draw(self.window_surface)
            coins.coin_group.draw(self.window_surface)
            obstacles.obstacle_group.draw(self.window_surface)
            world.exit_group.draw(self.window_surface)

            # check is player is still alive
            if self.player.alive:
                # check if level complete trigger has been met
                if self.player.level_complete:
                    world.level += 1
                    player.bg_scroll = 0
                    world.world_data = world.reset_level()
                    self.player.set_position(50, 400)  # reset the position of the player
                    self.player.level_complete = False
                    if world.level <= world.MAX_LEVELS:
                        # load in level data and create world using csv file
                        with open(f'level{world.level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    # assigning each index in 2D list to the tile number in csv file
                                    world.world_data[x][y] = int(tile)
                        # creating instance of class and calling method within
                        world.my_world = world.World()
                        world.my_world.process_data(world.world_data)
            # displaying score
            score = self.score_font.render("SCORE : " + str(self.score_value), True, (198, 90, 0))
            score_text_pos = self.score_x, self.score_y
            self.window_surface.blit(score, score_text_pos)

            # display health bar
            self.health.draw(self.player.health, self.window_surface)

            # update sprite groups
            decorations.decoration_group.update()
            coins.coin_group.update()
            obstacles.obstacle_group.update()
            world.exit_group.update()

            # draw method imported from player + animation
            self.player.draw(self.window_surface)
            self.player.update()
            self.player.update_anim(time_delta)
            pygame.display.flip()

        if self.end_game is True:
            self.window_surface.blit(pygame.transform.scale(pygame.image.load('img/bg.png').convert_alpha(),
                                                            (1200, 640)), (0, 0))
            self.ui_manager.draw_ui(self.window_surface)
            self.window_surface.blit(self.game_over_text, self.game_over_pos_rect)
            self.ui_manager.update(time_delta)
            # processing all user interface events
            for event in pygame.event.get():
                self.ui_manager.process_events(event)
