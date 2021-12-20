import pygame
import settings_state
import buttons
import csv

pygame.init()
clock = pygame.time.Clock()
FRAME_RATE = settings_state.FRAME_RATE

# level editor window
SCREEN_WIDTH = settings_state.SCREEN_WIDTH
SCREEN_HEIGHT = settings_state.SCREEN_HEIGHT
LOWER_MARGIN = 100
SIDE_MARGIN = 300


screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))

# define tile grid variables
ROWS = 16
MAX_COLS = 120
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
current_tile = 0
level = 0

# scrolling variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load image
background_img = pygame.transform.scale(pygame.image.load('img/bg.png').convert_alpha(), (1200, 640))

# storing tiles in list
tile_list = []
for n in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{n}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_list.append(img)

# saving and loading button images
save_img = pygame.image.load('img/save.png').convert_alpha()
load_img = pygame.image.load('img/load.png').convert_alpha()

# colour constants
BLUE = (62, 158, 255)
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# font
text_font = pygame.font.SysFont('Roboto', 30)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 2][tile] = 0
    world_data[ROWS - 1][tile] = 4


# output text onto screen
def draw_text(text, font, colour, x, y):
    text_img = font.render(text, True, colour)
    screen.blit(text_img, (x, y))


# function to draw bg
def draw_bg():
    screen.fill(BLUE)
    width = background_img.get_width()
    for j in range(4):
        screen.blit(background_img, ((j * width)-scroll, 0))


# draw grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE, 0), (c * TILE_SIZE, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


# draw world
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tile_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# create buttons
save_button = buttons.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 70, save_img, 0.6)
load_button = buttons.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 70, load_img, 0.6)

# button list variables
button_list = []
button_col = 0
button_row = 0

# adding buttons to list
for i in range(len(tile_list)):
    tile_button = buttons.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, tile_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

running = True
while running:

    # calling functions
    clock.tick(FRAME_RATE)
    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', text_font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('UP or DOWN to change level', text_font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load tiles
    if save_button.draw(screen):
         with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',)
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        # reset scroll variable
        scroll = 0

        # load the level data
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',',)
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    # draw tile panel and tiles
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choosing a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll map
    if scroll_left and scroll > 0:
        scroll -= 5
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5

    # add new tiles to screen
    # get position of mouse
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check coordinates are within tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # finds out value of coordinate of mouse on grid
        if pygame.mouse.get_pressed()[0] == 1:
            # adding tile with left click
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        # deleting tile with right click
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard presses
        # on press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True

        # key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False

    pygame.display.flip()

pygame.quit()
