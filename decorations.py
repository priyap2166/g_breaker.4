import pygame
import player
import world


# grass and rocks - creating group
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + world.TILE_SIZE // 2, y + (world.TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += player.screen_scroll


decoration_group = pygame.sprite.Group()
