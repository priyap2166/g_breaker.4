# importing libraries and files
import pygame

import settings_state
import csv
import player
import coins
import decorations
import obstacles

# sectioning screen and tile variables
ROWS = 16
COLS = 150
TILE_SIZE = settings_state.SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 0
MAX_LEVELS = 2

# load images
# store tiles in a list
tile_list = []
for x in range(TILE_TYPES):  # 21 tile types scaled to invisible grid size
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_list.append(img)  # list now full of tiles


# class world
class World:
    # initialising variable for ground tiles i.e. obstacle list
    def __init__(self):
        self.obstacle_list = []

    # processing all data in csv file
    def process_data(self, data):
        self.level_length = len(data[0])  # defining length level
        # go through each number in level data csv file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:  # tile name starts at 0
                    img = tile_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE  # creating a rectangle based on the position of the tile
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)  # tuple
                    if 0 <= tile <= 8:  # ground tiles
                        self.obstacle_list.append(tile_data)
                    if 11 <= tile <= 14:
                        # calling class decoration for grass and rocks
                        decoration = decorations.Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        # adds each tile in group to sprite group
                        decorations.decoration_group.add(decoration)
                    if tile == 18:
                        coin = coins.Coin(img, x * TILE_SIZE, y * TILE_SIZE)
                        coins.coin_group.add(coin)
                    if tile == 17:
                        obstacle = obstacles.Obstacle(img, x * TILE_SIZE, y * TILE_SIZE)
                        obstacles.obstacle_group.add(obstacle)
                    if tile == 20:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

    # drawing the ground tiles onto the screen, i.e. window surface
    def draw(self, screen):
        for tile in self.obstacle_list:
            tile[1][0] += player.screen_scroll
            screen.blit(tile[0], tile[1])


# exit tile class
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += player.screen_scroll


# sprite group creation
exit_group = pygame.sprite.Group()
# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# load in level data and create world using csv file
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            # assigning each index in 2D list to the tile number in csv file
            world_data[x][y] = int(tile)

# creating instance of class and calling method within
my_world = World()
my_world.process_data(world_data)
