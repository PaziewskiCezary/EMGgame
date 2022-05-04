try:
    from math import gcd
except ImportError:
    from fraction import gcd

from pygame.sprite import Sprite

import pygame


class Image(Sprite):

    def __init__(self, path, disp_size=(1920, 1080)):
        super(Sprite, self).__init__()

        # self.image = pygame.image.load(path).convert_alpha()

        screen_size = screen_width, screen_height = pygame.display.get_surface().get_size()

        disp_scale = gcd(*disp_size)
        disp_aspect = tuple(dim / disp_scale for dim in disp_size)
        screen_scale = gcd(*screen_size)
        screen_aspect = tuple(dim / screen_scale for dim in screen_size)

        self.image = pygame.image.load(path)
        if disp_aspect == screen_aspect:
            new_size = tuple(int(dim / disp_scale * screen_scale) for dim in self.image.get_rect().size)
            self.image = pygame.transform.smoothscale(self.image, new_size)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


if __name__ == '__main__':
    scale = 20

    screen = pygame.display.set_mode([16*scale, 9*scale])

    pygame.init()
    screen.fill((255, 255, 255))

    # I1 = Image('static/Trash/target/bio.png')
    # screen.blit(I1.image, I1.rect)

    I2 = Image('static/Trash/projectile/mixed/tea.png')
    screen.blit(I2.image, I2.rect)

    pygame.display.update()

    while True:
        pass
