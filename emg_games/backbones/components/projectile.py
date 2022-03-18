import pygame


class Projectile(pygame.sprite.Sprite):

    percentage = 0.05

    def __init__(self, position=(0, 0), *, img_path, projectile_type, desired_width, transparent=False):
        pygame.sprite.Sprite.__init__(self)

        self._x_position, self._y_position = position
        self.type = projectile_type
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = self.add_outline_to_image(self.image)
        if transparent:
            self.image.set_colorkey(self.image.get_at((0, 0)))

        self.rect = self.image.get_rect(center=(self._x_position, self._y_position))

        original_width, original_height = self.image.get_size()

        scale = desired_width / original_width

        final_width = int(original_width * scale)
        final_height = int(original_height * scale)

        self.image = pygame.transform.scale(self.image, (final_width, final_height))

        self._size = self.image.get_size()
        self.rect = self.image.get_rect(center=(self._x_position, self._y_position))
        self.mask = pygame.mask.from_surface(self.image)


    def add_outline_to_image(self, image, thickness=1, color=(0, 0, 0),
                             color_key: tuple = (0, 0, 255)):
        mask = pygame.mask.from_surface(image)
        mask_surf = mask.to_surface(setcolor=color)
        mask_surf.set_colorkey((0, 0, 0))

        new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
        new_img.fill(color_key)

        for i in -thickness, thickness:
            new_img.blit(mask_surf, (i + thickness, thickness))
            new_img.blit(mask_surf, (thickness, i + thickness))
        new_img.blit(image, (thickness, thickness))

        return new_img

    @property
    def get_position(self):
        return self._x_position, self._y_position

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
    def corners(self):
        projectile_width, projectile_height = self._size
        corner1_position = (self._x_position, self._y_position)
        corner2_position = (self._x_position + projectile_width, self._y_position + projectile_height)
        return corner1_position, corner2_position
