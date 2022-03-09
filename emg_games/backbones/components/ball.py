import pygame

import random


class Ball:
    def __init__(self):

        self.x = 500
        self.y = 500
        self.width = 20
        self.height = 20

        self.speed_x = None
        while not self.speed_x:
            self.speed_x = random.randint(-3, 3)
        self.speed_y = -3

        self.color = 255, 0, 255

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def update(self, screen):
        self.x = min(max(0, self.x + self.speed_x), screen.x_screen)
        self.y = min(max(0, self.y + self.speed_y), screen.y_screen)


    @property
    def top(self):
        return self.y

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.left + self.width
