# importing pygame library and player file to integrate
import pygame
import player
import world
import decorations
import coins
import obstacles
import health
import csv
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
        self.ui_manager_restart = pygame_gui.UIManager((settings_state.SCREEN_WIDTH,
                                                settings_state.SCREEN_HEIGHT), 'theme.json')
        self.restart_button = None
        self.end_game = False

        # game over variables
        self.game_over_img = pygame.transform.scale(pygame.image.load('img/game over.png'), (370, 61))
        self.game_over_img_pos_rect = self.game_over_img.get_rect()

        # pause variables
        self.pause_button = None
        self.pause = False
        self.pause_img = pygame.image.load('img/pause.png')
        self.pause_img_pos_rect = self.pause_img.get_rect()
        self.ui_manager_pause = pygame_gui.UIManager((settings_state.SCREEN_WIDTH,
                                                      settings_state.SCREEN_HEIGHT), 'theme.json')

        # resume variables
        self.resume_button = None
        self.ui_manager_resume = pygame_gui.UIManager((settings_state.SCREEN_WIDTH,
                                                       settings_state.SCREEN_HEIGHT), 'theme.json')

        # sounds
        self.coin_sfx = pygame.mixer.Sound('sounds/coin collect.wav')
        self.coin_sfx.set_volume(0.2)
        self.jump_sfx = pygame.mixer.Sound('sounds/jump.wav')
        self.jump_sfx.set_volume(0.05)
        self.over_sfx = pygame.mixer.Sound('sounds/game over.wav')
        self.over_sfx.set_volume(0.2)
        self.hit_sfx = pygame.mixer.Sound('sounds/hit.wav')
        self.hit_sfx.set_volume(0.2)

    # function for what happens as soon as game state is called through the main menu
    def start(self):
        self.transition_target = None
        self.background_surf = pygame.Surface((800, 640))

        # positioning buttons and activating them
        self.restart_button = UIButton(pygame.Rect((310, 300), (175, 50)),
                                       'RESTART',
                                       self.ui_manager_restart)

        self.pause_button = UIButton(pygame.Rect((700, 20), (80, 35)),
                                     'PAUSE',
                                     self.ui_manager_pause)

        self.resume_button = UIButton(pygame.Rect((310, 300), (175, 50)),
                                      'RESUME',
                                      self.ui_manager_resume)

    # function for killing screen when state is no longer in use
    def stop(self):
        self.background_surf = None

    # function for handling user events
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

            if event.ui_element == self.pause_button:
                self.pause = True
            if event.ui_element == self.resume_button:
                self.pause = False
                self.score_x = 20
                self.score_y = 20

    # when health is 0
    def game_over(self):
        self.end_game = True
        self.game_over_img_pos_rect.center = (400, 250)
        self.over_sfx.play()

    # update function for drawing elements onto screen
    def update(self, time_delta):
        if not self.end_game and not self.pause:
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
                self.hit_sfx.play()
                if self.player.health >= 0:
                    self.player.health -= 20
                elif self.player.health <= 0:
                    self.player.health = 0
                if self.score_value >= 0:
                    self.score_value -= 15
                elif self.score_value <= 0:
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

            self.ui_manager_pause.draw_ui(self.window_surface)  # draw button
            self.ui_manager_pause.update(time_delta)  # update ui button
            for event in pygame.event.get():
                self.ui_manager_pause.process_events(event)

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

        if self.pause is True:
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
            # processing all user interface events
            for event in pygame.event.get():
                self.ui_manager_resume.process_events(event)

        if self.end_game is True:
            # display bg image
            self.window_surface.blit(pygame.transform.scale(pygame.image.load('img/bg.png').convert_alpha(),
                                                            (1200, 640)), (0, 0))
            self.window_surface.blit(self.game_over_img, self.game_over_img_pos_rect)  # position
            self.ui_manager_restart.draw_ui(self.window_surface)  # draw button
            self.ui_manager_restart.update(time_delta)  # update ui button

            # redraw final score at position
            score = self.score_font.render(" FINAL SCORE : " + str(self.score_value), True, (198, 90, 0))
            self.score_x = 280
            self.score_y = 380
            score_text_pos = self.score_x, self.score_y
            self.window_surface.blit(score, score_text_pos)
            # processing all user interface events
            for event in pygame.event.get():
                self.ui_manager_restart.process_events(event)
