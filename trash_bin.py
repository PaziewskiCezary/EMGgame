import pygame

class TrashBin(pygame.sprite.Sprite):
    """docstring for Trash"""

    precent = 0.1

    def __init__(self, pos=(0, 0), img_path="static/trash.png", type=None, *, width):
        pygame.sprite.Sprite.__init__(self)

        self.type = type

        self.image = pygame.image.load(img_path).convert()
        self.image.set_colorkey((255, 255, 255))

        w, h = size = self.image.get_size()

        scale = width / w

        self.image = pygame.transform.scale(self.image, (int(size[0] * scale), int(size[1] * scale)))
        self.size = self.image.get_size()
        self.image.set_colorkey((173, 170, 218))

        self.x, self.y = pos

    @property
    def pos(self):
        return self.x, self.y

    @property
    def corrners(self):
        w, h = self.size
        p1, p2 = (self.x, self.y), (self.x + w, self.y + h)
        return p1, p2

    def draw(self):
        pass

    @property
    def bottom(self):
        return self.image.get_rect()[3] + self.pos[1]

    @property
    def top(self):
        return self.image.get_rect()[1] + self.pos[1]