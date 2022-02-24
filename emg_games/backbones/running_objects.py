import pygame
import random
import time

import numpy as np

from copy import copy

from emg_games.backbones.abstract_game import AbstractGame
from emg_games.backbones import utils
from emg_games.gui.components import palette

# TODO move to utils
MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0
NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class RunningObjects(AbstractGame):

    def __init__(self, full_screen, player):

        super().__init__(full_screen, player)

        self._backgrounds = []

        self._targets = []

        self._projectiles = []

        self._game_name = 'Running Object'

    def _move_target(self, shift):

        if not self._target:
            raise ValueError('self._target not set')
        if abs(shift) > 1:
            raise ValueError('arg must be between -1 and 1')

        self._target.x_position += self._max_shift * shift

    def _set_targets(self):

        only_target = 0

        self._target = self._targets[only_target]

        target_width, target_height = self._targets[only_target].size

        target_y_position = self._y_screen - target_height
        self._target.y_position = target_y_position
        self._target.x_position = self._x_screen // 2 - self._target.size[1] // 2

        return target_y_position

    def _set_new_projectile(self):

        projectile_index = random.randint(0, len(self._projectiles) - 1)
        self._projectile = copy(self._projectiles[projectile_index])

        self._projectile.x_position = random.randint(self._projectile.size[0], self._x_screen -
                                                     self._projectile.size[0])
        self._projectile.y_position = random.randint(-200, 0)

        self.running_projectiles.append(self._projectile)

        self.time_since_new_projectile = time.time()

        self._projectile_number += 1

    def _punctation(self, new_projectiles):

        break_loop = False
        new_projectile = False

        acceleration = 1.02 ** self._projectile_number

        y_step = self._y_screen * self._speed_rate * acceleration * 10 # tak jest ciekawiej na razie

        for (i, projectile_) in enumerate(self.running_projectiles):
            projectile_x_position, projectile_y_position = projectile_.get_position
            projectile_.y_position = projectile_y_position + y_step
            if projectile_.bottom > self._target.y_position:

                new_projectile = False
                if utils.collide_in(projectile_, self._target):
                    if self._target.type == projectile_.type:
                        self._score += 10
                    else:
                        self._lives -= 1
                        self._score += -100
                        self._missed += 1

                    new_projectile = True

                elif projectile_.top > self._y_screen:
                    if self._target.type == projectile_.type:
                        self._score -= 10
                    else:
                        self._score += 100
                    new_projectile = True

                if new_projectile:
                    new_projectiles += 1
                    self.running_projectiles.remove(projectile_)

                if self._lives <= 0:
                    break_loop = True

        return break_loop, new_projectile, new_projectiles

    def _play(self):

        np.random.shuffle(self._projectiles)
        self._set_targets()

        play = True
        new_projectiles = 1
        self._update_background()

        self.running_projectiles = []

        self.time_since_new_projectile = time.time()

        self.new_projectile_counter = time.time() + 10

        while play and self._lives > 0:

            while new_projectiles:
                self._set_new_projectile()
                new_projectiles -= 1

            if not self._lives:
                play = False

            while self.running_projectiles:

                if time.time() - self.new_projectile_counter > 0:
                    self._set_new_projectile()
                    self.new_projectile_counter = time.time() + 1 #+ 3 ** self._projectile_number

                break_loop = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._kill()

                    play, break_loop = self._escape_game(event)

                    self._keyboard_control(event, self._move_target)

                if break_loop:
                    break

                if not self._player._use_keyboard:
                    self._muscle_control(self._move_target)

                for event in pygame.event.get():
                    play, break_loop = self._escape_game(event)

                if break_loop:
                    break


                break_loop, new_projectile, new_projectiles = self._punctation(new_projectiles)

                if break_loop:
                    break

                self._screen.fill(palette.BACKGROUND_COLOR)
                self._update_background()

                self._screen.blit(self._target.image, self._target.get_position)

                for projectile_ in self.running_projectiles:
                    self._screen.blit(projectile_.image, projectile_.get_position)

                # labels with lives and score
                self._make_health_text()

                self._clock.tick(60)

        self._score = self._score
        self._save_score()

        self._what_next()

    def _update_background(self):
        pass
