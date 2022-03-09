import pygame


class Bat:
    def __init__(self):

        self.x = 500
        self.y = 500
        self.width = 200
        self.height = 30

        self.color = 255, 0, 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self, value):
        self.x += value
