import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, loc_x, loc_y, img_w, img_y, hor_flip, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/ground_1.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (img_w, img_y))
        self.image = pygame.transform.flip(self.image, hor_flip, False)
        self.rect = self.image.get_rect()
        self.rect.y = loc_y
        self.rect.x = loc_x


