import pygame

from .image import Image


# class Projectile(pygame.sprite.Sprite):
class Projectile(Image):

    percentage = 0.05

    def __init__(self, position=(0, 0), *, img_path, projectile_type, desired_width, max_height_ratio=400/1920, transparent=False):
        # pygame.sprite.Sprite.__init__(self)
        super(Projectile, self).__init__(img_path)
        self.x_position, self.y_position = position
        self.type = projectile_type
        # self.image = pygame.image.load(img_path).convert_alpha()
        # if transparent:
        #     self.image.set_colorkey(self.image.get_at((0, 0)))

        original_width, original_height = self.image.get_size()

        scale = desired_width / original_width

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        max_height = pygame.display.get_surface().get_size()[1] * max_height_ratio
        if new_height > max_height:
            new_width *= max_height / new_height
            new_height = max_height

        self.image = pygame.transform.scale(self.image, (new_width, new_height))

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
    def right(self):
        return self.image.get_rect()[2] + self.get_position[0]

    @property
    def left(self):
        return self.image.get_rect()[0] + self.get_position[0]

    @property
    def corners(self):
        projectile_width, projectile_height = self.size
        corner1_position = (self.x_position, self.y_position)
        corner2_position = (self.x_position + projectile_width, self.y_position + projectile_height)
        return corner1_position, corner2_position
