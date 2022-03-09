import random

import pygame

from emg_games.gui.components import palette
from emg_games.backbones.components import Bat, Ball
from emg_games.backbones.utils import collision, rect_collide, is_key_pressed

from emg_games.backbones import AbstractGame

NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class SimpleBreakout(AbstractGame):

    def __init__(self, full_screen, player, main_game):

        super().__init__(full_screen, player, main_game)

        self._backgrounds = []

        self._targets = []

        self._projectiles = []

        self._game_name = 'SimpleBreakout'

        self.emoji_name = None
        self.emoji_color = None

    def _update_background(self):
        pass

    def _set_targets(self):
        pass

    def _set_new_projectile(self):
        pass

    def _punctation(self):
        pass

    def _play(self):

        MAGIC_NUMBER = 25

        self._screen.fill(palette.PRIMARY_COLOR)
        pygame.display.flip()

        lives = self._max_lives
        self._score = 0
        self._lives = lives

        bat = Bat()
        bat.x = self._screen_properties.x_screen // 2
        bat.y = self._screen_properties.y_screen - 50

        ball = Ball()
        ball.x = self._screen_properties.x_screen // 2
        ball.y = self._screen_properties.y_screen // 2

        shift = 10

        while lives:
            # keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._kill()

            # update positions
            bat.x += -shift * is_key_pressed(pygame.K_LEFT, pygame.K_a) + \
                      shift * is_key_pressed(pygame.K_RIGHT, pygame.K_d)

            bat.x = min(max(0, bat.x), self._screen_properties.x_screen - bat.width)

            ball.update(screen=self._screen_properties)

            # collisions
            if ball.top <= MAGIC_NUMBER * 2:
                ball.speed_y *= -1
            elif ball.left <= 0:
                ball.speed_x *= -1
            elif ball.right >= self._screen_properties.x_screen:
                ball.speed_x *= -1
            elif rect_collide(ball, bat):
                ball.speed_y *= -1

            if ball.top >= self._screen_properties.y_screen:
                lives -= 1

            # drawings
            self._screen.fill(palette.PRIMARY_COLOR)

            bat.draw(self._screen)
            ball.draw(self._screen)

            self._make_health_text(self.emoji_name, self.emoji_color)

            self._update()
            self._clock.tick(60)

        # self._what_next()
