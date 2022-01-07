import pygame  # import pygame library to use commands

import settings_state
import world

SCROLL_THRESH = 200  # distance player is at edge of screen before scrolling
bg_scroll = 0
screen_scroll = 0


class Character(pygame.sprite.Sprite):  # class to create a Character
    # defining attributes i.e. position of character and animation
    def __init__(self, x, y, speed, frame_speed, frame_width, frame_height, animation_row, num_frames):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1  # determines which way character is facing
        self.flip = False

        # animation variables
        sprite_sheet = pygame.image.load('img/player/sprite sheet one.png').convert_alpha()
        self.frames = []
        for frame_number in range(0, num_frames):
            self.frames.append(sprite_sheet.subsurface(pygame.Rect((frame_number * frame_width)+12,
                                                                   animation_row * frame_height,
                                                                   47, frame_height)))

        self.current_frame_index = 0
        self.display_frame = self.frames[self.current_frame_index]
        self.frame_speed = frame_speed
        self.time_accumulator = 0.0
        # creates rectangle around sprite (useful for collision)
        self.rect = self.display_frame.get_rect()
        # positions the rectangle with x and y coordinates
        self.rect.center = (x, y)
        self.width = self.display_frame.get_width()
        self.height = self.display_frame.get_height()

        # jumping variables
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.GRAVITY = 0.75

        # movement triggers
        self.move_left = False
        self.move_right = False

        # health variables
        self.health = 100
        self.max_health = self.health

        self.level_complete = False

    def move(self):
        # variables to record change in movement and reset them where necessary (collision)
        delta_x = 0
        delta_y = 0

        # local scroll variable
        screen_scrolling = 0

        # conditions to ensure which way sprite is moving and what happens when movement initiated
        if self.move_left:
            delta_x = -self.speed
            self.flip = True  # flips and changes direction of character when moving backwards
            self.direction = -1
        elif self.move_right:
            delta_x = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        # gravity
        self.vel_y += self.GRAVITY
        delta_y += self.vel_y

        # check for collision
        for tile in world.my_world.obstacle_list:
            # check collision in x direction
            if tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.width, self.height):
                delta_x = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height):
                # check if below the ground (jumping)
                if self.vel_y < 0:
                    self.vel_y = 0
                    delta_y = tile[1].bottom - self.rect.top
                # check if above the ground (falling)
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    delta_y = tile[1].top - self.rect.bottom

        # collision with edges of screen
        if self.rect.left + delta_x < 0 or self.rect.right + delta_x > settings_state.SCREEN_WIDTH:
            delta_x = 0

        # check if fallen off platform
        if self.rect.bottom > settings_state.SCREEN_HEIGHT:
            self.health = 0

        # updating position of 'rect' i.e. character
        self.rect.x += delta_x
        self.rect.y += delta_y

        # checking for collision with exit sign
        if pygame.sprite.spritecollide(self, world.exit_group, False):
            self.level_complete = True

        # update scroll based on player position
        if (self.rect.right > (settings_state.SCREEN_WIDTH - SCROLL_THRESH) and bg_scroll < 4000) \
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(delta_x)):
            self.rect.x -= delta_x
            screen_scrolling = -delta_x

        return screen_scrolling

    def update(self):
        self.rect.x += screen_scroll

    def update_anim(self, time_passed):
        self.time_accumulator += time_passed

        if self.time_accumulator > self.frame_speed:
            self.time_accumulator = 0.0
            self.current_frame_index += 1

            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0

            self.display_frame = self.frames[self.current_frame_index]

    # method for drawing any instance of the class
    def draw(self, screen):
        # transforming the character when it changes direction
        screen.blit(pygame.transform.flip(self.display_frame, self.flip, False), self.rect)
