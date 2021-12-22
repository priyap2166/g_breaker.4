# importing pygame library and player file to integrate
import pygame
import player
import world
import decorations
import coins
import obstacles
import health


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
        self.world = world.my_world

        # health bar instance
        self.health = health.HealthBar(20, 60, self.player.health, self.player.max_health)

        self.score_value = 100
        self.score_font = pygame.font.SysFont('Roboto', 35)
        self.score_x = 20
        self.score_y = 20

        # collision variable
        self.get_hit = False

    # function for what happens as soon as game state is called through the main menu
    def start(self):
        self.transition_target = None
        self.background_surf = pygame.Surface((800, 640))

    # function for killing screen when state is no longer in use
    def stop(self):
        self.background_surf = None

    # function for handling user events (back to main menu when user presses escape)
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.transition_target = 'main_menu'

        # keyboard input (on press)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # initiates move
                self.player.move_left = True
            if event.key == pygame.K_d:
                self.player.move_right = True
            if event.key == pygame.K_LEFT:  # allows variance in controls
                self.player.move_left = True
            if event.key == pygame.K_RIGHT:
                self.player.move_right = True
            if event.key == pygame.K_w:
                self.player.jump = True
            if event.key == pygame.K_UP:
                self.player.jump = True

        # keyboard input (on release)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:  # stops movement on release
                self.player.move_left = False
            if event.key == pygame.K_d:
                self.player.move_right = False
            if event.key == pygame.K_LEFT:
                self.player.move_left = False
            if event.key == pygame.K_RIGHT:
                self.player.move_right = False

    # update function for drawing elements onto screen
    def update(self, time_delta):
        # calling the move function on the player
        player.screen_scroll = self.player.move()

        self.window_surface.blit(self.background_surf, (0, 0))
        # updating background image
        for x in range(4):
            # repeating background and parallax scrolling
            self.window_surface.blit(self.background_image, ((x * self.width) - player.bg_scroll * 0.75, 0))
        # drawing world
        self.world.draw(self.window_surface)
        player.bg_scroll -= player.screen_scroll

        # check for collision with coin - remove coin once collected
        if pygame.sprite.spritecollide(self.player, coins.coin_group, True):
            self.score_value += 15

        # check for collision with obstacle
        if pygame.sprite.spritecollide(self.player, obstacles.obstacle_group, False) and not self.get_hit:
            self.get_hit = True
            self.player.health -= 15
            if self.score_value >= 0:
                self.score_value -= 15
            if self.score_value <= 0:
                self.score_value = 0
        if not pygame.sprite.spritecollide(self.player, obstacles.obstacle_group, False):
            self.get_hit = False

        # drawing and updating decoration tiles
        decorations.decoration_group.draw(self.window_surface)
        coins.coin_group.draw(self.window_surface)
        obstacles.obstacle_group.draw(self.window_surface)
        world.exit_group.draw(self.window_surface)

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
