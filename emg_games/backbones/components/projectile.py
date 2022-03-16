import pygame


class Projectile(pygame.sprite.Sprite):

    percentage = 0.05

    def __init__(self, position=(0, 0), *, img_path, projectile_type, desired_width, transparent=False):
        pygame.sprite.Sprite.__init__(self)

        self._x_position, self._y_position = position
        self.type = projectile_type
        self._image = pygame.image.load(img_path).convert()
        if transparent:
            self._image.set_colorkey(self._image.get_at((0, 0)))

        self.rect = self._image.get_rect(center=(self._x_position, self._y_position))

        original_width, original_height = self._image.get_size()

        scale = desired_width / original_width

        final_width = int(original_width * scale)
        final_height = int(original_height * scale)

        self._image = pygame.transform.scale(self._image, (final_width, final_height))

        self._size = self._image.get_size()
        self._rect = self._image.get_rect(center=(self._x_position, self._y_position))
        self._mask = pygame.mask.from_surface(self._image)

    @property
    def get_position(self):
        return self._x_position, self._y_position

    @property
    def bottom(self):
        return self._image.get_rect()[3] + self.get_position[1]

    @property
    def top(self):
        return self._image.get_rect()[1] + self.get_position[1]

    @property
    def right(self):
        return self._image.get_rect()[2] + self.get_position[0]

    @property
    def left(self):
        return self._image.get_rect()[0] + self.get_position[0]

    @property
    def corners(self):
        projectile_width, projectile_height = self._size
        corner1_position = (self._x_position, self._y_position)
        corner2_position = (self._x_position + projectile_width, self._y_position + projectile_height)
        return corner1_position, corner2_position
