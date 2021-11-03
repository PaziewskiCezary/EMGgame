import pygame


class Projectile(pygame.sprite.Sprite):
    """docstring for Trash"""

    percentage = 0.05

    def __init__(self, position=(0, 0), *, img_path, projectile_type, desired_width):
        pygame.sprite.Sprite.__init__(self)

        self.x_position, self.y_position = position
        self.type = projectile_type
        self.image = pygame.image.load(img_path).convert()
        self.image.set_colorkey((255, 255, 255))

        original_width, original_height = self.image.get_size()

        scale = desired_width / original_width

        final_width = int(original_width * scale)
        final_height = int(original_height * scale)

        self.image = pygame.transform.scale(self.image, (final_width, final_height))

        self.size = self.image.get_size()

    @property
    def get_position(self):
        return self.x_position, self.y_position

    @property
    def bottom(self):
        return self.image.get_rect()[3] + self.get_position[1]

    @property
    def top(self):
        return self.image.get_rect()[1] + self.get_position[1]

    @property
    def corners(self):
        trash_width, trash_height = self.size
        corner1_position = (self.x_position, self.y_position)
        corner2_position = (self.x_position + trash_width, self.y_position + trash_height)
        return corner1_position, corner2_position
