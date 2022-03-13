import pygame
from numpy import sign


class Target(pygame.sprite.Sprite):

    percentage = 0.1

    def __init__(self, position=(0, 0), *, img_path, target_type=None, desired_width, flippable=False, transparent=False):
        pygame.sprite.Sprite.__init__(self)

        self._x_position, self.y_position = position
        self._facing = 0
        self.type = target_type
        self._image = pygame.image.load(img_path).convert_alpha()
        if transparent:
            self._image.set_colorkey(self._image.get_at((0, 0)))

        self.flippable = flippable

        original_width, original_height = self.image.get_size()

        scale = desired_width / original_width

        final_width = int(original_width * scale)
        final_height = int(original_height * scale)

        self._image = pygame.transform.scale(self._image, (final_width, final_height))
        if flippable:
            self._image_fliped = pygame.transform.flip(self._image.copy(), True, False)

        self.size = self.image.get_size()

    @property
    def x_position(self):
        return self._x_position

    @x_position.setter
    def x_position(self, value):
        flip = sign(value-self._x_position)
        self._facing = flip if flip else self._facing
        self._x_position = value

    @property
    def image(self):
        if self.flippable:
            if self._facing == -1:
                return self._image_fliped
            else:
                return self._image

        return self._image

    @property
    def facing(self):
        return self._facing

    @property
    def get_position(self):
        return self.x_position, self.y_position

    @property
    def corners(self):
        target_width, target_height = self.size
        corner1_position = (self.x_position, self.y_position)
        corner2_position = (self.x_position + target_width, self.y_position + target_height)
        return corner1_position, corner2_position

    @property
    def bottom(self):
        return self.image.get_rect()[3] + self.get_position[1]

    @property
    def top(self):
        return self.image.get_rect()[1] + self.get_position[1]

    @property
    def right(self):
        return self.image.get_rect()[2] + self.get_position[0]

    @property
    def left(self):
        return self.image.get_rect()[0] + self.get_position[0]

    @property
    def width(self):
        return self.image.get_rect()[2]