import random

import pygame

from emg_games.gui.components import palette
from emg_games.backbones.components import Bat, Ball
from emg_games.backbones.utils import collision, rect_collide

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

    def _keyboard_control(self, *keys):
        pressed = pygame.key.get_pressed()
        return any(pressed[key] for key in keys)

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
            bat.x += -shift * self._keyboard_control(pygame.K_LEFT, pygame.K_a) + \
                      shift * self._keyboard_control(pygame.K_RIGHT, pygame.K_d)

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

    # def _move_projectile(self, shift):
    #     if not self._projectile:
    #         raise ValueError('self.__projectile not set')
    #     if abs(shift) > 1:
    #         raise ValueError('arg must be between -1 and 1')
    #
    #     self._projectile.x_position += self._max_shift * shift
    #
    # def _set_targets(self):
    #     number_of_targets = len(self._targets)
    #
    #     offset = (1 - number_of_targets * Target.percentage) / (number_of_targets + 1)
    #     offset = round(self._x_screen * offset)
    #
    #     first_target = 0
    #
    #     target_width, target_height = self._targets[first_target].size
    #
    #     target_y_position = self._y_screen - target_height
    #
    #     for target_number, target_ in enumerate(self._targets):
    #         target_x_position = target_width * target_number
    #         target_x_position += offset * (target_number + 1)
    #         target_.x_position = target_x_position
    #         target_.y_position = target_y_position
    #
    #     return target_y_position
    #
    # def _set_new_projectile(self):
    #
    #     projectile_index = random.randint(0, len(self._projectiles) - 1)
    #     self._projectile = self._projectiles[projectile_index]
    #
    #     # recalculate x to be in center
    #     self._projectile.x_position = self._x_screen // 2 - self._projectile.size[1] // 2
    #     self._projectile.y_position = 100
    #
    # def _punctation(self):
    #
    #     new_projectile = False
    #     actual_projectile = True
    #
    #     target_y_position = self._set_targets()
    #
    #     projectile_x_position, projectile_y_position = self._projectile.get_position
    #
    #     acceleration = 1.02 ** self._projectile_number
    #
    #     y_step = self._y_screen * self._speed_rate * acceleration
    #     self._projectile.x_position, self._projectile.y_position = \
    #         projectile_x_position, projectile_y_position + y_step
    #     if self._projectile.bottom > target_y_position:
    #         collision = False
    #         for (i, target_) in enumerate(self._targets):
    #
    #             if utils.collide_in(self._projectile, target_, 2):
    #                 collision = True
    #                 if target_.type == self._projectile.type:
    #                     self._score += 100
    #
    #                 else:
    #                     self._score += -10
    #                     self._missed += 1
    #
    #         if not collision:
    #             self._lives -= 1
    #
    #         new_projectile = True
    #         actual_projectile = False
    #
    #     return new_projectile, actual_projectile
    #
    # def _play(self):
    #     super()._play()
    #     play = True
    #
    #     new_projectile = True
    #     actual_projectile = None
    #
    #
    #     while play and self._lives > 0:
    #         if new_projectile:
    #
    #             self._set_new_projectile()
    #
    #             new_projectile = False
    #             actual_projectile = True
    #             self._projectile_number += 1
    #
    #         if not self._lives:
    #             play = False
    #
    #         while actual_projectile:
    #             break_loop = False
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     self._kill()
    #                 play, break_loop = self._escape_game(event)
    #
    #                 self._keyboard_control(event, self._move_projectile)
    #
    #             if break_loop:
    #                 break
    #
    #             if not self._player._use_keyboard:
    #                 self._muscle_control(self._move_projectile)
    #
    #             for event in pygame.event.get():
    #                 play, break_loop = self._escape_game(event)
    #
    #             if break_loop:
    #                 break
    #
    #             new_projectile, actual_projectile = self._punctation()
    #
    #             # show stuff on screen
    #             self._screen.fill(palette.BACKGROUND_COLOR)
    #
    #             self._update_background()
    #
    #             for target_ in self._targets:
    #                 self._screen.blit(target_.image, target_.get_position)
    #
    #             self._screen.blit(self._projectile.image, self._projectile.get_position)
    #
    #             self._make_health_text(emoji_name=self.emoji_name, emoji_color=self.emoji_color)
    #
    #             self._clock.tick(60)
    #
    #     self._score = self._score
    #     self._save_score()
    #
    #     self._what_next()
    #
    # def _update_background(self):
    #     pass